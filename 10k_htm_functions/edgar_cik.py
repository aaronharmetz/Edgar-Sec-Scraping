import pandas as pd
import numpy as np
import requests 
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
#Goal: Create a dataframe holding every cik with its corresponding name, ticker, & exchange

# In[Additional Resources and Important Notes]
#1. How to access edgar data: https://www.sec.gov/os/accessing-edgar-data

## sec edgar request limit ~ 10 requests / second
## Extracting + cleaning + appending a single master.idx file ~ 0.3-0.4 seconds

# In[Request document and decode]

url = 'https://www.sec.gov/data/company_tickers_exchange.json'
req = requests.get(url).content


#decode utf-8 encoded byte string
#skip to 52: index to remove field names
#split split('],[') makes organized list for (1) cik, (2) name, (3) ticker, (4) exchange
document_content = req.decode('utf-8').replace(':','')[52:].split('],[')

# In[Extract and clean cik, name, ticker, exchange]

#Initialize empty list to append future clean rows
cik_list = []
for document_content in document_content:
    row = document_content.split(',') #split commas, each piece of content is an element in a list

    #Important: Some names that contain Inc. will hold 5 elements in a list instead of 4.
    #To keep data clean: row[0]=cik, row[1]=name, row[-2]=ticker, row[-1]=exchange
    #This will avoid mismatched rows and confusion

    row_values = [int(row[0]), row[1], row[-2], row[-1]]
    #Remove " from every string element in list
    clean_row = [x.strip('"') if type(x) == str else x for x in row_values]
    cik_list.append(clean_row)


df = pd.DataFrame(data=cik_list, columns=['cik', 'name', 'ticker', 'exchange'])
df.loc[df.index[-1], 'exchange'] = 'Nasdaq' #fix last row exchange name


# In[Create Edgar cik str value]

#Every url that contains a companies cik, contains a str length of 10. Add leading zeros to replicate cik url component
#Ex make cik # 320193 -> 0000320193
#Subtract len of cik str from 10 = number of leading zeros needed

cik_url_len = 10
cik_zeros = df.cik.map(lambda x: cik_url_len - len(str(x))) #amount of leading zeros needed for each cik

#Create cik string column and cik_zero column for adding leading zeros (apply lambda)
df['cik_str'] = df['cik'].astype(str)
df['cik_zeros'] = cik_zeros

#Add number of trailing zeros to cik string
cik_str = df.apply(lambda x: (x['cik_zeros'] * '0') + x['cik_str'], axis=1)
df.drop(['cik_str', 'cik_zeros'], axis=1, inplace=True)
df.insert(1, 'cik_str', cik_str)



#subset dataframe on the Nasdaq or NYSE exchange 

df = df[(df['exchange'] == 'Nasdaq') | (df['exchange'] == 'NYSE')]

#find every duplicated cik_str index 
duplicated_index = list(df[df.duplicated(subset=['cik_str'])].index)

#remove duplicate cik_str
df.drop(duplicated_index, inplace=True)
df.reset_index(drop=True, inplace=True)

#push to csv file 
df.to_csv('unique_cik.csv', index=False, header=True)




print(df.head(10))




