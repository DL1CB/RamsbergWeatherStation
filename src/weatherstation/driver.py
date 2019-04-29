from machine import Pin, ADC, I2C 
from bme280 import BME280

"""
The Driver is Written for a Nodemcu 
Pins
5   SCL BME280
4   SDA BME280
14  Wind Aneemometer Switch
0   Wind Direction Potentiometer
"""

""" initilize the i2c bus and the bme280 temperature, humidity and pressure sensor """
i2c = I2C(scl=Pin(5), sda=Pin(4))
bme280 = BME280(i2c=i2c)

annemometerPin = Pin(12, Pin.IN, Pin.PULL_UP)
winddirecitonPin = ADC(0)     

_annemometerCount = 0
_winddirraw = 0
_windspeedraw = 0
_tempraw = 0
_humidraw = 100
_pressureraw = 102000
_soiltempraw = 0
_soilmoistureraw = 100

# define interupt handler
def interruptHandler(pin):
    """ each pulse of the wind annemeter is counted """
    global _annemometerCount
    _annemometerCount = _annemometerCount + 1

# bind interupthandler ot interupt
annemometerPin.irq(trigger=Pin.IRQ_FALLING, handler=interruptHandler)

def readrawdata():
    """ reads the raw data from the sensors """
    global _annemometerCount
    global _winddirraw
    global _windspeedraw
    global _tempraw
    global _humidraw
    global _pressureraw
    global _soiltempraw

    _winddirraw = winddirecitonPin.read()
    _tempraw, _pressureraw, _humidraw = bme280.read_compensated_data()
    _windspeedraw = _annemometerCount
    _annemometerCount = 0 # resent the annemometerCount

def winddirraw():
    """ reads a raw analog value [0-1024] representing the winddirection """
    return _winddirraw

def windspeedraw():
    """ reads a raw counted value representing the windspeed in puleses per 10 seconds """
    return _windspeedraw

def tempraw():
    """ reads a raw analog value representing the temperature in celcius """
    return _tempraw

def humidraw():
    """ reads a raw analog value representing the humidity in % """
    return _humidraw

def pressureraw():
    """ reads a raw analog value representing the pressure in pascal """
    return _pressureraw

def soiltempraw():
    """ reads a raw analog value representing the raw soil temperature """
    return _soiltempraw

def soilmoistureraw():
    """ reads a raw analog value representing the raw soil moisture """
    return _soilmoistureraw