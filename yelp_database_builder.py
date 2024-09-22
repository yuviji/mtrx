# https://pypi.org/project/selenium/
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

# https://pypi.org/project/webdriver-manager/
from webdriver_manager.chrome import ChromeDriverManager

import string
import time
import json

cleaned_string = lambda s: ''.join(filter(lambda x: x in set(string.printable), s))

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

to_scrape = [
    # 'https://www.yelp.com/biz/reading-terminal-market-philadelphia',
    # 'https://www.yelp.com/biz/pats-king-of-steaks-philadelphia-5',
    # 'https://www.yelp.com/biz/el-vez-philadelphia',
    # 'https://www.yelp.com/biz/genos-steaks-philadelphia',
    # 'https://www.yelp.com/biz/zahav-philadelphia',
    # 'https://www.yelp.com/biz/parc-philadelphia-2',
    # 'https://www.yelp.com/biz/barbuzzo-philadelphia',
    # 'https://www.yelp.com/biz/dim-sum-garden-philadelphia',
    # 'https://www.yelp.com/biz/green-eggs-caf%C3%A9-philadelphia-7',
    # 'https://www.yelp.com/biz/the-dandelion-philadelphia',
    # 'https://www.yelp.com/biz/jims-south-st-philadelphia',
    # 'https://www.yelp.com/biz/nan-zhou-hand-drawn-noodle-house-philadelphia',
    # 'https://www.yelp.com/biz/tommy-dinics-philadelphia',
    # 'https://www.yelp.com/biz/monks-cafe-philadelphia-4',
    # 'https://www.yelp.com/biz/amada-philadelphia',
    # 'https://www.yelp.com/biz/talulas-garden-philadelphia',
    # 'https://www.yelp.com/biz/sampan-philadelphia-3',
    # 'https://www.yelp.com/biz/morimoto-philadelphia',
    # 'https://www.yelp.com/biz/sabrinas-cafe-art-museum-philadelphia-3',
    # 'https://www.yelp.com/biz/sonnys-famous-steaks-philadelphia',
    # 'https://www.yelp.com/biz/terakawa-ramen-philadelphia',
    # 'https://www.yelp.com/biz/the-continental-mid-town-philadelphia',
    # 'https://www.yelp.com/biz/johns-roast-pork-philadelphia',
    # 'https://www.yelp.com/biz/cafe-la-maude-philadelphia',
    # 'https://www.yelp.com/biz/buddakan-philadelphia',
    # 'https://www.yelp.com/biz/cleavers-philadelphia',
    # 'https://www.yelp.com/biz/village-whiskey-philadelphia',
    # 'https://www.yelp.com/biz/fogo-de-chao-philadelphia-8',
    # 'https://www.yelp.com/biz/oyster-house-philadelphia',
    # 'https://www.yelp.com/biz/vedge-philadelphia',
    # 'https://www.yelp.com/biz/white-dog-cafe-philadelphia-2',
    # 'https://www.yelp.com/biz/suraya-philadelphia-2',
    # 'https://www.yelp.com/biz/han-dynasty-philadelphia',
    # 'https://www.yelp.com/biz/chubby-cattle-shabu-philadelphia-2',
    # 'https://www.yelp.com/biz/gran-caffe-l-aquila-philadelphia',
    # 'https://www.yelp.com/biz/butcher-and-singer-philadelphia',
    # 'https://www.yelp.com/biz/honeys-sit-n-eat-philadelphia',
    # 'https://www.yelp.com/biz/bud-and-marilyns-philadelphia',
    # 'https://www.yelp.com/biz/double-knot-philadelphia',
    # 'https://www.yelp.com/biz/good-dog-bar-philadelphia',
    # 'https://www.yelp.com/biz/little-nonnas-philadelphia',
    # 'https://www.yelp.com/biz/cuba-libre-restaurant-and-rum-bar-philadelphia-philadelphia',
    # 'https://www.yelp.com/biz/mixto-restaurant-philadelphia-2',
    # 'https://www.yelp.com/biz/cafe-lift-philadelphia',
    # 'https://www.yelp.com/biz/del-friscos-double-eagle-steakhouse-philadelphia',
    # 'https://www.yelp.com/biz/devon-seafood-grill-philadelphia-3',
    # 'https://www.yelp.com/biz/nine-ting-philadelphia',
    # 'https://www.yelp.com/biz/penang-philadelphia-4',
    # 'https://www.yelp.com/biz/charlie-was-a-sinner-philadelphia',
    # 'https://www.yelp.com/biz/harp-and-crown-philadelphia',
    # 'https://www.yelp.com/biz/lukes-lobster-rittenhouse-philadelphia',
    # 'https://www.yelp.com/biz/fat-salmon-philadelphia',
    # 'https://www.yelp.com/biz/giorgio-on-pine-philadelphia-3',  
    # 'https://www.yelp.com/biz/hipcityveg-philadelphia',
    # 'https://www.yelp.com/biz/bleu-sushi-philadelphia-5',
    # 'https://www.yelp.com/biz/el-camino-real-philadelphia',
    # 'https://www.yelp.com/biz/vernick-food-and-drink-philadelphia',
    # 'https://www.yelp.com/biz/sang-kee-peking-duck-house-philadelphia-2',
    # 'https://www.yelp.com/biz/moshulu-philadelphia-4',
    # 'https://www.yelp.com/biz/the-love-philadelphia-2',
    # 'https://www.yelp.com/biz/el-rey-philadelphia',
    # 'https://www.yelp.com/biz/osteria-philadelphia-2',
    # 'https://www.yelp.com/biz/dan-dan-philadelphia-6',
    # 'https://www.yelp.com/biz/frankford-hall-philadelphia',
    # 'https://www.yelp.com/biz/silk-city-diner-and-lounge-philadelphia',
    # 'https://www.yelp.com/biz/sabrinas-caf%C3%A9-university-city-philadelphia-2',
    # 'https://www.yelp.com/biz/yards-brewing-company-philadelphia-3',
    # 'https://www.yelp.com/biz/national-mechanics-philadelphia', 
    # 'https://www.yelp.com/biz/cantina-dos-segundos-philadelphia', 
    # 'https://www.yelp.com/biz/pod-philadelphia-4',
    # 'https://www.yelp.com/biz/cantina-los-caballitos-philadelphia',
    # 'https://www.yelp.com/biz/elixr-coffee-roasters-philadelphia-3',
    # 'https://www.yelp.com/biz/tria-cafe-rittenhouse-philadelphia-2',
    # 'https://www.yelp.com/biz/vic-sushi-bar-philadelphia',
    # 'https://www.yelp.com/biz/barclay-prime-philadelphia',
    # 'https://www.yelp.com/biz/khyber-pass-pub-philadelphia',
    # 'https://www.yelp.com/biz/dutch-eating-place-philadelphia',
    # 'https://www.yelp.com/biz/angelos-pizzeria-philadelphia',
    # 'https://www.yelp.com/biz/garces-trading-company-philadephia',
    # 'https://www.yelp.com/biz/green-eggs-cafe-philadelphia-9',
    # 'https://www.yelp.com/biz/estia-philadelphia',
    # 'https://www.yelp.com/biz/oh-brother-philly-philadelphia',
    # 'https://www.yelp.com/biz/han-dynasty-philadelphia-11',
    # 'https://www.yelp.com/biz/campos-philly-cheesesteaks-philadelphia',
    # 'https://www.yelp.com/biz/high-street-philadelphia-philadelphia',
    # 'https://www.yelp.com/biz/spice-28-philadelphia',
    # 'https://www.yelp.com/biz/hershels-east-side-deli-philadelphia',
    # 'https://www.yelp.com/biz/front-street-cafe-philadelphia',
    # 'https://www.yelp.com/biz/ishkabibbles-philadelphia',
    # 'https://www.yelp.com/biz/devils-alley-bar-and-grille-philadelphia',
    # 'https://www.yelp.com/biz/pietros-coal-oven-pizzeria-philadelphia-2',
    # 'https://www.yelp.com/biz/positano-coast-by-aldo-lamberti-philadelphia',
    # 'https://www.yelp.com/biz/bar-bomb%C3%B3n-philadelphia-4',
    # 'https://www.yelp.com/biz/brauhaus-schmitz-philadelphia',
    # 'https://www.yelp.com/biz/standard-tap-philadelphia',
    # 'https://www.yelp.com/biz/barcelona-wine-bar-passyunk-philadelphia',
    # 'https://www.yelp.com/biz/ralphs-italian-restaurant-philadelphia',
    # 'https://www.yelp.com/biz/yakitori-boy-philadelphia',
    # 'https://www.yelp.com/biz/dizengoff-philadelphia',
    # 'https://www.yelp.com/biz/marrakesh-philadelphia-2'
]

