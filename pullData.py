from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
import requests
from heroList import herolist, hero_id
import json

def pullheros():
    url = 'https://api.opendota.com/api/heroes'
    response = requests.get(url)
    print(response)
    response.raise_for_status()
    heroes = response.json()
    formatted = {}
    for hDict in heroes:
        formatted[hDict['localized_name'].lower()] = hDict['id']
    print(formatted)
    


def pullHeroData(hero):
    hero = hero.lower()
    if hero in herolist:
        hId = hero_id[hero] 
        url = f"https://api.opendota.com/api/heroes/{hId}/matchups"
        response = requests.get(url)
        response.raise_for_status()
        matchups = response.json()
        return matchups

