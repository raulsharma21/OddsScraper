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





chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
s = Service('/usr/local/bin/chromedriver') 

driver = webdriver.Chrome(service=s)

def initializeBrowser():
    url = 'https://lvbet.com/sports/en/pre-matches'
    driver.get(url)


initializeBrowser()

time.sleep(3)


sidebar_buttons = driver.find_elements(By.CLASS_NAME, "sidebar-entry-heading__title")
for button in sidebar_buttons:
    if button.text == 'Football':
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        time.sleep(1)
        button.click() #clicks on Football

time.sleep(1.5)

leagues = driver.find_elements(By.CLASS_NAME, 'sidebar-list-entry__title')
for league in leagues:
    if league.text == 'Show all':
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", league)
        league.click() #clicks on Show all

time.sleep(1)



regions = driver.find_elements(By.CLASS_NAME, "sidebar-list-entry__title")
for region in regions:
        if region.text == 'Europe':
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region)
            region.click() #click on Europe for now, later scrape all the regions
            break


time.sleep(1)

leagues = driver.find_elements(By.CLASS_NAME, "checkbox-wrapp")
for league in leagues:
    print(league.text)

# select_button.click()

# # bold_elements = driver.find_elements(By.TAG_NAME, "strong")

# # for e in bold_elements:
# #     print(e.get_attribute('textContent'))

# html = driver.find_elements(By.CLASS_NAME, "text-sm")
# string_html = ""
# for e in html:
#     string_html += e.get_attribute('outerHTML')



# soup = BeautifulSoup(string_html, 'html.parser')

# teams_objects = soup.find_all(class_='pr-1')
# odds_objects = soup.find_all('strong')

# teams = []
# odds = []
# test = ''

# for team in teams_objects:
#     next_tag = team.find_next_sibling()
#     if next_tag and next_tag.name == 'i':
#         teams.pop()
#     else:    
#         teams.append(team.text.strip())

# for odd in odds_objects:
#     odds.append(odd.text.strip())

# data = []
# odds_counter = 0
# for i in range(0, len(teams), 2):
#     team1 = teams[i]
#     team2 = teams[i + 1]
#     home_odds = odds[odds_counter]
#     draw_odds = odds[odds_counter + 1]
#     away_odds = odds[odds_counter + 2]
    
#     data.append([team1, team2, home_odds, draw_odds, away_odds])
    
#     odds_counter += 3

# columns = ["Team 1", "Team 2", "Home Odds", "Draw Odds", "Away Odds"]
# df = pd.DataFrame(data, columns=columns)

# print(df)

