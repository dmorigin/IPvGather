

import time
import lib.log as log

from .config import ConfigInfluxDB
from .inverter import Inverter, DeviceInfo
from .sensors import Sensor
from .option import none, some, Option
from .error import ok, result, error, Result, Error

from goodwe import SensorKind
from typing import Any, Dict, List
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
#from influxdb_client.client.write_api import SYNCHRONOUS



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


class SensorCacheData:
    def __init__(self, value: Any) -> None:
        self.value = value
        self.time = time.time()


class SensorCache:
    def __init__(self, sensor: Sensor) -> None:
        self._sensor = sensor
        self._cache = none()

    def __eq__(self, __o: object) -> bool:
        return self._sensor == __o

    def set_cache(self, value: Any) -> None:
        self._cache = some(SensorCacheData(value))

    def get_cache(self) -> Option:
        return self._cache


"""

"""
class InfluxDB:

    def __init__(self, config: ConfigInfluxDB) -> None:
        self._config = config
        self._client = None
        self._writer = None
        self._cache = List[SensorCache]


    """
    Connect to InfluxDB setting up in config
    """
    def connect(self) -> None:
        self._client = InfluxDBClient(url=self._config.url, token=self._config.token, org=self._config.organisation)
        self._writer = self._client.write_api(batch_size=100)
        log.info("influxdb.connect: connection initiated")

    # // connect(self) -> None


    """
    """
    def close(self) -> None:
        if isinstance(self._client, InfluxDBClient) == True:
            self._client.close()
        self._client = None
        self._writer = None
        self._cache.clear()
        log.info("influxdb.close: connection closed")
    # // close(self) -> None


    """
    """
    def build_sensor_cache(self, inverter: Inverter) -> bool:
        sensors = inverter.sensors()
        if sensors.some():
            self._cache = list(map(
                lambda item: SensorCache(item),
                sensors.get()
            ))

            return len(self._cache) > 0

        log.error("influxdb.cache: No sensor data found")
        return False
    # // build_sensor_cache(self, inverter: Inverter) -> None


    """
    Aquire the data from the inverter directly and store this single
    dataset into the database.
    """
    def update(self, inverter: Inverter) -> Result:
        # Aquire device info
        device_info = inverter.device_info()
        if device_info.some():
            device_info = device_info.get()
        else:
            log.warning("influxdb.update: No device information found")

        # Update from inverter
        response = inverter.update()
        if response.some():
            # store data in database
            res = self.store(
                device_info,
                response.get()
            )

            if res.is_ok():
                log.debug(f"influxdb.update: {res.result().get()} sensors written")
                return result(res.result().get())

            log.error(res)
            return error(res.err())
        # // if response.some():

        log.error("influxdb.update: No response available")
        return error(Error.from_msg("No response available"))
    # // update(self, inverter: Inverter) -> Result


    """
    Stores all sensor data into the database.
    """
    def store(self, device_info: DeviceInfo, response: Dict[str, Any]) -> Result:
        if self._writer == None:
            log.error("influxdb.store: No writer api set")
            return False

        collection = []

        for item in self._cache:
            if item._sensor.id in response:
                value = response[item._sensor.id]

            # check cache
            if self._config.use_cache:
                cache = item.get_cache()
                if cache.some():
                    cache = cache.get()
                    cur = time.time()
                    if (cur - cache.time) > self._config.force_write or value != cache.value:
                        collection.append(InfluxDB.make_point(item._sensor, device_info, value))
                        log.debug(f"influxdb.store: update:{item._sensor.id}")
                    else:
                        log.debug(f"influxdb.store: ignore:{item._sensor.id} / value:{value}=={cache.value}")

                # update cache
                item.set_cache(value)
            else:
                collection.append(InfluxDB.make_point(item._sensor, device_info, value))

        # Write all sensor data
        if len(collection) > 0:
            written = self._writer.write(
                bucket = self._config.bucket,
                org = self._config.organisation,
                record = collection
            )
            return result(len(collection))

            print(written)
        return result(0)

    # // store(self, device_info: DeviceInfo, response: Dict[str, Any]) -> Result


    """
    Returns a single Point instance for the InfluxDB write API.
    """
    def make_point(sensor: Sensor, device_info: DeviceInfo, value: Any) -> Point:
        return Point(sensorkind_to_string(sensor.kind)) \
            .tag("model", device_info.model) \
            .tag("serial", device_info.serial) \
            .tag("sensor_name", sensor.name) \
            .tag("sensor_unit", sensor.unit) \
            .field(sensor.id, value) \
            .time(datetime.utcnow(), WritePrecision.NS)

    # // make_point(sensor: Sensor, device_info: DeviceInfo, value: Any) -> Point

# // class InfluxDB
