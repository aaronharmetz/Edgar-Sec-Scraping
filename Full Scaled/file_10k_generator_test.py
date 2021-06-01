import pandas as pd
import numpy as np
import time 
from file_10k_generator import url_10k_constructor, url_10k_htm, htm_10k_file



#NOTE: The purpose of this py file is to generate every htm url for 10K files for any given company
    #aka CIK (CIK strings were collected from edgar_cik.py) 

#step 1: construct url to land on edgar sec page that contains every 10k htm url  
#step 2: scrape every 10k htm url 
#step 3: request each 10k htm url and scrape for every htm 10k FILE (what we want to scrape different financial table data)




#read in dataframe with unique cik values 
df = pd.read_csv('unique_cik.txt', dtype=str)

#grab cik_str values & ticker 
unique_cik = list(df['cik_str'])
unique_ticker = list(df['ticker'])


cik_identification = list(zip(unique_cik, unique_ticker))


for cik in cik_identification:
    start = time.time()
    filings_10k = url_10k_constructor(cik=cik[0])

    htm_10k = url_10k_htm(filtered_10k_link=filings_10k)
    if len(htm_10k) == 0:
        continue
    final_htm_files, filing_date = htm_10k_file(htm_10k=htm_10k)
    #print(final_htm_files)

    df = pd.DataFrame(data=[final_htm_files, filing_date]).T
    df.insert(0, 'ticker', cik[1])
    df.to_csv('file_10k_htm.csv', mode='a', header=False, index=False)
    end = time.time()
    print('One CIK Iteration: ', end-start)
    print(cik[1])



