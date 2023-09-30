
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
    url = 'https://sports.bwin.com/en/sports/football-4/today'
    driver.get(url)

def getBwinFootball():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    s = Service('/usr/local/bin/chromedriver') 

    driver = webdriver.Chrome(service=s)

    initializeBrowser(driver)

    time.sleep(8)
    
    exit_button = driver.find_element(By.CLASS_NAME, 'theme-ex')
    try:
        exit_button.click()
    except Exception as e:
        print('exit button not clicked')

    time.sleep(3)
    teams = driver.find_elements(By.CLASS_NAME, "participants-pair-game")
    last_element = teams[len(teams)-1]
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", last_element)


    while True:
        try:
            footer = driver.find_element(By.CLASS_NAME, 'grid-footer')
            footer.click()
            # time.sleep(1)
            teams = driver.find_elements(By.CLASS_NAME, "participants-pair-game")
            # last_element = teams[len(teams)-1]
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", footer)


        except Exception as e:
            break

    odds = driver.find_elements(By.CLASS_NAME, 'option-indicator')
    # odds_container = driver.find_elements(By.CLASS_NAME, 'grid-group-container')
    odds_data = []
    for odd in odds:
        
        try:
            if odd.find_elements(By.TAG_NAME, 'i'):
                odds_data.append('N/A')
            else:
                odds_data.append(odd.text.strip())
        except Exception:
            print('exception')
            odds_data.append('N/A')
                  

    data = []
    odds_counter = 0
    for game in teams:
        temp = game.text.splitlines()
        team1 = temp[0].strip()
        team2 = temp[1].strip()
        home_odds = odds_data[odds_counter]
        draw_odds = odds_data[odds_counter+1]
        away_odds = odds_data[odds_counter+2]
        over_odds = odds_data[odds_counter+3]
        under_odds = odds_data[odds_counter+4]
        data.append([team1, team2, home_odds, draw_odds, away_odds, over_odds,under_odds])
        # data.append([team1, team2, home_odds, draw_odds, away_odds])
        odds_counter += 5

    columns = ["Team 1", "Team 2", "Home Odds", "Draw Odds", "Away Odds", "Over", "Under"]
    df = pd.DataFrame(data, columns=columns)
    return (df)
    

print(getBwinFootball().to_string())