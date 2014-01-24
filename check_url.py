import json
from os.path import isfile
import os

def check_url(url, allurls):

    find = False
    for nurl in allurls:
        #m = re.search('\W'+nurl[:-1], url) # regular expression is very slow
        #if m is not None:
        if('.'+str(nurl[:-1]) in str(url)) or ('/'+str(nurl[:-1]) in str(url)):
            find = True            
            break
    return find


if __name__ == "__main__":

    allurls = json.load(open('googlenews_url.json','r'))
    query = "apple+China"

#    for year in range(2009, 2014):
#        for istart in range(1, 100, 10):
#            date_range1 = 'date:r:%s0101:%s0630' %(year, year)
#            if year != 2013:
#                date_range2 = 'date:r:%s0701:%s1231' %(year, year)
#            else:
#                date_range2 = 'date:r:%s0701:%s0230' %(year, year+1)
#            
#            for date_range in (date_range1, date_range2):
#                filename = 'data-google/%s_%s_%s.json'%(query, date_range, istart)

    urls = {}
    for filename in os.listdir('data-google/'):
#        if not isfile(filename):
#            continue
        try:
            results = json.load(open('data-google/'+filename,'r'))
        except:
            continue
        try:
            items = results['items']
        except:
            continue
        for item in items:
            find = check_url(item['link'], allurls)
            if find:
                url = ".".join(item['link'][7:].split('/')[0].split('.')[-2:])
                if url not in urls.keys():
                    urls[url] = 1
                    print url






