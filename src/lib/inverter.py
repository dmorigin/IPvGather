
from .config import ConfigInverter
from .option import Option, none, some
from .sensors import get as get_sensor_list

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
        self.config = config
        self.inverter = None
        self.deviceinfo = None
        self.sensor_map = ()

    """
    Connect to Goodwe Inverter
    """
    def connect(self) -> bool:
        try:
            self.inverter = asyncio.run(goodwe.connect(
                self.config.ip,
                self.config.comm_addr,
                self.config.family,
                self.config.timeout,
                self.config.retries))

            log.info("Inverter::connect(): Connected")
            log.info("Inverter::connect(): Identified")
            log.info(f"     - Model: {self.inverter.model_name}")
            log.info(f"     - SerialNr: {self.inverter.serial_number}")
            log.info(f"     - Version: {self.inverter.software_version}")

            # Build device info
            self.deviceinfo = DeviceInfo(self.inverter)

            # Generate sensor list
            self.sensor_map = get_sensor_list(
                self.inverter.sensors(),
                self.config.sensors.add,
                self.config.sensors.ignore
            )

            return True
        except goodwe.InverterError as err:
            log.error("Inverter::connect(): Cannot connect to inverter")
            log.error(err)
            return False
    # // connect(config: config.ConfigInverter)


    """
    """
    def close(self) -> None:
        self.inverter = None
        self.sensor_map = tuple()
        log.info("Inverter::close(): Disconnected")
    # // close(self) -> None


    """
    """
    def update(self) -> Option:
        try:
            if self.inverter != None:
                return some(asyncio.run(self.inverter.read_runtime_data()))
            else:
                log.error("Inverter::update(): No inverter connected")
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
        return some(self.sensor_map)
    # // sensors(self) -> Option


    """
    """
    def device_info(self) -> Option:
        if isinstance(self.inverter, goodwe.Inverter) == True:
            return some(self.deviceinfo)
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
    if isinstance(inverter, goodwe.Inverter) == True:
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
