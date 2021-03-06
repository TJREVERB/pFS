from time import time as sys_time

from MainControlLoop.lib.StateFieldRegistry import StateFieldRegistry, StateField


class SystemTimeReadTask:

    def __init__(self, state_field_registry: StateFieldRegistry):
        self.state_field_registry: StateFieldRegistry = state_field_registry

    def execute(self):
        current_time: float = sys_time()
        self.state_field_registry.update(StateField.TIME, current_time)
        if self.state_field_registry.get(StateField.BOOT_TIME) == -1:
            self.state_field_registry.update(StateField.BOOT_TIME, current_time)
