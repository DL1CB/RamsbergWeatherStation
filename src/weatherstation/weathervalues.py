from driver import winddirraw, windspeedraw, tempraw, humidraw, pressureraw, soiltempraw, soilmoistureraw
from conversions import c_to_f, translate, pulses_to_mps, mps_to_mph, pa_to_inhg, dewpointf
from config import readperiod

def winddir():
    """ [0-360 instantaneous wind direction] """
    return round(translate(winddirraw(), 0, 1024, 0, 360), 0)

def windspeedmph(): 
    """ [mph instantaneous wind speed] """
    return mps_to_mph(pulses_to_mps(windspeedraw(),  readperiod))

def windgustmph(): 
    """ [mph current wind gust, using software specific time period] """
    pass

def windgustdir(): 
    """ [0 -360 using software specific time period] """
    pass

def windspdmph_avg2m():  
    """ [mph 2 minute average wind speed mph] """
    pass

def winddir_avg2m(): 
    """ [0-360 2 minute average wind direction] """
    pass

def windgustmph_10m():
     """ [mph past 10 minutes wind gust mph ] """
     pass

def windgustdir_10m(): 
    """ [0-360 past 10 minutes wind gust direction] """
    pass

def humidity():
    """ [% outdoor humidity 0-100%] """
    return humidraw() * 100 // 100

def dewptf():
    """ [F outdoor dewpoint F] """
    return dewpointf(tempf(),humidity())

def tempf():
     """ [F outdoor temperature] """ 
     return c_to_f(tempraw())

def rainin():
     """ [rain inches over the past hour)] """ 
     pass

def dailyrainin(): 
    """ [rain inches so far today in local time] """
    pass

def baromin(): 
    """[barometric pressure inches]"""
    return pa_to_inhg(pressureraw())

def soiltempf():
    """ [F soil temperature] """
    return c_to_f(soiltempraw())

def soilmoisture():
    """ [%] """
    return soilmoistureraw()
