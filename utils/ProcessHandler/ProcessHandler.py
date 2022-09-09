from ctypes import ArgumentError

from pymem import Pymem
from pymem.exception import ProcessNotFound
from pymem.process import module_from_name

from utils.ProcessHandler.Exceptions import *
from utils.ProcessHandler.Pointer import Pointer


class ProcessHandler:
    """
    Class that takes the name of a program and
    stores its base address and pymem object.

    Will also provide pointer objects when given
    a base address, offsets, and type.
    """

    def __init__(self, name):
        self.name = name
        try:
            self.pm = Pymem(name)
            try:
                module = module_from_name(self.pm.process_handle, name)
                self.base_address = module.lpBaseOfDll
            except ArgumentError:
                raise ModuleNotDiscoverable(name)
        except ProcessNotFound:
            raise ProcessNotDiscoverable(name)

    def get_pointer(self, base, offsets=False, value_type=None, length=None):
        address = self.get_pointer_address(base, offsets)
        return Pointer(address, value_type, self.pm, length)

    def get_pointer_address(self, base, offsets=False):
        addr = self.pm.read_ulonglong(base)

        if not offsets:  # No offsets, return address
            return addr

        for i in offsets[:-1]:  # Loop over all but the last
            addr = self.pm.read_ulonglong(addr + i)
        return addr + offsets[-1]
