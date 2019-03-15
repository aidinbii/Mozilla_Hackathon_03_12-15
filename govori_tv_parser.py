import json
import requests
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import glob
import os, shutil
from bs4 import BeautifulSoup
import requests


def get_youtube_links():
    #api_key = 'Your api key'
    playlist_id = 'PLrdGbobR_mSjN0wVH9Y7zD41OV_09Nk6t'
    url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={0}&key={1}'.format(playlist_id, api_key)


    content = requests.get(url).json()

    items = content['items']


    links = []
    for item in items:
        id_link = item['snippet']['resourceId']['videoId']
        links.append(['https://www.youtube.com/watch?v='+id_link])


    with open('govori_tv_links/playlist_one.csv', 'w', newline='') as wfile:
        s_wfile = csv.writer(wfile)
        s_wfile.writerows(links)


def get_youtube_mp3(link, driver):
    #link = 'https://www.youtube.com/watch?v=grpwtK1xfnE'

    driver.get("https://ytmp3.cc/")

    input_elem = driver.find_element_by_xpath('//*[@id="input"]')
    input_elem.clear()
    input_elem.send_keys(link)
    input_elem.send_keys(Keys.RETURN)
    time.sleep(5)

    driver.find_element_by_xpath('//*[@id="download"]').click()
    time.sleep(2)


def wait_for_element_and_click(driver, xpath, timeout, keys_to_send):
    try:
        element_present = EC.visibility_of_element_located((By.XPATH, xpath))
        click_object = WebDriverWait(driver, timeout).until(element_present)
        click_object.click()
        if keys_to_send != 'None':
            click_object.send_keys(keys_to_send)
            click_object.send_keys(Keys.RETURN)
        return click_object
    except ElementClickInterceptedException:
        if keys_to_send != 'None':
            wait_for_element_and_click(driver, xpath, timeout, keys_to_send)
        else:
            wait_for_element_and_click(driver, xpath, timeout, keys_to_send)


def entire():
    links = []
    with open('govori_tv_links/custom.csv') as rfile:
        s_rfile = csv.reader(rfile)
        for r in s_rfile:
            links.append(r[0])

    count = 0
    fp = webdriver.FirefoxProfile('path to profile')
    driver = webdriver.Firefox(firefox_profile=fp, executable_path='path to geckodriver')

    for link in links:

        driver.get("https://ytmp3.cc/")

        input_elem = driver.find_element_by_xpath('//*[@id="input"]')
        input_elem.clear()
        input_elem.send_keys(link)
        input_elem.send_keys(Keys.RETURN)
        time.sleep(5)
        wait_for_element_and_click(driver, '//*[@id="download"]', 500, 'None')
        time.sleep(2)
        count += 1
        print(count)

