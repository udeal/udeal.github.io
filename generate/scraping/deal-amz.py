from bs4 import BeautifulSoup
import requests
import pandas as pd
import time, datetime
import re
from urllib.parse import unquote

SITE='www.amazon.ca'
source = 'https://'+SITE+'/s?k=lightning+deals'

def get_url(term, page):
    ts = int(time.time())   
    pg = str(page)
    url = 'https://' + SITE + '/s?k='+ term.replace(' ','+') + '&page=' + pg + '&qid='+ str(ts) + '&ref=sr_pg_' + pg
    return url

def extract_record(item):
    atag = item.h2.a
    title = atag.text.strip()

    url_org = unquote(unquote('https://' + SITE + atag.get('href')))
    #print(url_org)
    m = re.search('/(?:dp|o|gp|-)\/(B[0-9]{2}[0-9A-Z]{7}|[0-9]{9}(?:X|[0-9]))/', url_org)
    item_url = 'https://' + SITE + m.group(0)

    try:
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text.replace('$','')
    except AttributeError:
        return
        
    try:
        price_origin_parent = item.find('span', 'a-price a-text-price')
        price_origin = price_origin_parent.find('span', 'a-offscreen').text.replace('$','')
    except AttributeError:
        price_origin = '0'

    try:
        rating = item.i.text
        review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
    except AttributeError:
        rating = ''
        review_count = ''

    image_url = item.find('img', 's-image')
    if image_url is not None:
        image_url = image_url.get('src')
    else:
        image_url = ''

    result = (title, price, price_origin, item_url, image_url)
    return result

def main(search_term):
    now = datetime.datetime.now().replace(microsecond=0).isoformat()
    df = pd.DataFrame(columns = ['Title', 'Price', 'Price_Origin', 'Link', 'Image', 'Retailer', 'TimeStamp', 'Source'])
    n = 0
    headers = {
        'authority': SITE,
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    
    for page in range(1,8):
        url = get_url(search_term, page)
        response = requests.get(url)
        res = requests.get(url, headers=headers)
        # Simple check to check if page was blocked (Usually 503)
        if res.status_code > 500:
            if "To discuss automated access to Amazon data please contact" in res.text:
                print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
            else:
                print("Page %s must have been blocked by Amazon as the status code was %d"%(url,res.status_code))
            return None
        # Pass the HTML of the page and create 

        soup = BeautifulSoup(res.text, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        for item in results:
            record = extract_record(item)
            #print(record)
            if record is not None:
                df.loc[n, 'Title'] = record[0]
                df.loc[n, 'Price'] = record[1]
                df.loc[n, 'Price_Origin'] = record[2]
                df.loc[n, 'Link'] = record[3]
                df.loc[n, 'Image'] = record[4]
                df.loc[n, 'Retailer'] = 'Amazon'
                df.loc[n, 'TimeStamp'] = now
                df.loc[n, 'Source'] = source
                n = n + 1

        time.sleep(1) #sleep 1 second

    # save records
    df.to_csv('amz.csv')

main('lightning deals')
