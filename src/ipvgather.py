
from lib.config import read as read_config
from lib.worker import Worker
from lib.inverter import discover
import lib.log as log
import signal
import argparse


worker = None


"""
Register signal handler
"""
def signal_handler_interrupt(signum, frame) -> None:
    global worker
    if isinstance(worker, Worker) == True:
        log.info("Signal Handler: Stop worker")
        worker.stop()
    else:
        log.debug("Signal Handler: No worker defined")
# // signal_handler_interrupt(signum, frame) -> None

# register signal handler
signal.signal(signal.SIGINT, signal_handler_interrupt)


"""
Parse command line
"""
parser = argparse.ArgumentParser(description="IPvGatherer")
parser.add_argument("-c", type=str, help="Configuration file name")
parser.add_argument("--discover", action="store_true", help="Search for an Goodwe inverter")
parser.add_argument("--check", action="store_true", help="Check the given configuration only")

args = parser.parse_args()


"""
Search for an inverter inside the network.
"""
if args.discover == True:
    log.info("Search for inverter")
    discover()
    exit()


"""
Load configuration
"""
config_file = "/etc/ipvgather.json"
if getattr(args, "c") != None and args.c != "":
    config_file = args.c

config = read_config(config_file, args.check)
if config.none():
    print("Cannot load configuration")
    exit()
config = config.get()

if args.check == True:
    print("Check config done")
    exit()


"""
Setup logging
"""
if log.setup(config.logging) == False:
    print("Cannot setup logging")
    exit()


"""
Start worker
"""
worker = Worker(config)
worker.start()
worker.join()
