
from curses import beep
from os import PRIO_USER
from pickle import TRUE
import requests
from bs4 import BeautifulSoup
import pandas as pd



URL = "https://www.carpages.ca/used-cars/search/?num_results=50&fueltype_id%5B0%5D=3&fueltype_id%5B1%5D=7&p=1"
page = requests.get(URL)

web_link = "https://www.carpages.ca"
soup = BeautifulSoup(page.text,"lxml")

data = pd.DataFrame({"Link":[""],"Name":[""],"Price":[""],"Colour":[""]})



counter = 0
while counter <= 10:
    post = soup.find_all("div",class_="media soft push-none rule")

    for i in post:
        link = i.find("a",class_="media__img media__img--thumb").get("href")
        full_link=web_link + link
        #print(full_link)
        name = i.find("h4",class_="hN")
        #name=name.text
        name = name.text.strip()
        #price = i.find("div",class_="l-column l-column--medium-4 push-none")
        price = i.find("strong",class_="delta")
        price = price.text.strip()
        colour = i.find("span",class_="chip push-half--right")
        try:
            colour=colour.text.strip()
        except:
            colour="n/a"    

        data = data.append({"Link":link,"Name":name,"Price":price,"Colour":colour},ignore_index=TRUE)

    try:
        next_page = soup.find_all('a', class_ = 'nextprev')[1].get('href')
    except:
        next_page = soup.find('a', class_ = 'nextprev').get('href')

    
    #next_page = soup.find("a",class_="nextprev").get("href")
    print(next_page)
    full_page = web_link+next_page
    print(full_page)
    page = requests.get(full_page)
    soup=BeautifulSoup(page.text,"lxml")
    counter=counter + 1




data.to_csv("/Users/macbookpro/Desktop/ETL FLOW/cars.csv")
print("FileCreated")

#print(soup.find("a",class_="nextprev"))