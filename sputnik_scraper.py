import urllib.request
from bs4 import BeautifulSoup
import time
from time import sleep
import csv
from selenium import webdriver
import pandas as pd
import re


def parse_paragraphs(page_url):
    request = urllib.request.Request(page_url)
    html = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find('h1') and soup.find('div', attrs={'class': 'b-article__lead'}) and soup.find('div', attrs={'class': 'b-article__text'}):
        title = soup.find('h1').text
        paragraph_lead = soup.find(
            'div', attrs={'class': 'b-article__lead'}).text
        paragraphs = soup.find('div', attrs={'class': 'b-article__text'}).text
    # put the data in a dict
        post_data = {
            'title': title,
            'paragraphs': paragraph_lead + paragraphs
        }
        return post_data


url = "https://sputnik.kg/Kyrgyzstan"
driver = webdriver.Chrome('/home/aidin/Downloads/chromedriver')
driver.get(url)
driver.find_element_by_xpath('/html/body/div[6]/div[3]/a[2]').click()
driver.find_element_by_css_selector(
    ".b-more.main").click()  # to click load more button

n = 1000  # number of clicks
while n != 0:
    driver.find_element_by_css_selector(".b-more.main").click()
    time.sleep(2)
    n = n - 1

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
links = soup.find_all('a', href=True)
urls = []
extracted_data = []
for a_tag in links:
    url = a_tag['href']
    if not url.startswith('http'):
        url = "https://sputnik.kg"+url
    if url.startswith('https://sputnik.kg') and url.endswith('html') and not url.startswith('https://sputnik.kg/docs'):
        urls.append(url)
        time.sleep(2)


urls = list(set(urls))  # unique list of urls
for l in urls:
    print('Extracting data from %s' % l)
    extracted_data.append(parse_paragraphs(l))


data = []
for d in extracted_data:
    if type(d) == type(extracted_data[0]):
        data.append(d)
pd.DataFrame(data).to_csv('section_Kyrgyzstan.csv', index=False)


df = pd.read_csv(
    "/home/aidin/Documents/hackaton_12-15_03/scrapper/sputnik_kg/section_Kyrgyzstan.csv")

# Replace with "" english letters and numbers
df.paragraphs = [re.sub(r'[a-zA-Z0-9]', "", p) for p in df.paragraphs]
df.title = [re.sub(r'[a-zA-Z0-9]', "", p) for p in df.title]
df.paragraphs = [re.sub(r'[© / @ _ 🏋 🏻‍ ♀️ () Ⓜ > < -]', " ", p)
                 for p in df.paragraphs]
df.paragraphs = [re.sub(r'Фото', "", p) for p in df.paragraphs]
df.paragraphs = [re.sub(r'[ğ ö Ü ü ç ş ı 🙏 ✊ • ]', " ", p)
                 for p in df.paragraphs]
# matches any character that is not a word character, whitespace or comma."
df.paragraphs = [re.sub(r'[^\w\s,]', " ", p) for p in df.paragraphs]
df.paragraphs = [re.sub(r'Посмотреть эту публикацию в', "", p)
                 for p in df.paragraphs]
df.paragraphs = [re.sub(r'Публикация от', "", p) for p in df.paragraphs]
df.title = [re.sub(r'[© / ]', " ", p) for p in df.title]


df.to_csv('section_Kyrgyzstan_clean_2.csv', index=False)  # Convert to csv file

# To txt format
csv_file = '/home/aidin/Documents/hackaton_12-15_03/scrapper/sputnik_kg/section_Kyrgyzstan_clean_2.csv'
txt_file = '/home/aidin/Documents/hackaton_12-15_03/scrapper/sputnik_kg/section_Kyrgyzstan_clean_2.txt'
with open(txt_file, "w") as my_output_file:
    with open(csv_file, "r") as my_input_file:
        [my_output_file.write(" ".join(row)+'\n')
         for row in csv.reader(my_input_file)]
    my_output_file.close()
