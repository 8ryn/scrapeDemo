import requests
from bs4 import BeautifulSoup
from softioc import softioc, builder
import cothread
import logging

#logging.basicConfig(level=logging.INFO, force=True)

#Device prefix
builder.SetDeviceName("bryn")

#URL to read weather data from
url = 'https://www.bbc.co.uk/weather/2647114'

maxTInput = builder.aIn('maxT', initial_value=-999)
minTInput = builder.aIn('minT', initial_value=-999)

# Get the IOC started
builder.LoadDatabase()
softioc.iocInit()

def getTemps():
    while True:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        allTempLines = soup.find_all(class_='wr-value--temperature--c')
        maxTemp = int(allTempLines[0].text[:-1]) #Today's max is first instance
        minTemp = int(allTempLines[1].text[:-1]) #Today's min is second
        logging.info('New max =%i', maxTemp)
        logging.info('Previous max=%i', maxTInput.get())
        logging.info('New min =%i', minTemp)
        logging.info('Previous min=%i', minTInput.get())
        maxTInput.set(maxTemp)
        minTInput.set(minTemp)
        cothread.Sleep(5)


cothread.Spawn(getTemps)

cothread.WaitForQuit()