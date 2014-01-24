import numpy as np
from saveto_mysql import saveto_mysql


def get_dataset(option='google', searchkey='apple+China'):
    import MySQLdb as mdb
    from datetime import datetime

    curstring = {
        'google': "SELECT * FROM dataGoogle WHERE searchkey = '%(searchkey)s'" % vars(), 
        'nytimes' : "SELECT * FROM dataNytimes WHERE searchkey = '%(searchkey)s' AND imgurl IS NOT NULL" % vars(),
# AND newstype = 'News'
        }

    con = mdb.connect('localhost', 'jun', 'insight', 'dataGoodb')
    cur = con.cursor()
    cur.execute(curstring[option])
    dataset = cur.fetchall()

    if len(dataset) == 0:
        print 'loading data from %s' %(option)
        print searchkey
        saveto_mysql(con, searchkey, engine="%s"%(option))
        print 'finishing saving to mysql'
        cur.execute(curstring[option])
        dataset = cur.fetchall()

    con.close()
    print 'number of articles', len(dataset)
    
    titles = []
    urls = []
    years = []
    imgurls = []
    snippets = []
    np.random.seed(0)
    for item in dataset:
        if option == 'google':
            year, istart, searchkey, title, snippet, url, imgurl, content = item
            pubdate = snippet.split(' ...')[0]
            try:
                year = datetime.strptime(pubdate.replace(',',''), '%b %d %Y')
            except:
                year = datetime(year, np.random.randint(1,12), np.random.randint(1,28), 0, 0)
        else:
            pubdate, searchkey, newstype, title, snippet, url, imgurl = item
            try:
                year = datetime.strptime(pubdate[:10], '%Y-%m-%d')
                if int(year.timetuple()[0]) < 1900:
                    continue
            except:
                continue

        titles.append(title)
        urls.append(url)
        years.append(year)
        imgurls.append(imgurl)
        snippets.append(snippet)
        
    return years, titles, urls, imgurls, snippets

if __name__ == "__main__":
    import sys
    searchkey = sys.argv[1]
    years, titles, urls, imgurls, snippets = get_dataset(option="nytimes", searchkey=searchkey)
    
