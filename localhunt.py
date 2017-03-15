from random import choice
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from bs4 import BeautifulSoup
import datetime
from concurrent.futures import ThreadPoolExecutor
import sqlite3 as sql
import time
from selenium import webdriver
import re
from collections import defaultdict
from threading import Thread

# Google Location Settings

domain = 'https://www.google.co.uk'
threads = 3
unix = int(time.time())
date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d'))
keyword = [line.rstrip('\n') for line in open('keywords.txt')]
keywords = [str.replace(x,' ','+') for x in keyword]

class local_results():

    data = defaultdict(list)

    def __init__(self, body, keyword,driver):
        soup = BeautifulSoup(body,'html')
        local = soup.find('a', attrs={'class':'cMjHbjVt9AZ__button'})
        local = local['href']
        geo = re.sub(".*rllag=",'',local)
        geo = re.sub(',[0-9]+&tbm.*','',geo)
        driver.get(domain+local)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source,'html')
        results = soup.find_all('div',attrs={'class':'_gt'})
        # Cycle through and grab out all the elements we care about from that local listing page
        for a, b in enumerate(results):
            dinner = b
            header = dinner.find('div', attrs={'class': '_rl'}).text
            result = a + 1
            try:
                url = dinner.find('a', attrs={'class': 'rllt__action-button _Jrh'})
                url = url['href']
                if url.find('/aclk') != -1:
                    url_type = 'Paid'
                else:
                    url_type = 'Organic'
            except:
                url = 'No website'
                url_type = 'N/A'
            try:
                score = dinner.find('span', attrs={'class': '_PXi'}).text
            except:
                score = 'No score'
            try:
                details = dinner.find('span', attrs={'class': 'rllt__details lqhpac'}).text
                number = re.sub('\).*', '', details)
                number = re.sub('.*\(', '', number)
            except:
                number = 'No info'
            try:
                address = dinner.find('a', attrs={'class': 'rllt__action-button rllt__directions-button'})
                address = address['href']
                address = re.sub('/maps/dir/\'\'/', '', address)
                address = re.sub('/data.*', '', address)
                address = re.sub('\+', ' ', address)
            except:
                address = "No Directions"

            self.to_csv(header,result,url,url_type,score,number,address,keyword,geo)
        time.sleep(5)
        self.save()

    @classmethod
    def to_csv(self,header, result, url, url_type, score, number, address, keyword, geo):
        local_results.data['title'].append(header)
        local_results.data['result'].append(result)
        local_results.data['url'].append(url)
        local_results.data['url_type'].append(url_type)
        local_results.data['score'].append(score)
        local_results.data['review'].append(number)
        local_results.data['address'].append(address)
        local_results.data['keyword'].append(keyword)
        local_results.data['geo'].append(geo)

    @classmethod
    def save(self):
        df1 = pd.DataFrame(self.data)
        df1.to_csv('results1.csv', mode='a', index=False, header=False)

def ranks(i):
    driver = webdriver.Chrome(executable_path='/Users/willcecil/Dropbox/Python/chromedriver')
    #driver = webdriver.PhantomJS(executable_path='/Users/willcecil/Dropbox/Python/phantomjs')
    url = domain + '#q=' + i + '&num=50'
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source)
    local_results(driver.page_source, i,driver)
    print("Opening this page " + domain+ '#q='+i)
    try:
        results = soup.findAll('div',attrs={'class':'g'})
        data = defaultdict(list)
        for a,b in enumerate(results):
            soup = b
            header = soup.find('h3')
            result = a + 1
            print(result)
            title = header.text
            link = soup.find('a')
            url = link['href']
            url = re.sub(r'/url\?q=', '',str(url))
            url = re.sub(r'&sa=.*', '',str(url))
            description = soup.find('span', attrs={'class':'st'})
            description = description.text
            result_type = "Standard Serp"
            # Store that data! All in dict so it's easy to dump into pandas/mongo
            data['Date'].append(date)
            data['Unix'].append(unix)
            data['Keyword'].append(i)
            data['Title'].append(title)
            data['Description'].append(description)
            data['Rank'].append(result)
            data['Type'].append(result_type)
            data['URL'].append(url)
            #data['Domain'].append(domain)

        df = pd.DataFrame(data)
        df.to_csv('results.csv', mode='a', index=False)

    except Exception as e:
        print(e)
    driver.quit()

def main():
    futures = []
    with ThreadPoolExecutor(max_workers=threads) as ex:
        for keyword in keywords:
            futures.append(ex.submit(ranks,keyword))


main()


