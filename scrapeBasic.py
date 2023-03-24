import requests
from bs4 import BeautifulSoup

url = 'https://www.bbc.co.uk/weather/2647114'
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

#test0=soup.find_all(id="bbccom_interstitial_ad")
#print(test0)

test =soup.find(class_='wr-value--temperature--c')
print(test)
print(test.text)
maxTemp = test.text[:-1]
print(maxTemp)

test2 =soup.find_all(class_='wr-value--temperature--c')
print('First 2 find all results')
print(test2[0])
print(test2[1])

test3=soup.find(class_='wr-c-location__name')
print(test3.find("span").previous_sibling)
print(test3.text)


