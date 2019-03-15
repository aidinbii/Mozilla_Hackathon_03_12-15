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
import re


def get_links_april():
    start_time = time.time()

    driver = webdriver.Firefox(executable_path='/home/daniiar_abdiev/Desktop/Mozilla_thing/geckodriver')

    driver.get("https://april.kg/ky")

    count = 0
    for page_number in range(1, 126):
        driver.get("https://april.kg/?page={0}".format(page_number))

        content = driver.page_source

        soup = BeautifulSoup(content, 'html.parser')

        div_content = soup.find('div',{'class':'content'})

        blocks = div_content.find_all('div', {'class':'col-12 col-md-10 news'})

        links = []
        for block in blocks:
            a = block.find('a')['href']
            link = 'https://april.kg/' + str(a)
            links.append([link])

        with open('april_links_files/april_{0}.csv'.format(page_number), 'w', encoding='utf-8', newline='') as wfile:
            s_wfile = csv.writer(wfile)
            s_wfile.writerows(links)

        count += 1
        if count % 10 == 0:
            print(count)


def get_link(link):
    # link = 'https://april.kg/ky/article/ayikpas-dartka-kabilgan-murat-sutalinov-kamaktan-boshotulabi'

    content = requests.get(link).content

    soup = BeautifulSoup(content, 'html.parser')

    h = soup.find('h1').text
    ps = soup.find('div', {'class':'col-sm-12 article'}).find_all('p')

    all_text = []
    for p in ps:
        text = p.text
        all_text.append(text)

    words = ''.join(all_text)

    with open('words_not_cleaned/{0}.txt'.format(link.split('/')[-1]), 'w', encoding='utf-8') as wfile:
        wfile.write(h+'\n'+words)


def get_all_the_articles():
    folder_links = 'april_links_files/'

    count = 0
    for file in os.listdir(folder_links):
        with open(folder_links+file, 'r') as rfile:
            s_rfile = csv.reader(rfile)
            for link in s_rfile:
                get_link(link[0])
        count += 1
        print(count)


def cleaning():
    p = 'words_not_cleaned'
    c = 0
    for file in os.listdir(p):
        f = open('words_not_cleaned/'+file, encoding='utf-8')
        r = f.read()
        #a = "".join((char if char.isalpha() else " ") for char in r).split()

        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', r)
        
        clean_sentences = []
        for sentence in sentences:
            clean_sentences.append([sentence.replace('\n', '')])
        f.close()
        
        with open('words_cleaned/{0}.txt'.format(file), 'w', newline='', encoding='utf-8') as wfile:
            s_wfile = csv.writer(wfile, delimiter='|')
            s_wfile.writerows(clean_sentences)
        c += 1
        if c % 10==0:
            print(c)

