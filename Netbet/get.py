from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup

import pandas as pd


import time

def initializeBrowser(driver):
    url = 'https://sport.netbet.com/football/'
    driver.get(url)

def getActiveData(data, driver):
    rows = driver.find_elements(By.CSS_SELECTOR, "div[class='flex flex-row w-full']")
    for row in rows:
            try:
                teams = row.find_elements(By.CSS_SELECTOR, "span[class='text-sm truncate pr-1 font-medium']")
                team1 = teams[0].text.strip()
                team2 = teams[1].text.strip()
                odds = row.find_elements(By.TAG_NAME, 'strong')
                home_odds = odds[0].text.strip()
                draw_odds = odds[1].text.strip()
                away_odds = odds[2].text.strip()
                data.append([team1, team2, home_odds, draw_odds, away_odds])
                obtained += 1
            except:
                 continue


def getNetbetFootball():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    s = Service('/usr/local/bin/chromedriver') 

    driver = webdriver.Chrome(service=s)

    initializeBrowser(driver)

    time.sleep(4)

    firstbutton = driver.find_element(By.TAG_NAME, "button")
    firstbutton.click()

    time.sleep(6)

    data = []
    


# <div data-v-20d1825c="" data-v-45080727="" class="w-24 text-xs text-center py-2 relative h-full cursor-pointer"><p data-v-20d1825c="" data-v-45080727="">Wednesday</p> <p data-v-20d1825c="" data-v-45080727="" class="font-bold">September 27</p> <div data-v-20d1825c="" data-v-45080727="" class="absolute bottom-0 left-0 w-full" style="bottom: -11px;"><i data-v-20d1825c="" data-v-45080727="" class="fas fa-caret-up text-xl text-gray-700"></i></div></div>
    days = driver.find_elements(By.CSS_SELECTOR, "div[class='w-24 text-xs text-center py-2 relative h-full cursor-pointer']")
    for i in range(3):
        days[i].click()
        time.sleep(3)
        getActiveData(data, driver)

    

    columns = ["Team 1", "Team 2", "Home Odds", "Draw Odds", "Away Odds"]
    df = pd.DataFrame(data, columns=columns)

    return(df)

# print(getNetbetFootball().to_string())