import threading
import time
import signal
import asyncio
import goodwe
import syslog


from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


run = True
intervall = 1.0


#
# Setup logging
#
def log_info(msg: str):
    syslog.syslog(syslog.LOG_INFO, msg)

def log_warning(msg: str):
    syslog.syslog(syslog.LOG_WARNING, msg)

def log_error(msg: str):
    syslog.syslog(syslog.LOG_ERR, msg)

def log_debug(msg: str):
    syslog.syslog(syslog.LOG_DEBUG, msg)

def log_critical(msg: str):
    syslog.syslog(syslog.LOG_CRIT, msg)


#
# Signal handling
#
def signal_handler_interrupt(signum, frame):
    global run
    run = False
# // signal_handler_interrupt(signum, frame)


# register signal handler
signal.signal(signal.SIGINT, signal_handler_interrupt)


#
# Connect to InfluxDB
#

# You can generate an API token from the "API Tokens Tab" in the UI
influxdb_token = "U7h3UQjh_qNmxBicEJhimICqvYgYxaNlqrihA8uzgM4N-pMcmoMIbjmns83lCDpnR3ITIetH-H-hZngNU7vBOg=="
influxdb_org = "Private Test"
influxdb_bucket = "goodwe"
influxdb_client = InfluxDBClient(url="http://localhost:8086", token=influxdb_token, org=influxdb_org)
influxdb_write = influxdb_client.write_api()


#
# Create inverter object
#
def connect_to_inverter():
    # Set the appropriate IP address
    IP_ADDRESS = "192.168.1.55"

    FAMILY = "ET"  # One of ET, EH, ES, EM, DT, NS, XS, BP or None to detect inverter family automatically
    COMM_ADDR = None  # Usually 0xf7 for ET/EH or 0x7f for DT/D-NS/XS, or None for default value
    TIMEOUT = 5
    RETRIES = 3

    inverter = asyncio.run(goodwe.connect(IP_ADDRESS, COMM_ADDR, FAMILY, TIMEOUT, RETRIES))
    print(
        f"Identified inverter\n"
        f"- Model: {inverter.model_name}\n"
        f"- SerialNr: {inverter.serial_number}\n"
        f"- Version: {inverter.software_version}"
    )

    return inverter
# // connect_to_inverter()


#
# Define functionality to read out the stats
# from the inverter
#

# Read out all stats from the goodwe inverter
def read_goodwe_stats():
    global run, intervall, influxdb_bucket, influxdb_org, influxdb_write

    # connect to inverter
    inverter = connect_to_inverter()

    while run:
        # aquire data
        try:
            response = asyncio.run(inverter.read_runtime_data())
        except:
            # make logging
            log_critical("Cannot read runtime data!")

            # try to reconnect
            time.sleep(5) # wait 5sec
            inverter = connect_to_inverter()
            response = asyncio.run(inverter.read_runtime_data())

        # process data
        for sensor in inverter.sensors():
            if sensor.id_ in response:
                if sensor.id_ != "timestamp":
                    # process data
                    unit = sensor.unit
                    value = response[sensor.id_]

                    if unit == "kW":
                        value = value * 1000.0;
                        unit = "W"
                    if unit == "Wh":
                        value = value / 1000.0;
                        unit = "kWh"

                    # store data to influxdb
                    point = Point("inverter") \
                        .tag("model", inverter.model_name) \
                        .tag("serial", inverter.serial_number) \
                        .tag("sensor_id", sensor.id_) \
                        .tag("sensor_unit", unit) \
                        .tag("sensor_name", sensor.name) \
                        .field(sensor.id_, value) \
                        .time(datetime.utcnow(), WritePrecision.NS)
                    
                    influxdb_write.write(influxdb_bucket, influxdb_org, point)
                
        
        time.sleep(intervall)
# // read_goodwe_stats()

print(datetime.now())

# start intervall thread
timerThread = threading.Thread(target=read_goodwe_stats)
timerThread.daemon = True
timerThread.start()
timerThread.join()

influxdb_client.close()

print(datetime.now(), "\nExit\n")
