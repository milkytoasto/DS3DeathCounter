class ModuleNotDiscoverable(Exception):
    def __init__(self, name):
        self.message = f"\n\nEncountered an ArgumentError while loading the module and its base address.\n"
        self.message += f"Possible Places of Concern:\n"
        self.message += f"\t- Make sure {name} is still running.\n"
        self.message += f"\t- You may be using a 32bit Python installation.\n"
        super().__init__(self.message)


class ProcessNotDiscoverable(Exception):
    def __init__(self, name):
        self.message = f"\n\nCould not find a running instance of {name}.\n"
        self.message += f"Please make sure {name} is running and try again.\n"
        super().__init__(self.message)


class ProcessUnexpectedlyClosed(Exception):
    def __init__(self):
        self.message = f"\n\nUnexpectedly lost access to the process -- did it close?\n"
        super().__init__(self.message)
