import requests
from bs4 import BeautifulSoup
from softioc import softioc, builder
import cothread
from cothread.catools import *
import logging

class Weather:
    
    def getSoup(url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup

    def getMaxT(soup):
        tempLine = soup.find(class_='wr-value--temperature--c')  #Today's max is first instance
        maxTemp = int(tempLine.text[:-1])
        return maxTemp
    
    def getMinT(soup):
        tempLine = soup.find_all(class_='wr-value--temperature--c')[1] #Today's min is second instance
        minTemp = int(tempLine.text[:-1])
        return minTemp
    
    def getLoc(soup):
        locLine=soup.find(class_='wr-c-location__name')
        location = locLine.find("span").previous_sibling #Gets just the location avoiding weather warning
        return location

#logging.basicConfig(level=logging.INFO, force=True)

#Device prefix
builder.SetDeviceName("bryn")

#Create PVs
maxTInput = builder.aIn('maxT', initial_value=-999)
minTInput = builder.aIn('minT', initial_value=-999)
urlOutput = builder.stringOut('url', initial_value='https://www.bbc.co.uk/weather/2647114')
locInput = builder.stringIn('loc')

# Get the IOC started
builder.LoadDatabase()
softioc.iocInit()

def getTemps():
    while True:
        url = urlOutput.get()
        soup = Weather.getSoup(url)
        maxTemp = Weather.getMaxT(soup)
        minTemp = Weather.getMinT(soup)
        location = Weather.getLoc(soup)
        logging.info('New max =%i', maxTemp)
        logging.info('Previous max=%i', maxTInput.get())
        logging.info('New min =%i', minTemp)
        logging.info('Previous min=%i', minTInput.get())
        logging.info(location) 
        maxTInput.set(maxTemp)
        minTInput.set(minTemp)
        locInput.set(location)  
        cothread.Sleep(10)



cothread.Spawn(getTemps)

cothread.WaitForQuit()