
from .config import ConfigInverter
from .option import Option, none, some
from .sensors import get as get_sensor_list, Sensor
from typing import List

import lib.log as log
import goodwe
import asyncio


"""
"""
class DeviceInfo:
    def __init__(self, inverter: goodwe.Inverter) -> None:
        self.configuration_url = "https://www.semsportal.com"
        self.host = inverter.host
        self.manufacturer = "GoodWe"
        self.model = inverter.model_name
        self.serial = inverter.serial_number
        self.sw_version = f"{inverter.software_version} ({inverter.arm_version})"


"""
"""
class Inverter:
    def __init__(self, config: ConfigInverter) -> None:
        self._config = config
        self._inverter = None
        self._deviceinfo = None
        self._sensors = List[Sensor]

    """
    Connect to Goodwe Inverter
    """
    def connect(self) -> bool:
        try:
            self._inverter = asyncio.run(goodwe.connect(
                self._config.ip,
                self._config.comm_addr,
                self._config.family,
                self._config.timeout,
                self._config.retries))

            log.info("inverter.connect: Connected")
            log.info("inverter.connect: Identified")
            log.info(f"     - Model: {self._inverter.model_name}")
            log.info(f"     - SerialNr: {self._inverter.serial_number}")
            log.info(f"     - Version: {self._inverter.software_version}")

            # Build device info
            self._deviceinfo = DeviceInfo(self._inverter)

            # Generate sensor list
            self._sensors = get_sensor_list(
                self._inverter.sensors(),
                self._config.sensors.add,
                self._config.sensors.ignore
            )

            return True
        except goodwe.InverterError as err:
            log.error("inverter.connect: Cannot connect to inverter")
            log.error(err)
            return False
    # // connect(config: config.ConfigInverter)


    """
    """
    def close(self) -> None:
        self._inverter = None
        self._sensors = tuple()
        log.info("inverter.close: Disconnected")
    # // close(self) -> None


    """
    """
    def update(self) -> Option:
        try:
            if self._inverter != None:
                return some(asyncio.run(self._inverter.read_runtime_data()))
            else:
                log.error("inverter.update: No inverter connected")
                return none()
        except goodwe.RequestFailedException as err:
            log.error(err)
            return none()
        
        # MaxRetriesException
        # RequestFailedException
    # // read(inverter)


    """
    """
    def sensors(self) -> Option:
        return some(self._sensors)
    # // sensors(self) -> Option


    """
    """
    def device_info(self) -> Option:
        if isinstance(self._inverter, goodwe.Inverter):
            return some(self._deviceinfo)
        return none()

# // class Inverter


"""
Searches for inverters inside your network. It returns a list of all
inverters that can be found. Use this method generate your configuration.
"""
def discover() -> None:
    # Search for inverter
    found = asyncio.run(goodwe.search_inverters()).decode("utf-8").split(",")

    # Discover inverter
    inverter = asyncio.run(goodwe.discover(found[0], 8899))
    if isinstance(inverter, goodwe.Inverter):
        print(
            f"Identified inverter\n"
            f"- Model: {inverter.model_name}\n"
            f"- SerialNr: {inverter.serial_number}\n"
            f"- Version: {inverter.software_version}\n"
            f"- IP: {found[0]}\n"
            f"- MAC: {found[1]}\n"
            f"- Name: {found[2]}"
        )
# // discover() -> None
