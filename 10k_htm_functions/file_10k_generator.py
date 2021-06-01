import pandas as pd
import numpy as np
import requests 
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time 
from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path

#NOTE: The purpose of this py file is to generate every htm url for 10K files for any given company
    #aka CIK (CIK strings were collected from edgar_cik.py) 

#step 1: construct url to land on edgar sec page that contains every 10k htm url  
#step 2: scrape every 10k htm url 
#step 3: request each 10k htm url and scrape for every htm 10k FILE (what we want to scrape different financial table data)




#################### NOTE: Test file for a single company, Apple Inc ####################


#given a company cik, gather every 10-K document 
def url_10k_constructor(cik):
    annual_url = f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=10-K&dateb=&owner=exclude&count=100&search_text='
    return annual_url 


#construct every 10k hml url for a given cik (aka company)
def url_10k_htm(filtered_10k_link): 

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('disable-blink-features=AutomationControlled')
    ua = UserAgent()
    ua_str = str(ua.chrome)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(filtered_10k_link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    driver.close()
    
    try:
        table_tags = soup.find_all('table')#.find_all('tr') #last table always contains information 
        tr_tags = table_tags[-1].find_all('tr')
    
    except IndexError:
        return []

    else:
   
        document_html = []
        base_url = 'https://www.sec.gov'
        for tr_tags in tr_tags[1:]:
            td_tags = tr_tags.find_all('td')
            if td_tags[0].text == '10-K':
                a_href_tag = tr_tags.find_all('td')[1].find('a')['href']
                document_html.append(base_url+a_href_tag)
        return document_html


#20 second run time 
### Important Note: url's only work until 2000-2002 range, any time before will be text files.
    ### Fully scaling pre 2000-2002 files will require completly different functions and code ###

def htm_10k_file(htm_10k):

    htm_file_list = []
    filing_date = []
    base_url = 'https://www.sec.gov'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('disable-blink-features=AutomationControlled')
    for files in htm_10k:

        ua = UserAgent()
        ua_str = str(ua.chrome)
        chrome_options.add_argument('user-agent=f{ua_str}')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(files)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        driver.close()

        tr_tags = soup.find_all('tr') #faster to search table but not every file contains table
        for tr in tr_tags:
            try:

                if tr.find('td').text == '1': #if first element of td tag text is 1, we have our target row
                    target_td = tr.find_all('td')
                    target_url = target_td[2].find('a')['href'] #url is always in index 2 with a tag href tag]
                    htm_file_list.append(base_url + target_url)
                    filing_date.append(int(soup.find_all('div', {'class': 'info'})[0].text[:4]))

            except (AttributeError, IndexError):
                pass

    return htm_file_list, filing_date






