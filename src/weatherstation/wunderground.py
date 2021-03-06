try:
    import urllib.urequest as request
except ImportError:
    import urllib.request as request

from config import stationid, stationkey

from weathervalues import winddir, windspeedmph, humidity, dewptf, tempf, baromin, soiltempf, soilmoisture

def printvalues():

    print('{:<15} {:>1}'.format( 'winddir', winddir() )),
    print('{:<15} {:>1}'.format( 'windspeedmph', windspeedmph())),
    print('{:<15} {:>1}'.format( 'humidity', humidity())),
    print('{:<15} {:>1}'.format( 'dewptf', dewptf())),
    print('{:<15} {:>1}'.format( 'tempf', tempf())),
    print('{:<15} {:>1}'.format( 'baromin', baromin())), 
    print('{:<15} {:>1}'.format( 'soiltempf', soiltempf())),
    print('{:<15} {:>1}'.format( 'soilmoisture', soilmoisture()))
    print('------------------------')


def updatewunderground():
    """ generates the update url """

    url = ''.join([
    'http://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?',
    'ID={}'
    '&PASSWORD={}',
    '&dateutc=now',
    '&winddir={}',
    '&windspeedmph={}',
    '&humidity={}',
    '&dewptf={}',
    '&tempf={}',
    '&baromin={}', 
    '&soiltempf={}',
    '&soilmoisture={}',
    '&action=updateraw']).format(
        stationid,
        stationkey,
        winddir(),
        windspeedmph(),
        humidity(),
        dewptf(),
        tempf(),
        baromin(), 
        soiltempf(),
        soilmoisture()
    )

    try:
        r = request.urlopen(url)
    except Exception as e:
        print('could not send data to wunderground')
        print(e)
    


if __name__ == "__main__":
    printvalues()
    updatewunderground()