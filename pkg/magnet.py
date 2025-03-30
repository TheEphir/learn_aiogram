import datetime
import requests
import re
from bs4 import BeautifulSoup

def check_date(soup: BeautifulSoup) -> bool:
    soup_date = str(soup.find("div", class_="meta__date").text).split()
    today = datetime.datetime.today().day
    return soup_date[0] == str(today)
    
def get_k_index() -> str: 
    try:
        url = "https://api.meteoagent.com/widgets/v1/kindex"
        site = requests.get(url=url).text
        soup = BeautifulSoup(site, features="html.parser")
        today_info = soup.find("div", class_="forecast__meta")
        
        if check_date(today_info):
            k_index = today_info.find("strong").text
            return k_index
    except:
        return "Can't check k-index"