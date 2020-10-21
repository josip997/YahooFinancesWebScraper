from datetime import datetime, timedelta
import time
import requests, pandas, lxml
from lxml import html

import json

#formatiranje datuma za link
def format_date(date_datetime):
    date_timetouple=date_datetime.timetuple()
    date_mktime = time.mktime(date_timetouple)
    date_int = int(date_mktime)
    date_str = str(date_int)
    return date_str

#sastavljanje dijela linka
#proslijeđuje se simbol(firma), početni i krajnji datum, defaultni filter na history
def subdomain(symbol,start,end,filter='history'):
    subdoma='/quote/{0}/history?period1={1}&period2={2}&interval=1d&filter={3}&frequency=1d'
    subdomain = subdoma.format(symbol,start,end,filter)
    return subdomain

#funkcija za sastavljanje headera
def header_function(subdomain):
     hdrs =  {"authority": "finance.yahoo.com",
               "method": "GET",
               "path": subdomain,
               "scheme": "https",
               "accept": "text/html",
               "accept-encoding": "gzip, deflate, br",
               "accept-language": "en-US,en;q=0.9",
               "cache-control": "no-cache",
               "dnt": "1",
               "pragma": "no-cache",
               "sec-fetch-mode": "navigate",
               "sec-fetch-site": "same-origin",
               "sec-fetch-user": "?1",
               "upgrade-insecure-requests": "1",
               "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64)"}
     return hdrs

#scrape funkcija koja vraća html
def scrape_page(url, header):
    #pošalji request sa proslijeđenim url i header
    page = requests.get(url,header)
    #definiši sadržaj stranice u objekat elemenata html
    element_html = html.fromstring(page.content)
    #pokupi sve tabele iz objekta
    table = element_html.xpath('//table')
    #pretvori prvu pronađenu tabelu u byte string
    table_tree = lxml.etree.tostring(table[0], method='xml')
    panda = pandas.read_html(table_tree)
    return panda

if __name__ == '__main__':

    #početni datum je unazad godinu dana
    dt_start = datetime.today() - timedelta(days=365)
    #krajnji datum je danas
    dt_end = datetime.today()
    #formatiraj datume
    date_start = format_date(dt_start)
    date_end = format_date(dt_end)

    #definisan simbol
    sym='AAPL'

    #kreiran dio linka i header
    sub = subdomain(sym,date_start,date_end)
    header = header_function(sub)

    #sastavljen link
    base_url = 'https://finance.yahoo.com'
    url = base_url + sub

    #html sa podacima
    price_history = scrape_page(url,header)
    
    with open('price_history.txt', 'w') as filehandle:
        for listitem in price_history[0].values:
            filehandle.write('%s\n' % listitem)

    #print(price_history[0].values[3])
    


    




