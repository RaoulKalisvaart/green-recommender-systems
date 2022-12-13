from bs4 import BeautifulSoup
from requests import get
import re
import pandas as pd
import time

def scraper(ingredient):
    length =  len(ingredient.split())
    html_doc = "Not found"
    if(length == 1):
        html_doc, url = generateUrl1(ingredient)
    if(length == 2):
        html_doc, url = generateUrl2(ingredient)
    if(length > 2):
        html_doc, url = generateUrl3(ingredient)

    print(html_doc)

    if(html_doc == "Not found"):
        return "Not found", url
    return scrape_doc(html_doc, url)

def scrape_doc(html_doc, url):
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    print(soup)
    CO2_text = soup(text=re.compile('CO2e'))
    if(len(CO2_text) == 0):
        return -1, url

    carbon = re.search("\d+\.\d+", CO2_text[0])
    if(carbon):
        carbon = carbon.group()
    else:
        return -1, url
    print(carbon)
    return carbon, url

def generateUrl1(ingredient):
    firstLetter = ingredient[0]
    url = "https://healabel.com/"+ firstLetter + "-ingredients/" + ingredient
    print(url)
    html_doc = get(url, headers = {'User-agent': 'your bot 0.1'})

    if(html_doc.status_code == 404):
        change = changeUrl1_1(url)
        print(change)
        return change
    return html_doc, url

def changeUrl1_1(url):
    url = url+"s"
    print(url)
    html_doc = get(url, headers = {'User-agent': 'your bot 0.1'})
    if(html_doc.status_code == 404):
        return "Not found", url
    return html_doc, url

def generateUrl2(ingredient):
    firstLetter = ingredient[0]
    words = ingredient.split()
    url = "https://healabel.com/"+ firstLetter + "-ingredients/" + words[0] + "-" + words[1]
    print(url)
    html_doc = get(url, headers = {'User-agent': 'your bot 0.1'})

    if(html_doc.status_code == 404):
        return generateUrl3(ingredient)
    return html_doc, url

def generateUrl3(ingredient):
    words = ingredient.split()
    ingredient = words[len(words)-1]
    firstLetter = ingredient[0]
    url = "https://healabel.com/"+ firstLetter + "-ingredients/" + ingredient
    print(url)
    html_doc = get(url, headers = {'User-agent': 'your bot 0.1'})

    if(html_doc.status_code == 404):
        return changeUrl1_1(url)
    return html_doc, url


df = pd.read_csv("ingredient_scraping_subset.csv")

count = 0

for index, row in df.iterrows():
    if(count > 100):
        df.to_csv("scraped_ingredients4.csv")
        count = 0
    count = count + 1
    ingr = row['ingr_name']
    sc = scraper(ingr)
    carbon, url = sc
    if(carbon == 'Not found' or carbon == -1):
        carbon = -1
        url = 'Not found'
    df.at[index, 'CO2'] = carbon
    df.at[index, 'url'] = url

df.to_csv("scraped_ingredients4.csv")

