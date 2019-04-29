# init wifi
# start drivers
# take raw data
# scale, convert and map raw data to measurment values
# send measurements to wunderground
# reboot every hour

try:
    import asyncio
except (ImportError):
    import uasyncio as asyncio   
    from wifi import joinwifi    
 
from driver import readrawdata
from wunderground import updatewunderground, printvalues
from config import readperiod

async def readrawdataTask():
    """ driver reads the raw data from the hardware """
    while 1:
        ## do some updating
        readrawdata()
        await asyncio.sleep(readperiod)

async def updateWundergroundTask():
    """ send the processed weather data to the wunderground cloud"""
    while 1:
        joinwifi()
        await asyncio.sleep(10)
        updatewunderground()
        printvalues()

def run():
    """ get thw wifi going then push data to the wunderground cloud """

    print('starting Ramsberg weatherstation to wunderground upload')

    loop = asyncio.get_event_loop()

    loop.create_task( updateWundergroundTask() )
    loop.create_task( readrawdataTask() )  

    loop.run_forever()

if __name__ == "__main__":
    run()


    