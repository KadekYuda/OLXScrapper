from datetime import datetime
import requests
import csv
import time

from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

base_url = "https://www.olx.co.id/mobil-bekas_c198"
car_url_prefix = "https://www.olx.co.id"
MUAT_LAINNYA_XPATH = "/html/body/div/div/main/div/section/div/div/div[5]/div[2]/div[1]/div[3]/button"

def crawlCarData(car_url):
    response = requests.get(car_url)
    page = soup(response.text, 'html.parser')
    value_tag = page.find_all(class_="_2vNpt")
    value_list = []
    for value in value_tag:
        value_list.append(value.contents[0])
    price = page.find(class_='_2xKfz')
    if price:
        value_list.append(int(page.find(class_='_2xKfz').contents[0].replace('.','').replace('Rp', '')))
    return value_list

def writeCSV(data, filename = 'test.csv'):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)
    csvfile.close()

def crawlWebsite():
    print('[ INFO ] ' + 'Crawling from ' + base_url)
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    driver.get(base_url)
    more_button = driver.find_elements_by_xpath(MUAT_LAINNYA_XPATH)
    btn_counter = 0
    while (len(more_button) > 0):
        more_button[0].click()
        btn_counter += 1
        print('[ INFO ] Clicked MUAT LAINNYA! Number of clicks: ' +  str(btn_counter))
        time.sleep(2)
        more_button = driver.find_elements_by_xpath(MUAT_LAINNYA_XPATH)
    print('[ INFO ] No more MUAT LAINNYA button. Oh boy time to parse!')
    page = soup(driver.page_source, 'html.parser')
    car_tags = page.find_all(class_='EIR5N')
    car_data = []
    print('[ INFO ] Total link: ' + str(len(car_tags)))
    for cars in car_tags:
        car_link = cars.find('a', href=True)
        car_url = car_url_prefix + car_link['href']
        value_list = crawlCarData(car_url)
        car_data.append(value_list)
        percentage = str(int((len(car_data) / len(car_tags))*100)).rjust(3)
        print('[ ' + percentage + '% ] ' + 'Crawled from ' + car_url)
        time.sleep(2)
    driver.close()
    print('[ INFO ] Crawling finished. Total data crawled: ' + str(len(car_data)))
    return car_data

data = crawlWebsite()
now = datetime.today()
filename = str(now.year) + str(now.month) + str(now.day) + "-" + str(int(now.timestamp())) + '_carlist.csv'
writeCSV(data,filename=filename)
print('[ INFO ] Crawled data saved to ' + filename)