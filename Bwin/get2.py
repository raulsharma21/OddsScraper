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

def american_to_decimal(american_odds):
    american_odds = int(american_odds)
    if american_odds > 0:
        decimal_odds = (american_odds / 100) + 1
    elif american_odds < 0:
        decimal_odds = (100/-american_odds) + 1
    else:
        decimal_odds = 1
    return round(decimal_odds, 2)


def initializeBrowser(driver):
    url = 'https://sports.bwin.com/en/sports/football-4/today'
    driver.get(url)

def closePopup(driver):
    try:
        exit_button = driver.find_element(By.CLASS_NAME, 'theme-ex')
        exit_button.click()
    except Exception as e:
        try: 
            driver.quit()
            initializeBrowser(driver)
        except:           
            raise Exception('Exit button not clicked')
        

def displayEverything(driver):
    while True:
        try:
            footer = driver.find_element(By.CLASS_NAME, 'grid-footer')
            footer.click()
            # time.sleep(1)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", footer)

        except Exception as e:
            break
    
def getActiveData(driver, data):
    events = driver.find_elements(By.CLASS_NAME, 'grid-event-wrapper')

    for event in events:

        try:  
            teams = event.find_elements(By.CLASS_NAME, 'participant-container')
            team1 = teams[0].text.strip()
            team2 = teams[1].text.strip()

            odds = event.find_elements(By.CLASS_NAME, 'option-indicator')
            home_odds = american_to_decimal(odds[0].text.strip())
            draw_odds = american_to_decimal(odds[1].text.strip())
            away_odds = american_to_decimal(odds[2].text.strip())
            over_odds = american_to_decimal(odds[3].text.strip())
            under_odds = american_to_decimal(odds[4].text.strip())
            # home_odds = (odds[0].text.strip())
            # draw_odds = (odds[1].text.strip())
            # away_odds = (odds[2].text.strip())
            # over_odds = (odds[3].text.strip())
            # under_odds = (odds[4].text.strip())
            data.append([team1, team2, home_odds, draw_odds, away_odds, over_odds,under_odds])
        except:
            # print('exception:, row ignored')
            # print('previous')
            # print(data[len(data)-1])
            # print('current:')
            # print(event.text)
            continue



def getBwinFootball():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    s = Service('/usr/local/bin/chromedriver') 

    driver = webdriver.Chrome(service=s)

    initializeBrowser(driver)

    time.sleep(8)
    
    closePopup(driver)
    time.sleep(3)

    # get today's games
    displayEverything(driver)
    data = []
    getActiveData(driver, data)



    #switch to tomorrow
    menu_bar = driver.find_elements(By.CLASS_NAME, 'scroll-adapter__container')
    buttons = menu_bar[1].find_elements(By.TAG_NAME, 'ms-item')

    for button in buttons:
        if 'Tomorrow' in button.text:
            button.click()

    time.sleep(5)
        
    displayEverything(driver)   
    getActiveData(driver, data) 

    columns = ["Team 1", "Team 2", "Home Odds", "Draw Odds", "Away Odds", "Over", "Under"]
    df = pd.DataFrame(data, columns=columns)
    return (df)




# print(getBwinFootball().to_string())