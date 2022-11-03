
import lib.log as log

from .config import ConfigInfluxDB
from .inverter import Inverter

from goodwe import Sensor, SensorKind
from typing import Any, Dict, Tuple
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS



# You can generate an API token from the "API Tokens Tab" in the UI
#influxdb_token = "U7h3UQjh_qNmxBicEJhimICqvYgYxaNlqrihA8uzgM4N-pMcmoMIbjmns83lCDpnR3ITIetH-H-hZngNU7vBOg=="
#influxdb_org = "Private Test"
#influxdb_bucket = "goodwe"
#influxdb_client = InfluxDBClient(url="http://localhost:8086", token=influxdb_token, org=influxdb_org)
#influxdb_write = influxdb_client.write_api()


"""
Convert the sensor kind to a string. The kind of the sensor
is used for the messurment name.
"""
def sensorkind_to_string(k: SensorKind) -> str:
    if k == SensorKind.PV:
        return "pv"
    elif k == SensorKind.AC:
        return "ac"
    elif k == SensorKind.UPS:
        return "ups"
    elif k == SensorKind.BAT:
        return "battery"
    elif k == SensorKind.GRID:
        return "grid"
    
    return "inverter"


"""

"""
class InfluxDB:

    def __init__(self, config: ConfigInfluxDB) -> None:
        self.config = config
        self.client = None
        self.writer = None


    """
    Connect to InfluxDB setting up in config
    """
    def connect(self) -> None:
        self.client = InfluxDBClient(url=self.config.url, token=self.config.token, org=self.config.organisation)
        self.writer = self.client.write_api()
        log.info("InfluxDB::connect(): connection initiated")
    # // connect(self) -> None


    """
    """
    def close(self) -> None:
        if isinstance(self.client, InfluxDBClient) == True:
            self.client.close()
        self.client = None
        self.writer = None
        log.info("InfluxDB::close(): connection closed")
    # // close(self) -> None


    """
    Aquire the data from the inverter directly and store this single
    dataset into the database.
    """
    def update(self, inverter: Inverter) -> bool:
        # Aquire device info
        device_info = inverter.device_info()
        if device_info.some() == True:
            device_info = device_info.get()
            model = device_info.model
            serial = device_info.serial
        else:
            log.warning("InfluxDB::update(): No device information found")

        # Update from inverter
        response = inverter.update()
        sensors = inverter.sensors()
        if response.some() and sensors.some():
            # store data in database
            return self.store(
                model,
                serial,
                sensors.get(),
                response.get()
            )

        log.error("InfluxDB::update(): No response or sensors available")
        return False
    # // update(self, inverter: Inverter) -> bool
    

    """
    Stores a dataset into the database.
    """
    def store(self, model: str, serial: str, sensors: Tuple[Sensor, ...], response: Dict[str, Any]) -> bool:
        if self.writer == None:
            log.error("InfluxDB::store(): No writer api set")
            return False

        for sensor in sensors:
            if sensor.id_ in response:
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
                point = Point(sensorkind_to_string(sensor.kind)) \
                    .tag("model", model) \
                    .tag("serial", serial) \
                    .tag("sensor_name", sensor.name) \
                    .tag("sensor_unit", unit) \
                    .field(sensor.id_, value) \
                    .time(datetime.utcnow(), WritePrecision.NS)
                
                self.writer.write(self.config.bucket, self.config.organisation, point)
        
        return True

    # // def store(sensors)
# // class InfluxDB