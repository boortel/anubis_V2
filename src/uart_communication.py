import serial
import serial.tools.list_ports

def set_light(intensity, lightID, comport):
    with serial.Serial(comport, 
                    baudrate=9600, 
                    parity=serial.PARITY_NONE, 
                    bytesize=serial.EIGHTBITS, 
                    stopbits=serial.STOPBITS_ONE) as port:
        msg = bytes(f'$set_light;{intensity};{lightID}\n', "utf-8")
        port.write(msg)

def set_speed(intensity, comport):
    with serial.Serial(comport, 
                    baudrate=9600, 
                    parity=serial.PARITY_NONE, 
                    bytesize=serial.EIGHTBITS, 
                    stopbits=serial.STOPBITS_ONE) as port:
        msg = bytes(f'$set_speed;{intensity}\n', "utf-8")
        port.write(msg)

def change_direction(direction, comport):
    with serial.Serial(comport, 
                    baudrate=9600, 
                    parity=serial.PARITY_NONE, 
                    bytesize=serial.EIGHTBITS, 
                    stopbits=serial.STOPBITS_ONE) as port:
        msg = bytes(f'$change_direction;{direction}\n', "utf-8")
        port.write(msg)

def toggle_rotation(state, comport):
    with serial.Serial(comport, 
                    baudrate=9600, 
                    parity=serial.PARITY_NONE, 
                    bytesize=serial.EIGHTBITS, 
                    stopbits=serial.STOPBITS_ONE) as port:
        msg = bytes(f'$toggle_rotation;{state}\n', "utf-8")
        port.write(msg)
    
def toggle_light(state, lightID, comport):
    with serial.Serial(comport, 
                    baudrate=9600, 
                    parity=serial.PARITY_NONE, 
                    bytesize=serial.EIGHTBITS, 
                    stopbits=serial.STOPBITS_ONE) as port:
        msg = bytes(f'$toggle_light;{state};{lightID}\n', "utf-8")
        port.write(msg)
    
def get_com_ports():
    return([dev[0] for dev in serial.tools.list_ports.comports()])