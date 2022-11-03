
import json
import io
from typing import Dict

from .option import Option, none, some


"""
Informations to connect to the InfluxDB 2
"""
class ConfigInfluxDB:
    url: str
    token: str
    organisation: str
    bucket: str

    def __init__(self, items: Dict) -> None:
        for key, value in items.items():
            self.__setattr__(key, value)

    def __str__(self) -> str:
        res = "ConfigInfluxDB: {\n"
        for attr in filter(lambda attr: attr.startswith("__") == False, dir(self)):
            res = res + "  " + attr + " = " + str(self.__getattribute__(attr)) + "\n"
        return res + "}\n"


"""
"""
class ConfigInverterSensors:
    def __init__(self, items: Dict) -> None:
        self.add = []
        self.ignore = []

        for key, value in items.items():
            self.__setattr__(key, value)

    def __str__(self) -> str:
        res = "ConfigInverterSensors: {\n"
        for attr in filter(lambda attr: attr.startswith("__") == False, dir(self)):
            res = res + "  " + attr + " = " + str(self.__getattribute__(attr)) + "\n"
        return res + "}\n"



"""
Informations to connect to the inverter himself
"""
class ConfigInverter:
    def __init__(self, items: Dict) -> None:
        self.ip = "" # 192.168.1.55
        self.family = "" # One of ET, EH, ES, EM, DT, NS, XS, BP or None to detect inverter family automatically
        self.comm_addr = None # Usually 0xf7 for ET/EH or 0x7f for DT/D-NS/XS, or None for default value
        self.timeout = 1
        self.retries = 3
        self.sensors = ConfigInverterSensors(items.get("sensors", dict()))

        for key, value in items.items():
            if key != "sensors":
                self.__setattr__(key, value)

    def __str__(self) -> str:
        res = "ConfigInverter: {\n"
        for attr in filter(lambda attr: attr.startswith("__") == False, dir(self)):
            res = res + "  " + attr + " = " + str(self.__getattribute__(attr)) + "\n"
        return res + "}\n"


"""
Setup logging

 :syslog    Set value to True to use syslog for logging. Default is false
 :file      If you don't use syslog, a log file must be given.
 :level     A numeric value to setup log level
            0 - Infos
            1 - Warnings
            2 - Errors ( Default )
            3 - Debug
"""
class ConfigLogging:
    syslog: bool
    file: str
    level: int

    def __init__(self, items: Dict) -> None:
        self.syslog = False
        self.file = "/var/log/ipvgather.log"
        self.level = 2
    
        for key, value in items.items():
            self.__setattr__(key, value)

    def __str__(self) -> str:
        res = "ConfigLogger: {\n"
        for attr in filter(lambda attr: attr.startswith("__") == False, dir(self)):
            res = res + "  " + attr + " = " + str(self.__getattribute__(attr)) + "\n"
        return res + "}\n"


"""
"""
class ConfigWorker:
    def __init__(self, items: Dict) -> None:
        self.intervall = 1 # process data every 1s
        self.err_pause = 10 # wait 10s after an error

        for key, value in items.items():
            self.__setattr__(key, value)

    def __str__(self) -> str:
        res = "ConfigWorker: {\n"
        for attr in filter(lambda attr: attr.startswith("__") == False, dir(self)):
            res = res + "  " + attr + " = " + str(self.__getattribute__(attr)) + "\n"
        return res + "}\n"


"""
Configuration object
"""
class Config(object):
    def __init__(self,
        influxdb: ConfigInfluxDB,
        inverter: ConfigInverter,
        logging: ConfigLogging,
        worker: ConfigWorker
    ) -> None:
        self.influxdb = influxdb
        self.inverter = inverter
        self.logging = logging
        self.worker = worker

    def __str__(self) -> str:
        res = "Config: {\n"
        for attr in filter(lambda attr: attr.startswith("__") == False, dir(self)):
            res = res + "  " + attr + " = " + str(self.__getattribute__(attr)) + "\n"
        return res + "}\n"


"""
Read out a given json file to generate
a config object.
"""
def read(file: str, probe: bool = False) -> Option:
    try:
        if probe == True:
            print(f"Read config file: {file}")

        fp = io.open(file, "r")
        data = json.load(fp)
        fp.close()

        if probe == True:
            print("Raw Data read: \n=========================================\n",
                f"{data}\n",
                "=========================================\n"
            )

        # create config objects
        influxdb = ConfigInfluxDB(data.get("influxdb", dict()))
        inverter = ConfigInverter(data.get("inverter", dict()))
        logging = ConfigLogging(data.get("logging", dict()))
        worker = ConfigWorker(data.get("worker", dict()))

        config = Config(influxdb, inverter, logging, worker)
        if probe == True:
            print(f"{config}")

        #return some(Config(influxdb, inverter, logging, worker))
        return some(config)

    except Exception as err:
        print(err.with_traceback())
        return none()
# // read(file: str) -> Option

"""
conf = read("test.json")
if conf.some():
    print(f"{conf.get()}")
else:
    print("Failed")
"""