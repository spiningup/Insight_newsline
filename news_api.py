import json
import time
from apiclient.discovery import build
from os.path import isfile
from urllib2 import urlopen


def google_api(query, date_range, start, save_json=True):

    filename = 'data-google/%s_%s_%s.json'%(query, date_range,start)
    if isfile(filename):
        res = json.load(open(filename,'r'))
    else:
        DevKey = (open('google-apikey.txt','r')).read().replace('\n','')
        cxkey = '008838510968646805464:e2528gaize0'
        service = build("customsearch", "v1",developerKey=DevKey) 
        res = service.cse().list(q = query, 
                                         cx = cxkey,  
                                         sort = date_range,  
                                         start=start, 
                                         ).execute() 
        if save_json:
            with open('data-google/%s_%s_%s.json'%(query, date_range,start), 'w') as outfile:
                     json.dump(res, outfile, sort_keys = True, indent = 2)

    return res

def nytimes_api(queue, save_json=True):
    apikey = "352BFF2F987829A9EB0652FE6AA12946:7:68679319"
    sections = ['all-sections']

    for page in range(99):

        if page % 10 == 0:
            print "%d number of articles retrived"%(page*10)
        filename = 'data-nytimes/articles_%(queue)s_%(page)s.json' % vars()
        if isfile(filename):
            continue
        else:
            url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?q=%(queue)s&page=%(page)d&api-key=%(apikey)s" % vars()
            articles = json.loads(urlopen(url).read())
            if save_json:
                with open(filename, 'w') as outfile:
                    json.dump(articles, outfile, sort_keys = True, indent = 2)

            n_articles = articles['response']['meta']['hits']
            if page * 10 > n_articles:
                break
#        time.sleep(0.1)
    return n_articles

def getnews(item, getcontent=False):
    
    from boilerpipe.extract import Extractor
    title = item['title']
    snippet = item['snippet']
    url = item['link']

    try:
        imgurl = item['pagemap']['cse_image'][0]['src']
    except:
        imgurl = None
    text = None
    if getcontent:
        try:
            extractor = Extractor(extractor='ArticleExtractor', url=url)
            text = extractor.getText().encode('utf-8')
        except:
            print 'not able to extract text'

    return title.encode('utf-8'), snippet.encode('utf-8'), url, imgurl, text
