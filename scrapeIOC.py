import requests
from bs4 import BeautifulSoup
from softioc import softioc, builder
import cothread
from cothread.catools import *
import logging

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
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        allTempLines = soup.find_all(class_='wr-value--temperature--c')
        maxTemp = int(allTempLines[0].text[:-1]) #Today's max is first instance
        minTemp = int(allTempLines[1].text[:-1]) #Today's min is second
        locLine=soup.find(class_='wr-c-location__name')
        location = locLine.find("span").previous_sibling #Gets just the location avoiding weather warning
        logging.info('New max =%i', maxTemp)
        logging.info('Previous max=%i', maxTInput.get())
        logging.info('New min =%i', minTemp)
        logging.info('Previous min=%i', minTInput.get())
        logging.info(location) 
        maxTInput.set(maxTemp)
        minTInput.set(minTemp)
        locInput.set(location)  
        cothread.Sleep(10)

def getLoc():
    while True:
        url = urlOutput.get()
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        locLine=soup.find(class_='wr-c-location__name')
        location = locLine.find("span").previous_sibling #Gets just the location avoiding weather warning
        logging.info(location) 
        locInput.set(location)
        cothread.Sleep(10)

def getLoc2(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    locLine=soup.find(class_='wr-c-location__name')
    location = locLine.find("span").previous_sibling #Gets just the location avoiding weather warning
    logging.info(location) 
    locInput.set(location)    


cothread.Spawn(getTemps)
#cothread.Spawn(getLoc)
#camonitor('bryn:url',getLoc2)

cothread.WaitForQuit()