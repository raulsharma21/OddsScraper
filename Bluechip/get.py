from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup

import time

def extract_div_content(html_code):
    # Parse the HTML code using Beautiful Soup
    soup = BeautifulSoup(html_code, 'html.parser')

    div_elements = soup.find_all('div', class_='bt253')

    contents = []
    for div_element in div_elements:
        # Extract content from each div
        content = div_element.get_text().strip()
        contents.append(content)

    return contents





chrome_options = Options()
chrome_options.add_argument("--disable-gpu")


s = Service('/usr/local/bin/chromedriver') 

driver = webdriver.Chrome(service=s)

def initializeBrowser(extension):
    url = 'https://www.bluechip.io/in-en/sport?bt-path=%2Fsoccer-' + str(extension)
    driver.get(url)


initializeBrowser(1)

time.sleep(5)

result = driver.execute_script('''return document.querySelector("#bt-inner-page").shadowRoot.querySelector("div")''')

innerHTML = result.get_attribute("innerHTML")

#print(innerHTML)
# print(extract_div_content(innerHTML))


soup = BeautifulSoup(innerHTML, 'html.parser')

div_elements = soup.find_all('div', class_='bt255')


print("Div Elements:")
for div_element in div_elements:
    print(div_element)