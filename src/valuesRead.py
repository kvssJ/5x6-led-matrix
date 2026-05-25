import numpy as np
import serial
import time
from struct import * # import everything from the struct package

check = True
ArduinoNano = serial.Serial(baudrate = 115200, timeout = 1, port = 'COM3')
time.sleep(2)

file_path = "src\led_matrix_information.txt"
file = open(file_path, 'r')
rows  = file.readlines()
rowsUpload = []
lines = 0
for line in rows:
    if line[-1] == '\n':
        rowsUpload.append(line[:-1])
    else:
        rowsUpload.append(line)  
     

while True:
    if ArduinoNano.in_waiting:
        arduinoMsg = ArduinoNano.readline().decode("utf-8", errors = "ignore").strip()
        
        if arduinoMsg == "S":
            
           if(len(rowsUpload[lines])>5):
              
                
                numsList = [int(x) for x in rowsUpload[lines].split()]
                del numsList[19]
                del numsList[15]
                del numsList[11]
                del numsList[7]
                del numsList[3]

                bytesList = bytearray(numsList)
                print(str(lines) + " " + str(numsList))
                
                ArduinoNano.write(bytes([0xAA, lines%6]) +bytesList) 
               
                ArduinoNano.flush()
            
                lines  = lines + 1
                if(lines>=len(rowsUpload)):
                    break
                


ArduinoNano.close()
            
            
                
            
            
            
        

           
           

"""
data = np.genfromtxt(file_path, delimiter= " ")
# an array for each column - R, G, B, Brightness arrays in each column. An arary for time
column1 = [data[:, 0], data[:,1], data[:, 2], data[:, 3]]
column2 = [data[:, 4], data[:,5], data[:, 6], data[:, 7]]
column3 = [data[:, 8], data[:,9], data[:, 10], data[:, 11]]
column4 = [data[:, 12], data[:,13], data[:, 14], data[:, 15]]
column5 = [data[:, 16], data[:,17], data[:, 18], data[:, 19]]
timeUpdate = data[:, 20]
dataSend = 0

"""


