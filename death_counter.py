"""
Author: MILKYTOASTO milkietoast@gmail.com
Python code for reading from DS3's memory and writing the death count
to a file. See the ProcessHandler utils file for more info on how
this is achieved.

Requires a x64 version of Python to be installed for this to work.
"""

import logging

from pymem.exception import MemoryReadError

from utils.ProcessHandler import ProcessHandler
from utils.ProcessHandler.Exceptions import (
    ProcessNotDiscoverable,
    ProcessUnexpectedlyClosed,
)

logging.basicConfig(
    format="[%(asctime)s]: %(message)s", datefmt="%d-%b-%y %H:%M:%S", level=logging.INFO
)


def get_deaths_from_pointer(pointer):
    return int.from_bytes(pointer.read(), "little")


def write_deaths(deaths):
    with open("DS3Deaths.txt", "w") as f:
        f.write("%d" % deaths)


def main():
    process_name = "DarkSoulsIII.exe"

    ph = ProcessHandler(process_name)

    gameModule = ph.base_address
    base_address = gameModule + 0x047572B8

    death_count_pointer = ph.get_pointer(
        base_address, offsets=[0x98], value_type="bytes", length=4
    )
    deaths = get_deaths_from_pointer(death_count_pointer)

    logging.info(
        f"Discovered {process_name} process. Setting current deaths to {deaths}."
    )
    write_deaths(deaths)

    death_counter = 0
    while True:
        deaths = get_deaths_from_pointer(death_count_pointer)
        if deaths != death_counter:
            death_counter = deaths

            write_deaths(deaths)
            logging.info(f"Updated death count written to file: {deaths}")


debug = False
if __name__ == "__main__":
    while True:
        try:
            logging.info("Looking for process. . .")
            while True:
                try:
                    main()
                except ProcessNotDiscoverable:
                    # Process isn't running
                    pass
                except MemoryReadError:
                    # Couldn't read pointer (usually because the process is starting up)
                    pass
                except AttributeError:
                    # Process is loading up / stalled
                    pass
        except ProcessUnexpectedlyClosed:
            # Process closed.
            logging.info(f"Process terminated.")
