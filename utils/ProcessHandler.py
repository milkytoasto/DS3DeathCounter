'''
Author: MILKYTOASTO milkietoast@gmail.com
Python code for writing to / reading from memory using pymem.

The goal of this implementation is to make it easy and simple to use 
by creating pointer objects with functions that take a minimal amount 
of arguments.
'''

from pymem import Pymem
from pymem.process import module_from_name
from pymem.exception import ProcessNotFound
from functools import wraps
import ctypes

class ProcessHandler():
    '''
    Class that takes the name of a program and
    stores its base address and pymem object.

    Will also provide pointer objects when given
    a base address, offsets, and type.
    '''    
    def __init__(self, name):
        self.name = name
        try:
            self.pm = Pymem(name)
            try:
                module = module_from_name(self.pm.process_handle, name)
                self.base_address = module.lpBaseOfDll
            except AttributeError:
                print(f'Encountered an AttributeError while loading the module and its base address.')
                print(f'Possible Places of Concern:')
                print(f'- Make sure {name} is still running.')
                print(f'- You may be using a 32bit Python installation.')
                print(f'Exiting')
                exit()
            except ctypes.ArgumentError:
                print(f'Encountered an ArgumentError while loading the module and its base address.')
                print(f'Possible Places of Concern:')
                print(f'- Make sure {name} is still running.')
                print(f'- You may be using a 32bit Python installation.')
                print(f'Exiting')
                exit()
        except ProcessNotFound:
            print(f'Could not find a running instance of {name}.')
            print(f'Please launch {name} and try again.')
            print(f'Exiting')
            exit()
        except Exception as e: # As of Python 3.6 exceptions can be used as string literals
            print(f'Unhandled exception: {e}')
            print(f'Exiting')
            exit()

    def get_pointer(self, base, offsets=False, value_type=None, length=None):
        address = self.get_pointer_address(base, offsets)
        return Pointer(address, value_type, self.pm, length)

    def get_pointer_address(self, base, offsets=False):
        addr = self.pm.read_ulonglong(base)

        if not offsets: # No offsets, return address
            return addr

        for i in offsets[:-1]: # Loop over all but the last
            addr = self.pm.read_ulonglong(addr + i)
        return addr + offsets[-1]

def check_process(fn):
    '''
    Wrapper that exits the program when it can't
    find the process.

    @TODO: See if there's a better solution.
    '''
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        try:
            self.pm.process_base
        except Exception as e:
            print(f'Check for process failed. It may no longer be running.')
            print(f'Unhandled exception: {e}')
            print(f'Exiting.')
            exit()
        output = fn(self, *args, **kwargs)
        return output
    return wrapper

class Pointer():
    '''
    Pointer class that takes an address, value type,
    and pymem object and provides functions for
    reading / writing to that address.

    The value type is the value you expect to be at
    that address.

    @TODO: Make variables for all of the
    different types that the user can import and
    reference when creating pointer objects.
    '''        
    def __init__(self, address, value_type, pm, length=None):
        self.address = address
        self.type = value_type
        self.length = length
        self.pm = pm

    @check_process
    def read(self):
        if self.type == 'float':
            return self.pm.read_float(self.address)
        elif self.type == 'bytes':
            return self.pm.read_bytes(self.address, length=self.length)
        elif self.type == 'aob':
            return self.pm.read_bytes(self.address, length=self.length)
        return False

    @check_process
    def write(self, value):
        if self.type == 'float':
            self.pm.write_float(self.address, float(value))
            return True
        elif self.type == 'bytes':
            self.pm.write_bytes(self.address, value, length=self.length)
            return True
        elif self.type == 'aob':
            self.pm.write_bytes(self.address, value, length=self.length)
            return True
        return False
    
    def __str__(self):
        output = self.read()
        return str(output)
