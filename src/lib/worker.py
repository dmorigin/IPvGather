
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
        self._config = config
        self._run = True
        self._inverter = None
        self._influxdb = None
        self._thread = threading.Thread(
            target=self.run,
            name="IPyGatherWorker",
            daemon=True
        )

    # // __init__(self, config: ConfigWorker) -> None

    """
    Entry method for the thread. This is the main process.
    """
    def run(self) -> None:

        """
        Main worker loop. Inside this loop everything will be initalized
        and startet. It calls self::_update_data() that processing the
        update routine.
        """
        while self._run:

            try:
                log.info("worker.thread: Connect to end points")

                # Connect to inverter
                self._inverter = Inverter(self._config.inverter)
                if self._inverter.connect():
                    # Connect to influx db
                    self._influxdb = InfluxDB(self._config.influxdb)
                    self._influxdb.connect()
                    if self._influxdb.build_sensor_cache(self._inverter):
                        log.info("worker.thread: Start update data")
                        self.update_data()
                    else:
                        log.error("worker.thread: Failed to build sensor cache data")

            except Exception as err:
                log.error(err)

            log.info("worker.thread: Disconnect from end points")

            # Disconnect from influx db
            if isinstance(self._influxdb, InfluxDB):
                self._influxdb.close()
                self._influxdb = None
            
            # Disconnect from inverter
            if isinstance(self._inverter, Inverter):
                self._inverter.close()
                self._inverter = None
            
            # If something went wrong, wait some time and
            # retry again. Only worker isn't stopped.
            if self._run:
                time.sleep(self._config.worker.err_pause)

    # // _run() -> None


    """
    Inside this method all data are updated from the inverter
    and stored into influx db.
    """
    def update_data(self) -> None:
    
        count = 0
        updates = 0
        last = time.time()

        while self._run:
            res = self._influxdb.update(self._inverter)
            if res.is_error():
                log.error(res.err())
                return
            
            # do some statistics
            count = count + 1
            updates = updates + res.result().get()
            cur = time.time()
            diff = cur - last
            if diff >= 600: # every 10min
                log.info(f"ipvgather.statistics: Avg Sec/Batches: {round(diff / count, 4)}s")
                log.info(f"ipvgather.statistics:      Runtime: {round(diff, 4)}s")
                log.info(f"ipvgather.statistics:      Batches: {count}")
                log.info(f"ipvgather.statistics:      Updates: {updates}")
                last = cur
                count = 0
                updates = 0

            # sleep for some time
            time.sleep(self._config.worker.intervall)
        # // while self._run:

    # // update_data(self) -> None


    """
    """
    def join(self) -> None:
        self._thread.join()


    """
    """
    def start(self) -> None:
        self._thread.start()


    """
    """
    def stop(self) -> None:
        self._run = False