import json
import time
from datetime import datetime
import urllib2
from BeautifulSoup import BeautifulSoup
from readability.readability import Document
from nltk import clean_html
from boilerpipe.extract import Extractor
from check_url import check_url

def getnews(item):
    
    title = item['title']
    snippet = item['snippet']
#     date, snippet = item['snippet'].split(' ...')[:2]
#     date_object = datetime.strptime(date.replace(',',''), '%b %d %Y')
#     print date_object, snippet
    url = item['link']

    try:
        imgurl = item['pagemap']['cse_image'][0]['src']
    except:
        imgurl = None
#        print 'no image'
    text = None
#    try:
#        extractor = Extractor(extractor='ArticleExtractor', url=url)
#        text = extractor.getText().encode('utf-8')
#    except:
#        text = None
#        print 'text not extracted'

    return title.encode('utf-8'), snippet.encode('utf-8'), url, imgurl, text

if __name__ == "__main__":
    
    year = 2013
    istart = 1
    filename = 'data-google/apple+China_%(year)d0101:%(year)d1231_%(istart)d.json' % vars()
    data = json.load(open(filename,'r'))
    items = data['items']
    for item in items:
        tmp = getnews(item)
        if tmp is not None:
            title, snippet, url, imgurl, text = getnews(item)
