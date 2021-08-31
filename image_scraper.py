'''
Given a GeoGuessr map URL take a number of screenshots each one step further down the road and rotated ~90 degrees.
You must have a chromedriver installed to use Selenium webdriver. This can be downloaded from: https://chromedriver.chromium.org/downloads
You must have a geonames account to use geopy for reverseGeolocation. You can make an account here: https://www.geonames.org/login
Then just fill in the fields below and run the script!
Note: When running the script would crash after 500-600 iterations. This was usually either due to GeoGuessr Bot detection or automatic sign outs.
'''
from selenium import webdriver
import time
import sys
import json
from bs4 import BeautifulSoup
import requests
from geopy.geocoders import GeoNames
import os
import pickle
from selenium.webdriver.chrome.options import Options

NUM_ROUNDS = 5
NUMBER_OF_SCREENSHOTS = 4


# geo_guessr_map = sys.argv[1]
#
# #log in with your Geoguessr user. Chrome must be closed!
# chrome_options = Options()
# chrome_options.add_argument("--user-data-dir=C:/Users/rohan/AppData/Local/Google/Chrome/User Data")
# driver = webdriver.Chrome('C:/Users/rohan/Downloads/chromedriver.exe', options=chrome_options)
# driver.get(geo_guessr_map)
#
# # let JS etc. load
# time.sleep(2)

def screenshot_canvas(header):
    '''
    Take a screenshot of the streetview canvas.
    '''
    if not os.path.exists(f'dataset/{header}'):
        os.makedirs(f'dataset/{header}')

    with open(f'dataset/{header}/canvas_{int(time.time())}.png', 'xb') as f:
        canvas = driver.find_element_by_tag_name('canvas')
        f.write(canvas.screenshot_as_png)


def rotate_canvas():
    '''
    Drag and click the <main> elem a few times to rotate us ~90 degrees.
    '''
    main = driver.find_element_by_tag_name('main')
    for _ in range(0, 5):
        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element(main)
        action.click_and_hold(main)
        action.move_by_offset(118, 0)
        action.release(main)
        action.perform()

def move_to_next_point():
    '''
    Click one of the next point arrows, doesn't matter which one
    as long as it's the same one for a session of Selenium.
    '''
    next_point = driver.find_element_by_css_selector('[fill="black"]')
    action = webdriver.common.action_chains.ActionChains(driver)
    action.click(next_point).perform()

def guess():
    map = driver.find_element_by_css_selector("#__next > div > main > div > div > div.game-layout__guess-map > div")
    action = webdriver.common.action_chains.ActionChains(driver)
    action.click(map).perform()
    button = driver.find_element_by_css_selector("#__next > div > main > div > div > div.game-layout__guess-map > div > div.guess-map__guess-button")
    action = webdriver.common.action_chains.ActionChains(driver)
    action.click(button).perform()
    time.sleep(2)
    button = driver.find_element_by_css_selector("#__next > div > main > div.result > div.result__bottom > div > div > div > div.card__content > div > div > section > section:nth-child(3) > button")
    action = webdriver.common.action_chains.ActionChains(driver)
    action.click(button).perform()
    time.sleep(2)

def url_to_map(latitude, longitude):
    geo = GeoNames(username='YOUR ARCGIS USERNAME') #https://www.geonames.org/login
    location = geo.reverse(query=(latitude, longitude), exactly_one=False, timeout=5)
    location_name = location[0]
    location_country = str(location_name).split(',')[-1].strip()
    return location_country

def register_country(geo_guessr_map):
    re = requests.get(geo_guessr_map)
    print(re)
    soup = BeautifulSoup(re.text, 'html.parser')
    element = soup.select("#__NEXT_DATA__")[0].text
    data = json.loads(element)
    rounds = data['props']['pageProps']['game']['rounds']
    current_round = rounds[len(rounds) - 1]
    lat = current_round['lat']
    lng = current_round['lng']
    country = url_to_map(lat, lng)
    print('true answer country: ', country)
    return country

num_iterations = 100
for i in range(num_iterations):
    print(i)
    geo_guessr_map = 'https://www.geoguessr.com/'

    # log in with your Geoguessr user. Chrome must be closed!
    chrome_options = Options()
    chrome_options.add_argument("YOUR CHROME OPTIONS DIRECTORY") #Typically --user-data-dir=C:/Users/XXXXXX/AppData/Local/Google/Chrome/User Data
    driver = webdriver.Chrome('PATH TO YOUR CHROMEDRIVER.EXE', options=chrome_options) #https://chromedriver.chromium.org/downloads
    driver.get(geo_guessr_map)

    # let JS etc. load
    time.sleep(2)
    #start world guessr
    world_button = driver.find_element_by_css_selector('#__next > div > main > div > div > div > section:nth-child(3) > section > section:nth-child(1) > article > div.map-teaser__body > div > button')
    action = webdriver.common.action_chains.ActionChains(driver)
    action.click(world_button).perform()
    time.sleep(2)
    #click play game
    play_game = driver.find_element_by_css_selector('#__next > div > main > div > div > div > div > div > div > article > div.game-settings__section.margin--top > button')
    action = webdriver.common.action_chains.ActionChains(driver)
    action.click(play_game).perform()
    time.sleep(2)

    for r in range(NUM_ROUNDS):
        header = register_country(driver.current_url)
        #for _ in range(0, NUMBER_OF_SCREENSHOTS):
        screenshot_canvas(header)
            #move_to_next_point()
            #rotate_canvas()
        guess()

    driver.close()
