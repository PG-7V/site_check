import lxml
import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool
import time
from config import file_for_read, file_output

start_time = time.time()




# url = 'https://mail.ru'
# headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
#                'accept': 'text/html',
#                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}
#
# r = requests.get(url, headers=headers)
# soup = BeautifulSoup(r.text, 'lxml')
# head = soup.find('head')
# title = head.find('title').text.strip()
# print(title)
# desc = head.find_all("meta")
#
# print(desc)


#url = 'https://e-stroi.by/'
url = 'http://zhivi.by'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
    'AppleWebKit/537.36 (KHTML, like Gecko)'
    'Chrome/64.0.3282.167 Safari/537.36'
}

result = requests.get(url, headers=headers)


#print(result.text)
soup = BeautifulSoup(result.text, 'lxml')

# mail = soup.select('a[href^="mailto:"]')#.get_text(strip=True)
# tel = soup.select('a[href^="tel:"]')

mail = []
tel = []

links = soup.find_all('a')

for link in links:
    print(link)
    try:
        if (link.get('href').find('mailto:') > -1):
            #print(link.get('href').find('mailto:'))
            mail.append(link.string.strip())
    except:
        pass

    try:

        if (link.get('href').find('tel:') > -1):
            #print(link.get('href').find('tel:'))
            tel.append(link.string.strip())
        elif(link.get('href').find('tel:') > -1):
            tel.append(link.attrs['href'].strip())

    except:
        pass






# match = soup.find_all('a', "mailto:")
#match = soup.find('meta', name='description').attrs('content')
print(list(set(tel)))
print('------')
print(list(set(mail)))





