'''
Author: MILKYTOASTO milkietoast@gmail.com
Python code for reading from DS3's memory and writing the death count
to a file. See the ProcessHandler utils file for more info on how
this is achieved.

Requires a x64 version of Python to be installed for this to work.
'''


from utils.ProcessHandler import ProcessHandler


if __name__ == "__main__":
    ph = ProcessHandler("DarkSoulsIII.exe")
    gameModule = ph.base_address
    base_address = gameModule + 0x047572B8
    death_count_pointer = ph.get_pointer(base_address, offsets=[0x98], value_type="bytes", length=4)

    death_counter = 0
    while True:
        deaths = int.from_bytes(death_count_pointer.read(), "little")
        if deaths != death_counter:
            death_counter = deaths
            with open('DS3Deaths.txt', 'w') as f:
                f.write('%d' % deaths)
