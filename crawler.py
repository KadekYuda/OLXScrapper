import datetime
import requests
import csv
import time

from bs4 import BeautifulSoup as soup
from pprint import pprint

base_url = "https://www.olx.co.id"
page_base_url = "https://www.olx.co.id/mobil-bekas_c198?page="

def crawlCarData(car_url):
    print('[ INFO ] ' + 'Crawling from ' + car_url)
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

def crawlPage(page_url):
    print('[ INFO ] ' + 'Crawling from ' + page_url)
    response = requests.get(page_url)
    page = soup(response.text, 'html.parser')
    car_tags = page.find_all(class_='EIR5N')
    car_data = []
    for cars in car_tags:
        car_link = cars.find('a', href=True)
        car_url = base_url + car_link['href']
        value_list = crawlCarData(car_url)
        car_data.append(value_list)
        time.sleep(2)
    return car_data

def crawlWebsite(page = 1):
    print('[ INFO ] ' + 'Crawling from ' + base_url)
    data = []
    for i in range(page):
        page_url = page_base_url + str(i+1)
        results = crawlPage(page_url)
        data += results
        time.sleep(2)
    print('[ INFO ] ' + 'Total data crawled: ' + str(len(data)))
    return data

def writeCSV(data, filename = 'test.csv'):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)
    csvfile.close()

def crawlCSV():
    data = crawlWebsite(page=1)
    now = datetime.datetime.now()
    fileName = str(now.year) + str(now.month) + str(now.day) + "-" + str(now.hour) + "_" + str(now.minute) + "_" + str(now.second) + "_carlist.csv"
    writeCSV(data, filename=fileName)

crawlCSV()