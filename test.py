import serial
import serial.tools.list_ports
 
port_list = list(serial.tools.list_ports.comports())
 
if len(port_list) <= 0:
    print("The Serial port can't find!")
     
else:
    port_list_0 =list(port_list[0])
 
    port_serial = port_list_0[0]
    print(port_list_0)
 
    ser = serial.Serial(port_serial,9600,timeout = 60)
 
    print("check which port was really used >",ser.name)