
# coding: utf-8

# In[1]:


import re
import random
import time
import numpy as np
import pandas as pd
from contextlib import contextmanager

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import staleness_of

from joblib import Parallel, delayed


# In[2]:


driver_path = 'crawler/chromedriver'
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--window-size=1200, 600')

def get_wtime(mean=2.25, std=0.75, min_bound=0.75):
    wtime = np.random.normal(mean, std)
    return wtime if wtime > min_bound else min_bound

wtime_async = 5
total_attemps = 3
batch_size = 25


# In[3]:


@contextmanager
def wait_for_page_load(driver, timeout=5):
    old_page = driver.find_element_by_tag_name('html')
    yield
    WebDriverWait(driver, timeout).until(staleness_of(old_page))


# In[4]:


def get_cid_and_back(driver, element, original_url=None):
    ActionChains(driver).move_to_element(element).perform()
    element.click()
    time.sleep(get_wtime())
    cid_match = re.findall(r':0x(.+?)!', driver.current_url, re.M|re.I)[-1]

    if original_url is None:
        back_button = driver.find_element_by_xpath("//button[@class='section-back-to-list-button blue-link noprint']")
        back_button.click()
        time.sleep(get_wtime())
    else:
        driver.get(original_url)
        time.sleep(get_wtime())
    
    return int(cid_match, 16)


# In[5]:


def get_view_more_results(driver):
    name_cid_pairs = []

    names_elements = driver.find_elements_by_xpath("//h3[@class='section-result-title']")
    if names_elements == []:
        raise Exception('Empty names')
    names = [name.text.strip() for name in names_elements]

    for i, name in enumerate(names):
        res_i_element = driver.find_elements_by_xpath("//div[@class='section-result']")[i]
        cid = get_cid_and_back(driver, res_i_element)
        name_cid_pairs.append((name, cid))
    
    return name_cid_pairs


# In[6]:


def get_origin_results(driver):
    name_cid_pairs = []
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    names = soup.find_all("div", {"class": "section-related-place-title blue-link"})
    if names == []:
        raise Exception('No related searches')
    names = [name.text.strip() for name in names]

    for i, name in enumerate(names):
        res_i_element = driver.find_elements_by_xpath("//div[@class='section-related-place-title blue-link']")[i]
        cid = get_cid_and_back(driver, res_i_element, driver.current_url)
        name_cid_pairs.append((name, cid))
        
    return name_cid_pairs


# In[7]:


def get_people_also_search_for(place_id):
    url = 'https://www.google.com/maps/place/?q=place_id:' + place_id

    name_cid_pairs = []
    attempts = 0
    crawl_err = True
    err_mess = ''
    
    while attempts < total_attemps and crawl_err == True:
        driver = webdriver.Chrome(driver_path, options=options)
        try:            
            with wait_for_page_load(driver, timeout=wtime_async):
                driver.get(url)

            view_more = False

            view_more_elements = driver.find_elements_by_xpath("//button[@aria-label='View more']")
            if view_more_elements != []:
                view_more_button = view_more_elements[0]
                view_more = True

            if view_more:
                ActionChains(driver).move_to_element(view_more_button).perform()
                view_more_button.click()
                time.sleep(get_wtime())
                name_cid_pairs = get_view_more_results(driver)
            else:
                name_cid_pairs = get_origin_results(driver)

            if name_cid_pairs == []:
                raise Exception('Empty pairs')
        
            crawl_err = False
        except Exception as e:
            attempts+=1
            crawl_err = True
            err_mess = str(e)
            time.sleep(get_wtime())
        finally:
            driver.close()
    
    if crawl_err:
        return place_id, attempts, 'ERR: ' + err_mess
    else:
        return place_id, attempts, name_cid_pairs


# In[8]:


def get_people_also_search_for_batch(batch_place_ids):
    batch_attempts = 0
    previous_errs = 0
    batch_err = True
    batch_results = []
    batch_erros = []

    while batch_attempts < total_attemps and batch_err:
        start = time.time()

        results = Parallel(n_jobs=4)(delayed(get_people_also_search_for)(place_id) for place_id in batch_place_ids)
        finished_pages = [res for res in results if 'ERR:' not in res[2]]
        err_pages = [res for res in results if 'ERR:' in res[2]]

        end = time.time()
        seconds = end - start
        print(str(len(finished_pages)) + ' finished pages: ' + 
              str(seconds/60.) + ' mins, ' +
              str(seconds/3600.) + ' hours')
        print('total errors:', len(err_pages))
        
        batch_results.extend(finished_pages)
        if err_pages == [] or len(err_pages) == previous_errs:
            batch_err = False
        else:
            previous_errs = len(err_pages)
            batch_place_ids = [res[0] for res in err_pages]
            batch_attempts+=1
            time.sleep(get_wtime())
            
    batch_erros = err_pages
    return batch_results, batch_erros


# In[9]:


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


# In[10]:

if __name__ == "__main__":
    
    df = pd.read_csv('data/place_ids_singapore.csv')
    place_ids = df['place_id']
    total_place_ids = len(place_ids)
    
    #Crawl a batch and append the results to files
    for i, place_id_chunk in enumerate(chunks(place_ids[:total_place_ids], batch_size)):
        batch_results, batch_erros = get_people_also_search_for_batch(place_id_chunk)
        
        if batch_results != []:
            df_results = pd.DataFrame(batch_results)
            with open('data/recommendations.csv', 'a') as f:
                df_results.to_csv(f, index=False, header=False)
        else:
            df_empties = pd.DataFrame(place_id_chunk)
            with open('data/empties_crawl.csv', 'a') as f:
                df_empties.to_csv(f, index=False, header=False)
                
        if batch_erros != []:
            df_erros = pd.DataFrame(batch_erros)
            with open('data/error_pages.csv', 'a') as f:
                df_erros.to_csv(f, index=False, header=False)
        
        print('DONE BATCH: %s/%s' %(batch_size*(i+1), total_place_ids))
        time.sleep(get_wtime(6,2))
        
    #TODO: Fix OSError: [Errno 12] Cannot allocate memory after running for a while

    df1 = pd.read_csv('data/place_ids_singapore.csv')
    placeid_name_dict = dict(zip(df1['place_id'], df1['name']))
    df2 = pd.read_csv('data/recommendations.csv')
    names = [placeid_name_dict[m_id] for m_id in df2['place_id']]
    df2['name'] = names
    df2 = df2[['place_id', 'name', 'recommendations']]
    df2.to_csv('data/recommendations.csv', index=False)