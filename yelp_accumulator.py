# https://pypi.org/project/selenium/
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

# https://pypi.org/project/webdriver-manager/
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--log-level=3")
options.add_argument("--start-maximized")
# options.add_argument('--headless')

chrome_prefs = {}
options.experimental_options["prefs"] = chrome_prefs    
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(7)

query = 'https://www.yelp.com/search?find_desc=Restaurants&find_loc=Philadelphia%2C+PA&l=g%3A-75.22235870361328%2C39.91421300128754%2C-75.12004852294922%2C39.993166618114195&sortby=recommended'
driver.get(query)
print(driver.find_element(By.XPATH, '//h2[2]').text)

# while True:
#     try:
#         print(driver.find_element(By.XPATH, '//h2[2]').text)
#     except:
#         break