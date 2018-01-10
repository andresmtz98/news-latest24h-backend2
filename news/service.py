# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import urllib
from .models import Article

CITY_DICTIONARY = {
    'es-419': 'ciudad',
    'en': 'city',
    'de': 'stadt',
    'ar': 'مدينة',
    'fr-ca': 'ville',
    'fr': 'ville',
    'iw': 'עִיר',
    'nl': 'stad',
    'it': 'città',
    'pl': 'miasto',
    'pt-BR': 'cidade',
    'pt-PT': 'cidade',
    'ru': 'город'
}

def search(edition_code, language_code, country_code, query):
    articles = []
    if query.find(':') == -1 or query == '':
        query = urllib.parse.quote(query)
        query = query.replace('%', '%25')
        url = "http://www.rssdog.com/index.htm?url=http%3A%2F%2Fnews.google.com%2Fnews%3Fpz%3D1%26cf%3Dall%26ned%3D{}%26hl%3D{}%26gl%3D{}%26scoring%3Dn%26q%3D{}%26output%3Drss%26num%3D30&mode=html&showonly=&maxitems=0&showdescs=1&desctrim=0&descmax=0&tabwidth=100%25&showdate=1&utf8=1&linktarget=_blank&textsize=inherit&bordercol=%23d4d0c8&headbgcol=%23999999&headtxtcol=%23ffffff&titlebgcol=%23f1eded&titletxtcol=%23000000&itembgcol=%23ffffff&itemtxtcol=%23000000&ctl=0"\
        .format(edition_code, language_code, country_code, query) # edition, language, country, query
        extractor(url,articles)
    else:
        if CITY_DICTIONARY[language_code] == query[:query.find(':')].lower():
            query = query[query.find(':')+1:]
            query = urllib.parse.quote(query)
            query = query.replace('%', '%25')
            url = "http://www.rssdog.com/index.htm?url=http%3A%2F%2Fnews.google.com%2Fnews%3Fpz%3D1%26cf%3Dall%26ned%3D{}%26hl%3D{}%26gl%3D{}%26scoring%3Dn%26geo%3D{}%26output%3Drss%26num%3D30&mode=html&showonly=&maxitems=0&showdescs=1&desctrim=0&descmax=0&tabwidth=100%25&showdate=1&utf8=1&linktarget=_blank&textsize=inherit&bordercol=%23d4d0c8&headbgcol=%23999999&headtxtcol=%23ffffff&titlebgcol=%23f1eded&titletxtcol=%23000000&itembgcol=%23ffffff&itemtxtcol=%23000000&ctl=0"\
            .format(edition_code, language_code, country_code, query) # edition, language, country, query
            extractor(url,articles)
    return articles


    
def extractor(url, articles):
    req = requests.get(url)
    bs = BeautifulSoup(req.text, 'html.parser')
    titles = bs.find_all('a', {'class': 'rssdog'})
    titles.pop(0)
    titles.pop(0)
    image_url = bs.find_all('img', {'class': 'rssdog'})
    description = bs.find_all('font', {'size': '-1'})
    publishedAt = bs.find_all('i')
    publishedAt.pop(0)
    for index in range(len(image_url)):
        article = Article()
        title = titles[index].text
        if title.count('-') >= 3:
            article.title, aux, article.source = tuple(title.rsplit('-',2))
            article.source =  aux.strip() + '-' + article.source
        else:
            article.title, aux = tuple(title.rsplit('-',1))
            article.source = aux.strip()

        article.publishedAt, article.url, article.urlImage = publishedAt[index].text, \
            titles[index]['href'], 'http://'+image_url[index]['src'][2:]
        articles.append(article)

    count = 0
    for desc in description:
        if len(desc.text) > 150 and count < len(image_url):
            articles[count].description = desc.text
            count += 1