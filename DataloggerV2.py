import time
import csv
import datetime
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import numpy as np
from random import randint
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(27,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15,GPIO.OUT)

GPIO.output(15,GPIO.HIGH)
Boost=[]
Oil=[]
FuelP=[]
FSH=[]
RSH=[]
RWS=[]
CP=[]

# trigger program,
while GPIO.input(27)==1:
    while GPIO.input(17)==1:
        
        #Create the SPI Bus
        spi=busio.SPI(clock=board.SCK,MISO=board.MISO, MOSI=board.MOSI)
        
        #Create the CS (Chip Select)
        cs=digitalio.DigitalInOut(board.D22)
        
        #Create the MCP object
        mcp=MCP.MCP3008(spi,cs)
        
        #Create an analog input channel on pin 0
        chan0=AnalogIn(mcp,MCP.P0)
        chan1=AnalogIn(mcp,MCP.P1)
        
        #Sensor RAW Channels
        S1=[0,65536] # Map Sensor
        S2=[0,65536] # Oil Pressure
        S3=[0,65536] # Fuel Pressure
        S4=[0,65536] # Front Shock Height
        S5=[0,65536] # Rear Shock Height
        S6=[0,65536] # Rear Wheel Speed
        S7=[0,65536] # Coolant Pressure 
        S8=[0,65536]
        S9=[0,65536]
        S10=[0,65536]
        S11=[0,65536]
        S12=[0,65536]
        S13=[0,65536]
        S14=[0,65536]
        S15=[0,65536]
        S16=[0,65536]
        
        #Sensor Bounds
        Y1=[-14.5,43.5]  # Map Sensor
        Y2=[0,100]       # Oil Pressure
        Y3=[0,100]       # Fuel Pressure
        Y4=[0,100]       # Front Shock Height
        Y5=[0,100]       # Rear Shock Height
        Y6=[0,100]       # Rear wheel speed 
        Y7=[0,100]       # Coolant Pressure Sensor
        Y8=[0,100]
        Y9=[0,100]
        Y10=[0,100]
        Y11=[0,100]
        Y12=[0,100]
        Y13=[0,100]
        Y14=[0,100]
        Y15=[0,100]
        Y16=[0,100]
        
        # Interpolation data
        boost=np.interp(chan0.value,S1,Y1)
        oil=np.interp(chan1.value,S2,Y2)
        fuelp=randint(0,100)
        fsh=randint(0,100)
        rsh=randint(0,100)
        rws=randint(0,100)
        cp=randint(0,100)
        
        # Appending  
        Boost.append(boost)
        Oil.append(oil)
        FuelP.append(fuelp)
        FSH.append(fsh)
        RSH.append(rsh)
        RWS.append(rws)
        CP.append(cp)
        
        #Create Rows
        header=["Boost"]
        row= Boost
        #Create CSV
        with open("Datalog.csv", 'w+',newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(header)
            csv_writer.writerow(row)
            print(Boost)
            time.sleep(.001)