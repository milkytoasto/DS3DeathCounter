from utils.ProcessHandler.Exceptions import *
from pymem.exception import ProcessError

from functools import wraps

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
        except ProcessError:
            raise ProcessUnexpectedlyClosed()
        except Exception as e:
            raise ProcessUnexpectedlyClosed()
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