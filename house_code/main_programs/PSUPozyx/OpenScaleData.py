## import the serial library
import serial
##import string


fileName= input('Enter file name: ') #ask user to name the file

####fileType= input('Enter file type: ') #ask the user or choose for the user?
fileType= '.csv'

def OpenScaleData():
    ser=serial.Serial('COM8',4800)
    ser2=serial.Serial('COM11', 1200)

## open text file to store the current 
    text_file = open(fileName+fileType, 'w')
    text_file.write(' ,time,force,units, ,x ,y ,z, \n')
## read serial data from arduino 
    while 1:
        if ser.inWaiting():

            x=ser.readline()
            print(x)
            text_file.write(str (x))


            
##        if ser2.inWaiting():
            x1=ser2.readline() 
            print(x1)
##        data= int(filter(str.isdigit, x))
            text_file.write(str (x1))
            text_file.write('\n')
            if x1=='\n':
                text_file.seek(0)
                text_file.truncate()
            text_file.flush()

## close the serial connection and text file
    text_file.close()
    ser.close()
    ser2.close()
OpenScaleData()
