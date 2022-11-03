
import threading
import time
import lib.log as log
from .config import Config
from .influxdb import InfluxDB
from .inverter import Inverter


class Worker:
    """
    Initialize worker. This method also generates the worker
    thread, but not start it. You have to start the thread
    by calling Worker::start().
    """
    def __init__(self, config: Config) -> None:
        self.config = config
        self.run = True
        self.inverter = None
        self.influxdb = None
        self.thread = threading.Thread(
            target=self._run,
            name="IPyGatherWorker",
            daemon=True
        )
        self.test = 1

    # // __init__(self, config: ConfigWorker) -> None

    """
    Entry method for the thread. This is the main process.
    """
    def _run(self) -> None:

        """
        Main worker loop. Inside this loop everything will be initalized
        and startet. It calls self::_update_data() that processing the
        update routine.
        """
        while self.run:

            try:
                log.info("Worker::thread: Connect to end points")

                # Connect to influx db
                self.influxdb = InfluxDB(self.config.influxdb)
                self.influxdb.connect()

                # Connect to inverter
                self.inverter = Inverter(self.config.inverter)
                if self.inverter.connect() == True:
                    log.info("Worker::thread: Start update data")
                    self._update_data()

            except Exception as err:
                log.error(err)

            log.info("Worker::thread: Disconnect from end points")

            # Disconnect from influx db
            if isinstance(self.influxdb, InfluxDB) == True:
                self.influxdb.close()
                self.influxdb = None
            
            # Disconnect from inverter
            if isinstance(self.inverter, Inverter) == True:
                self.inverter.close()
                self.inverter = None
            
            # If something went wrong, wait some time and
            # retry again. Only worker isn't stopped.
            if self.run == True:
                time.sleep(self.config.worker.err_pause)


    # // _run() -> None


    """
    Inside this method all data are updated from the inverter
    and stored into influx db. If something went wrong, this method
    returns False.
    """
    def _update_data(self) -> bool:
    
        count = 0
        last = time.time()

        while self.run:
            if self.influxdb.update(self.inverter) == False:
                return False
            
            # do some statistics
            count = count + 1
            cur = time.time()
            diff = cur - last
            if diff >= 600: # every 10min
                log.info(f"ipvgather.statistics: Avg Sec/Update: {((diff) / count)}s / {count} updates in {(diff)}s")
                last = cur
                count = 0

            # sleep for some time
            time.sleep(self.config.worker.intervall)
        return True
    # // _update_data(self) -> bool


    """
    """
    def join(self) -> None:
        self.thread.join()


    """
    """
    def start(self) -> None:
        self.thread.start()


    """
    """
    def stop(self) -> None:
        self.run = False