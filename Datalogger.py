import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import numpy as np
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(27,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15,GPIO.OUT)

GPIO.output(15,GPIO.HIGH)
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
        S1=[0,65536]
        S2=[0,65536]
#Sensor Bounds
        Y1=[-14.5,43.5]  # Map Sensor
        Y2=[0,100]       # Oil Pressure
# Interpolation data
        Map=np.interp(chan0.value,S1,Y1)
        Oil=np.interp(chan1.value,S2,Y2)
        print("Boost",Map)
        print("Oil Pressure",Oil)
        time.sleep(.5)