for business_link in to_scrape:
    driver.get(business_link + '?sort_by=date_desc')

    try:
        business_name = driver.find_element(By.TAG_NAME, 'h1').text
    except:
        business_name = None

    try:
        business_address = driver.find_element(By.XPATH, '//a[text()="Get Directions"]/parent::p/following-sibling::p').text
    except:
        business_address = None

    try:
        business_cost = driver.find_element(By.XPATH, '//h1/parent::div/parent::div/span/span[contains(text(), "$")]').text.strip()
    except:
        business_cost = None

    try:
        business_rating = float(cleaned_string(driver.find_element(By.XPATH, '//a[@href="#reviews"]/parent::span/preceding-sibling::span').text))
    except:
        business_rating = None

    try:
        business_tags = driver.find_element(By.XPATH, '//h1/parent::div/parent::div/span[last()]').text.strip().split(', ')
    except:
        business_tags = None

    try:
        driver.find_element(By.XPATH, '//span[text()="Read more"]').click()
        business_description = driver.find_element(By.XPATH, '//h2[text()="From the business"]/parent::div/following-sibling::div/div/div/div/div/div[1]').text.strip().replace('\n', '')
        driver.find_element(By.XPATH, "//span[text()='Close']").click()
    except:
        business_description = None

    business_reviews = []
    try:
        while True:
            num_pages = tuple(map(int, driver.find_element(By.XPATH, '//div[@aria-label="Pagination navigation"]/div[2]').text.split(' of ')))
            reviews = driver.find_elements(By.XPATH, '//*[@id="reviews"]/section/div[2]/ul/li')[:-1]  # last one is navbar
            print(f'Pg. {num_pages[0]} of {num_pages[1]}: {len(business_reviews)} + {len(reviews)} reviews')
            
            for review in reviews:
                review_data = {}
                
                review_data['reviewer_id'] = cleaned_string(review.find_element(By.TAG_NAME, 'a').get_attribute('href').split('=')[-1])
                review_data['review_date'] = cleaned_string(review.find_element(By.XPATH, 'div/div[2]/div/div[2]/span').text)
                review_data['review_rating'] = float(cleaned_string(review.find_element(By.XPATH, 'div/div[2]/div/div/span/div').get_attribute('aria-label').split(' ')[0]))
                review_data['review_content'] = cleaned_string(review.find_element(By.XPATH, 'div/div/p').text)

                driver.implicitly_wait(0)
                try:
                    review_data['elite'] = len(review.find_elements(By.XPATH, 'div/div//a[@href="/elite"]')) == True
                except:
                    review_data['elite'] = False
                driver.implicitly_wait(7)

                business_reviews.append(review_data)
            
            print(f'Completed Pg. {num_pages[0]} of {num_pages[1]}: {len(business_reviews)}')

            if num_pages[0] == num_pages[1]:    # scraped all pages for business
                break
            elif num_pages[0] == 50:
                break
            else:
                driver.find_element(By.XPATH, '//div[@aria-label="Pagination navigation"]/div[1]//a[@aria-label="Next"]/parent::span').click()
        
                # keep trying to go to next page if still on the page
                current_page = int(driver.find_element(By.XPATH, '//div[@aria-label="Pagination navigation"]/div[2]').text.split(' of ')[0])
                while num_pages[0] == current_page:
                    print(f'Retrying navigation from Pg. {current_page} to {num_pages[1]}')
                    driver.find_element(By.XPATH, '//div[@aria-label="Pagination navigation"]/div[1]//a[@aria-label="Next"]/parent::span').click()            
                    current_page = int(driver.find_element(By.XPATH, '//div[@aria-label="Pagination navigation"]/div[2]').text.split(' of ')[0])
    except:
        pass

    business_info = {
        'business_name': business_name,
        'business_rating': business_rating,
        'business_address': business_address,
        'business_cost': business_cost,
        'business_tags': business_tags,
        'business_description': business_description,
        'business_reviews': business_reviews
        }

    print(f'Business: {business_name}')
    print(f'Rating: {business_rating}')
    print(f'Address: {business_address}')
    print(f'Cost: {business_cost}')
    print(f'Tags: {business_tags}')
    print(f'Description: {business_description}')
    print(f'Reviews: {len(business_reviews)}')

    print('\n----------------------------------------------------------------\n')

    try:
        with open('business_data_dated.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(business_info)

    with open('business_data_dated.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)