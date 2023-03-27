import requests
from bs4 import BeautifulSoup
from softioc import softioc, builder
import cothread
from cothread.catools import *
import logging

class Weather:
    def __init__(self,url: str, file_path=False) -> None:
        """
        Initialiser of Weather class

        Parameters:
        url (str): BBC Weather URL to read data from or path to HTML file if file_path=True
        file_path (bool): True if reading from a file rather than a URL
        """
        if file_path:
            page = open(url)
            self.soup =BeautifulSoup(page.read(), "html.parser")
        else:
            page = requests.get(url)
            self.soup = BeautifulSoup(page.content, "html.parser")

    
    def setURL(self,url: str) -> None:
        """
        Sets URL and updates object's soup (BeautifulSoup) state

        Parameters:
        url (str): BBC Weather URL to read data from
        """
        page = requests.get(url)
        self.soup = BeautifulSoup(page.content, "html.parser")

    def getMaxT(self) -> int:
        """
        Returns today's forecast maximum temperature

        Returns:
        int: Today's forecast maximum temperature
        """
        tempLine = self.soup.find(class_='wr-value--temperature--c')  #Today's max is first instance
        maxTemp = int(tempLine.text[:-1])
        return maxTemp
    
    def getMinT(self) -> int:
        """
        Returns today's forecast minimum temperature

        Returns:
        int: Today's forecast minimum temperature
        """
        tempLine = self.soup.find_all(class_='wr-value--temperature--c')[1] #Today's min is second instance
        minTemp = int(tempLine.text[:-1])
        return minTemp
    
    def getLoc(self) -> str:
        """
        Returns location of forecast currently being read

        Returns:
        str: Location of Weather forecast being read
        """
        locLine=self.soup.find(class_='wr-c-location__name')
        location = locLine.find("span").previous_sibling #Gets just the location avoiding weather warning
        return location

#logging.basicConfig(level=logging.WARNING, force=True)

if __name__ == "__main__":

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

    def getTemps(weather:Weather):
        maxTemp = weather.getMaxT()
        minTemp = weather.getMinT()
        location = weather.getLoc()
        logging.info('New max =%i', maxTemp)
        logging.info('Previous max=%i', maxTInput.get())
        logging.info('New min =%i', minTemp)
        logging.info('Previous min=%i', minTInput.get())
        logging.info(location) 
        maxTInput.set(maxTemp)
        minTInput.set(minTemp)
        locInput.set(location)
        cothread.Sleep(10)


    def runTemps(): 
        url = urlOutput.get()
        weather = Weather(url)
        getTemps(weather)
        while True:
            url = urlOutput.get()
            weather.setURL(url)
            getTemps(weather)


    cothread.Spawn(runTemps)

    cothread.WaitForQuit()