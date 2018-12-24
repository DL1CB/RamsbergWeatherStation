from machine import Pin, ADC, I2C 
from bme280 import BME280

""" initilize the i2c bus and the bme280 temperature, humidity and pressure sensor """
#i2c = I2C(scl=Pin(2), sda=Pin(0))
#bme280 = BME280(i2c=i2c)
annemometerPin = Pin(4, Pin.IN)
winddirecitonPin = ADC(0)     
#sucessLED = Pin(6, Pin.OUT)
#sucessLED.value(1)

_annemometerCount = 0
_winddirraw = 250
_windspeedraw = 40
_tempraw = 27.5
_humidraw = 91
_pressureraw = 102096
_soiltempraw = 10
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
    #_tempraw, _pressureraw, _humidraw = bme280.read_compensated_data()
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