import serial
import serial.tools.list_ports

baudrate_sett = 9600
parity_sett = serial.PARITY_NONE
bytesize_sett = serial.EIGHTBITS
stopbits_sett = serial.STOPBITS_ONE
timeout_sett = 0.5


def set_light(intensity, lightID, comport):
    try:
        with serial.Serial(comport, 
                        baudrate=baudrate_sett, 
                        parity=parity_sett, 
                        bytesize=bytesize_sett, 
                        stopbits=stopbits_sett,
                        write_timeout=timeout_sett) as port:
            msg = bytes(f'$set_light;{intensity};{lightID}\n', "utf-8")
            port.write(msg)
            return 0
    except:
        return 1

def set_speed(intensity, comport):
    try:
        with serial.Serial(comport, 
                        baudrate=baudrate_sett, 
                        parity=parity_sett, 
                        bytesize=bytesize_sett, 
                        stopbits=stopbits_sett,
                        write_timeout=timeout_sett) as port:
            msg = bytes(f'$set_speed;{intensity}\n', "utf-8")
            port.write(msg)
            return 0
    except:
        return 1

def change_direction(direction, comport):
    try:
        with serial.Serial(comport, 
                        baudrate=baudrate_sett, 
                        parity=parity_sett, 
                        bytesize=bytesize_sett, 
                        stopbits=stopbits_sett,
                        write_timeout=timeout_sett) as port:
            msg = bytes(f'$change_direction;{direction}\n', "utf-8")
            port.write(msg)
            return 0
    except:
        return 1

def toggle_rotation(state, comport):
    try:
        with serial.Serial(comport, 
                        baudrate=baudrate_sett, 
                        parity=parity_sett, 
                        bytesize=bytesize_sett, 
                        stopbits=stopbits_sett,
                        write_timeout=timeout_sett) as port:
            state = int(state)
            msg = bytes(f'$toggle_rotation;{state}\n', "utf-8")
            port.write(msg)
            return 0
    except:
        return 1
    
def toggle_light(state, lightID, comport):
    try:
        with serial.Serial(comport, 
                        baudrate=baudrate_sett, 
                        parity=parity_sett, 
                        bytesize=bytesize_sett, 
                        stopbits=stopbits_sett,
                        write_timeout=timeout_sett) as port:
            state = int(state)
            msg = bytes(f'$toggle_light;{state};{lightID}\n', "utf-8")
            port.write(msg)
            return 0
    except:
        return 1
    
def get_com_ports():
    return([dev[0] for dev in serial.tools.list_ports.comports()])


    