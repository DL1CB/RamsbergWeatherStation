

def c_to_f(celsius):
    """ conversion of celcius to farenheit """
    fahrenheit = round((celsius * 1.8) + 32, 2)
    return fahrenheit

def translate(value, leftMin, leftMax, rightMin, rightMax):
    """ transaltes a range in input value to a range of output values """
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def pulses_to_mps(pulses, period=10):
    """ calcualtes wind speed in meters per second, based on #pulsed and sameling period """
    return pulses / (period * 4) # there are 4 pulses per rotation of the annemometer
    
def mps_to_kmh(mps):
    kph = 3.6 * mps    
    return round(kph, 4)

def mps_to_mph(mps):
    mph = 2.23694 * mps    
    return mph

def pa_to_inhg(pa):
    """ pascal to inches mercury 1Pa= 0.0002952998inHg"""
    inhg = pa * 0.0002952998
    return round(inhg, 4)


def dewpointf(tempf, humidity):
    """ calculates the dewpoint in farenheit from relative humididty and temperature """
    return round(tempf - ((100-humidity) / 2.778), 2)
    