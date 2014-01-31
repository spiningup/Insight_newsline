import os, json
from flask import Flask, render_template, request, jsonify
from ml import *
from get_data import *
import MySQLdb

app = Flask(__name__)
default_engine = "google"

def initialize_data():
    # get jobQuery and start
    q = request.form['jobQuery']
    if ":" in q:
        engine = q.split(':')[-1]
        if not (engine == "google" or engine == "nytimes"):
            engine = default_engine
        else:
            q = q.replace(':', '')
            q = q.replace(engine, '')
    else:
        engine = default_engine

    print "Search Engine : ", engine

    searchkey = "+".join(q.split())
    years, titles, urls, imgurls, snippets = get_dataset(option=engine, searchkey=searchkey)

    if engine == "google":
        ctitles, title_idx = clean_titles(titles, searchkey, light=False)
        displaytitles = clean_titles(titles, searchkey, light=True)[0]
    else:
        ctitles = titles
        title_idx = np.arange(len(titles))
        displaytitles = titles

    # clustering using hashing
    if len(displaytitles) > 150:
        n_clusters = 50
    else:
        n_clusters = len(displaytitles) // 3

    return searchkey, years, titles, urls, imgurls, ctitles, displaytitles, title_idx, n_clusters
        

@app.route("/")
def hello():
    return render_template('index.html') 

@app.route('/search')
def search():
    query = request.args.get('q', '')
    return render_template('search.html', query=query)

@app.route('/search?q=<query>')
def searchTo(query):
    query = query.replace('+',' ')
    return render_template('search.html', query=query)


@app.route('/analyze', methods=['POST'] )
def runAnalyze():
    
    searchkey, years, titles, urls, imgurls, ctitles, displaytitles, title_idx, n_clusters = initialize_data()

    dictResults = {}
    dictResults['query'] = searchkey

    # get timeline
    print "Number of clusters for timeline :", n_clusters
    timeline_method = "hashing"     # method = Hashing will lose featureshapce
    X, features = vectorization(displaytitles, method=timeline_method, n_features=300)
    ilabels = ml_kmeans(X, n_clusters=n_clusters)

    dictResults['items'] = []
    for idx in ilabels:
        if imgurls[idx] is not None:
            dictResults['items'].append({
                                     'title': displaytitles[idx], 'readmoreurl': urls[idx], 'photourl': imgurls[idx],
                                    'date': years[idx].strftime("%m/%d/%y"), 
                                    'displaydate': years[idx].strftime("%m/%d/%y"), 
                                    'caption': None,
                                    'body': None,
                                    })
    return jsonify(dictResults)


@app.route('/topics', methods=['POST'] )
def runGettopics():
    
    searchkey, years, titles, urls, imgurls, ctitles, displaytitles, title_idx, n_clusters = initialize_data()
    dictResults = {}
    dictResults['query'] = searchkey

    # get feature matrix 
#    sortbyyear = dictsorted({title: year for year, title in zip(years, displaytitles)})
#    sortedtitles = [item[0] for item in sortbyyear]
#
#    if timeline_method != "tfidf":
#        X, features = vectorization(sortedtitles, method="tfidf")
#        ilabels = ml_kmeans(X, n_clusters=n_clusters)
#            
#    dictResults['dim'] = X.shape
#
#    print "Shape of feature space : ", X.shape
#    dictResults['X'] = []
#    dictResults['yearlabel'] = []
#    for i in range(X.shape[0]):
#        yearlabel = None
#        if i > 1:
#            if int(sortbyyear[i-1][1].timetuple()[0]) - int(sortbyyear[i][1].timetuple()[0]) == 1:
#                yearlabel = sortbyyear[i][1].timetuple()[0]
#                dictResults['yearlabel'].append({'i': int(i), 'year': yearlabel})
#
#        for j, d in zip(X[i].indices, X[i].data):
#            dictResults['X'].append({'i': int(i), 'j': int(j), 'data': float(d), 
#                                     'year': yearlabel, 'label': features[j]})
#            yearlabel = None

    # topic extraction
    topics = topic_extraction(ctitles, n_features=500, n_topics = 10, n_top_words=2)
    topic_sorted_idx = sortby_topic(topics, ctitles, titles, title_idx)

    dictResults['topics'] = []
    for topic in topics:
        topicyears = []
        topictitle = None
            
        for item in topic_sorted_idx[topic]:
            i, similarity = item
            idx = title_idx[i]
            topicyears.append(years[idx])

        syear, smonth, sday = min(topicyears).timetuple()[0:3]
        eyear, emonth, eday = max(topicyears).timetuple()[0:3]

        # make topic captile
        topicCap = " ".join(["".join([b[0].upper(), b[1:]]) for b in topic.split()])
        dictResults['topics'].append({'term':topicCap, 'syear':syear, 'eyear':eyear, 'smonth':smonth, 'emonth':emonth,
                                      'sday':sday, 'eday':eday,
                                    })

    return jsonify(dictResults)


@app.route('/<pagename>') 
def regularpage(pagename=None): 
    """ 
    Route not found by the other routes above. May point to a static template. 
    """ 
    return "You've arrived at " + pagename
    #if pagename==None: 
    #    raise Exception, 'page_not_found' 
    #return render_template(pagename) 

if __name__ == '__main__':
    print "Starting debugging server."
    app.run(debug=False, host="0.0.0.0", port=80)



