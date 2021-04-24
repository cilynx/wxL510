import pylibmodbus
from parameters import Config

class VFD():
    def __init__(self, portname, slaveaddress):
        self.config = Config()
        self.modbus = pylibmodbus.ModbusRtu(portname.encode(), 19200, "N".encode(), 8, 1)
        self.modbus.set_debug(True)
        self.modbus.rtu_set_rts(1) # MODBUS_RTU_RTS_UP 1
        self.modbus.set_slave(slaveaddress)
        self.is_connected = False

    def connect(self):
        self.is_connected = True if self.modbus.connect() == None else False
        return self.is_connected

    def disconnect(self):
        self.modbus.close()
        self.is_connected = False

    def parameter(self, parameter):
        address = 0x100 * int(parameter.group.num) + int(parameter.num)
        print("Reading:",address)
        value = self.modbus.read_registers(address, 1)
        if len(value) == 1:
            try:
                return parameter.options[str(value[0])]
            except:
                return value[0] * parameter.scale
