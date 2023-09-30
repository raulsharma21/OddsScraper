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

def isOdd(s):
    parts = s.split('.')
    for part in parts:
        if not part.isnumeric():
            return False
    
    return True


def getActiveData(driver):
    data = []
    blocks = driver.find_elements(By.CLASS_NAME, "KambiBC-bet-offer__outcomes")
    for block in blocks:    
          
        text = block.text.splitlines()  
        
        if len(text) == 6:
            data.append(text)
        # else:
        #     print('rejected:')
        #     for line in text:
        #         print(line)

    return data
    




def acceptCookies(driver):
    allow_button = driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
    allow_button.click()
    

def initializeBrowser(driver):
    url = 'https://www.unibet.com/betting/sports/filter/all/all/all/all'
    driver.get(url)



def getUnibetFootball():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    s = Service('/usr/local/bin/chromedriver') 

    driver = webdriver.Chrome(service=s)
    driver.maximize_window()

    initializeBrowser(driver)
    
    try:
        acceptCookies(driver)
    except:
        print('no cookies')
        
    time.sleep(2)
    try:
        footballbutton = driver.find_element(By.CLASS_NAME, "KambiBC-navicon__sport-icon--football")
        footballbutton.click()
    except:
        viewport_height = driver.execute_script("return window.innerHeight")
        driver.execute_script(f"window.scrollBy(0, {viewport_height});")
        
        try:
            driver.implicitly_wait(15)
            footballbutton = driver.find_element(By.CLASS_NAME, "KambiBC-navicon__sport-icon--football")
            footballbutton.click()
        except:
            raise Exception("Football Button Not Found")

    time.sleep(3)

    headers = driver.find_elements(By.TAG_NAME, "header")



    click = False
    next = False
    for header in headers:
        
        # print(header.text)

        if(header.text.strip() == ''):
            click = False

        if(click):
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", header)

            header.click()
            time.sleep(.1)

            try:
                sibling_element = header.find_element(By.XPATH, "./following-sibling::*[1]")
                leagues = sibling_element.find_elements(By.TAG_NAME, 'header')
            
                for league in leagues:
                    try:
                        right_text = league.find_element(By.CLASS_NAME, 'CollapsibleContainer__RightText-sc-14bpk80-10')
                        league.click()
                    except Exception:
                        continue
            except:
                print('no siblings for')

        if(next):
            click = True

        if(header.text == 'League'):
            next = True

        


    data = getActiveData(driver)

    frame_data = []
    for row in data:
        team1 = row[0]
        home_odds = row[1]
        draw_odds = row[3]
        team2 = row[4]
        away_odds = row[5]
        frame_data.append([team1, team2, home_odds, draw_odds, away_odds])


    # for i in range(0, len(data)-1, 6):
    #     try:
    #         team1 = data[i]
    #         home_odds = data[i+1]
    #         draw_odds = data[i+3]
    #         team2 = data[i+4]
    #         away_odds = data[i+5]

    #         frame_data.append([team1, team2, home_odds, draw_odds, away_odds])
    #     except Exception:
    #         print('error storing data')
    #         print('last row')
    #         print(frame_data[len(frame_data)-1])


    columns = ["Team 1", "Team 2", "Home Odds", "Draw Odds", "Away Odds"]
    df = pd.DataFrame(frame_data, columns=columns)
    l1 = len(df)
    df = df.drop_duplicates()
    l2 = len(df)
    # print('dropped: ' + str(l1-l2))
    return(df)


# print(getUnibetFootball().to_string())



