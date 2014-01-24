#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb as mdb
import json
import time
import sys 
from apiclient.discovery import build
from os.path import isfile
from urllib2 import urlopen

def google_api(query, date_range, start, save_json=True):

    filename = 'data-google/%s_%s_%s.json'%(query, date_range,start)
    if isfile(filename):
        res = json.load(open(filename,'r'))
    else:
        DevKey = None  # pls provide your api-key
        cxkey = None
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
#            articles = json.load(open(filename,'r'))
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



def check_url(url, allurls):

    find = False
    for nurl in allurls:
        #m = re.search('\W'+nurl[:-1], url) # regular expression is very slow
        #if m is not None:
        if('.'+str(nurl[:-1]) in str(url)) or ('/'+str(nurl[:-1]) in str(url)):
            find = True            
            break
    return find


def saveto_mysql(con, searchkey, engine="google"):

    if engine == 'google':
        allurls = json.load(open('googlenews_url.json','r'))
        
        with con:
            cur = con.cursor()
        #    cur.execute("DROP TABLE IF EXISTS dataGoogle");
        #    cur.execute("CREATE TABLE IF NOT EXISTS dataGoogle(year INT, istart INT, searchkey TINYTEXT, \
        #                 title TINYTEXT, snippet TINYTEXT, url TINYTEXT, imgurl TINYTEXT, content TEXT)");
            cur.execute("SELECT title FROM dataGoogle WHERE searchkey = '%(searchkey)s'" % vars())
            existing_titles = [title[0] for title in cur.fetchall()]

            for year in range(2013, 2008, -1):
                for istart in range(1, 100, 10):
                    date_range1 = 'date:r:%s0101:%s0630' %(year, year)
                    if year != 2013:
                        date_range2 = 'date:r:%s0701:%s1231' %(year, year)
                    else:
                        date_range2 = 'date:r:%s0701:%s0230' %(year, year+1)

                    for date_range in (date_range1, date_range2):
                        results = google_api(searchkey, date_range, istart, save_json=True)
                        n_results = int(results['searchInformation']['totalResults'])
                        if n_results < istart:
                            break
                        items = results['items']
                        for item in items:
                            find = check_url(item['link'], allurls)
                            if find:
                                title, snippet, url, imgurl, text = getnews(item)
                                if title not in existing_titles:
                                    cur.execute("INSERT INTO dataGoogle(year, istart, searchkey, title, snippet, url, \
                                         imgurl, content) values (%s, %s, %s, %s, %s, %s, %s, %s)", \
                                            (year, istart, searchkey, title, snippet, url, imgurl, text))
                print "Finishing getting 200 news from %s" %(year)
            
            con.commit()
    
    elif engine == 'nytimes':
        with con:
            cur = con.cursor()
    #        cur.execute("DROP TABLE IF EXISTS dataNytimes");
    #        cur.execute("CREATE TABLE IF NOT EXISTS dataNytimes(pubdate TINYTEXT, searchkey TINYTEXT, newstype TINYTEXT, \
    #                     title TEXT, snippet TINYTEXT, url TINYTEXT, imgurl TINYTEXT)");
            n_articles = nytimes_api(searchkey, save_json=True)
            maxpage = min(n_articles // 10, 99)
            print "finished retriving %d articles from Nytimes" %(n_articles)
            for page in range(maxpage):
                    filename = 'data-nytimes/articles_%(searchkey)s_%(page)s.json' % vars()
                    data = json.load(open(filename,'r'))
                    items = data['response']['docs']
                    for item in items:
                        try:
                            pubdate = item['pub_date'].encode('utf-8')
                        except:
                            pubdate = None
                        title = item['headline']['main'].encode('utf-8')
                        url = item['web_url']
    
                        try:
                            newstype = item['type_of_material'].encode('utf-8')
                        except:
                            newstype = None
                        if newstype == 'Letter':
                            continue
    
                        try:
                            snippet = item['snippet'].encode('utf-8')
                        except:
                            snippet = None
    
                        try:
                            imgurl = "http://www.nytimes.com/"+item['multimedia'][1]['url']
                        except:
                            imgurl = None
    
    
                        cur.execute("INSERT INTO dataNytimes(pubdate, searchkey, newstype, title, snippet, url, \
                                     imgurl) values (%s, %s, %s, %s, %s, %s, %s)", \
                                        (pubdate, searchkey, newstype, title, snippet, url, imgurl))
            
            con.commit()
                        
if __name__ == "__main__":
    con = mdb.connect('localhost', 'jun', 'insight', 'dataGoodb');
    saveto_mysql(con, "government+shutdown")
