import numpy as np

def clean_titles(titles, searchkeys, light=True):
    import nltk
#    stemmer = nltk.stem.lancaster.LancasterStemmer()
#    stemmer = nltk.stem.snowball.EnglishStemmer(ignore_stopwords=True)

    searchkeys = searchkeys.split('+')
    print 'searchkeys', searchkeys
    ctitles = []
    index = []
    # google titles have such patterns : 
    # ... something ... 
    # ... something | cnet 
    for idx, title in enumerate(titles):
        # clean the title to make it looks better
        if "-" in title:
            title = " ".join(title.split('-')[:-1])
        elif "|" in title:
            title = " ".join(title.split('|')[:-1])
        elif "..." in title:
            title = title.replace("...", "")
        if light is True: # the following is for machine learning purposes
            ctitles.append(title)
        else:
            title = title.lower().decode('utf-8')
            for searchkey in searchkeys:
                    title = title.replace(searchkey.lower(), "")
            #title = " ".join([stemmer.stem(t) for t in title.lower().split()])
            if not (title in ctitles):
                ctitles.append(title)
                index.append(idx)

    return ctitles, index

def vectorization(dataset, method="tfidf", n_features=2000):
    if method == "hashing":
        from sklearn.feature_extraction.text import HashingVectorizer
        vectorizer = HashingVectorizer(n_features=n_features,
                                   stop_words='english', non_negative=True,
                                       norm=None, binary=False)
        X_train = vectorizer.fit_transform(dataset) # dim(n_dataset, n_features)

        return X_train, None

    elif method == 'tfidf':
        # Tf-IDF tells the frequency of each term in each document
        from sklearn.feature_extraction.text import TfidfVectorizer
        import scipy.sparse as sp
    
        # nfeatures are the number of distinct words, except stop_words, in the dataset
        vectorizer = TfidfVectorizer(max_df=0.8, stop_words='english', ngram_range=(1, 2))
        X_train = vectorizer.fit_transform(dataset) # X-dim(ndataset, nfeatures)
        assert sp.issparse(X_train)

        features = vectorizer.get_feature_names()
        # get the most frequent features by summing over the tf-idf
#        featurefreqs = {feature : 0 for feature in features}
#        for i in range(len(dataset)):
#            for indice, data in zip(X_train[i].indices, X_train[i].data):
#                featurefreqs[features[indice]] += data
#        featurefreqs = dictsorted(featurefreqs)

        return X_train, features


def ml_kmeans(X, n_clusters=50):
    # help to cluster my dataset(titles or text) into buckets and show the centroid of the cluster on timeline
    from sklearn.cluster import KMeans
    from sklearn import metrics

    km = KMeans(n_clusters=n_clusters, init='k-means++', 
                max_iter=100, n_init=1,
                    verbose=False)
    km.fit(X)

    uniquelabels = np.unique(km.labels_) # n_clusters
    centers = km.cluster_centers_ # n_features
    
    minscore = {} #np.zeros(len(centers))
    ilabels = np.zeros(len(centers), dtype=int) # labels that are close to the centroid of each cluster

    clusters_idx = {}
    for i in range(n_clusters):
        clusters_idx[i] = np.where(km.labels_ == i)
#        print i, len(clusters_idx[i][0])

    for ilabel, label in enumerate(uniquelabels): # ncluster
        for id, i in enumerate(km.labels_): # ndataset
            if i == label:
                distance = X[id] - centers[ilabel]
                score = np.sqrt(np.inner(distance, distance))
                # find the article label close to the centroid
                if not minscore.has_key(ilabel):
                    minscore[ilabel] = score
                    ilabels[ilabel] = id
                else:
                    if minscore[ilabel] > score:
                        minscore[ilabel] = score
                        ilabels[ilabel] = id
    return ilabels

def ml_meanshift(X):
    from sklearn.cluster import MeanShift, estimate_bandwidth
    bandwidth = estimate_bandwidth(X, quantile=0.5, n_samples=300)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(X)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_

    labels_unique = np.unique(labels)
    n_clusters = len(labels_unique)
    for i in range(n_clusters):
        print i, len(np.where(labels == i))
    return

def topic_extraction(dataset, n_features = 300, n_topics = 10, n_top_words=2):
    # http://scikit-learn.org/stable/auto_examples/applications/topics_extraction_with_nmf.html#example-applications-topics-extraction-with-nmf-py
    from sklearn.feature_extraction import text
    from sklearn import decomposition
    n_samples = len(dataset)

    vectorizer = text.CountVectorizer(max_df=0.85, max_features=n_features, stop_words='english')
    counts = vectorizer.fit_transform(dataset[:n_samples])
    tfidf = text.TfidfTransformer().fit_transform(counts)

    # Fit the NMF model
    print("Fitting the NMF model on with n_samples=%d and n_features=%d..."
          % (n_samples, n_features))
    nmf = decomposition.NMF(n_components=n_topics).fit(tfidf)
    
    # Inverse the vectorizer vocabulary to be able
    feature_names = vectorizer.get_feature_names()

    topics = []
    for topic_idx, topic in enumerate(nmf.components_):
        topics.append(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    return topics

def sortby_topic(topics, cdataset, dataset, transform_idx): 
    # cdataset - cleaned dataset
    # dataset - full dataset
    # transform_idx provides indices from dataset -> cdataset
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    X_train = vectorizer.fit_transform(cdataset) # X-dim(ndataset, nfeatures)
    features = vectorizer.get_feature_names()

    vec = np.zeros(X_train.shape[1], dtype=int)
    topic_sorted_idx = {}
    for topic in topics:
        vec[:] = 0
        for item in topic.split():
            vec[features.index(item)] = 1
        similarity = X_train.dot(vec)
        relevant_title_idx = np.where(similarity > 0)[0]
        #topic_sorted_data[topic] = dictsorted({titles[title_idx[idx]]: similarity[idx] for idx in relevant_title_idx})
        topic_sorted_idx[topic] = dictsorted({idx: similarity[idx] for idx in relevant_title_idx})
        
    return topic_sorted_idx

def save_csv(years, titles, urls, imgurls, ilabels):
    import csv
    f = csv.writer(open("results-kmeans-titleonly.csv", "w"))                
    for i in ilabels:
        f.writerow([titles[i], '1/1/%s'%(years[i]), 
                    '1/1/%s'%(years[i]), imgurls[i], None, None, urls[i]])

def dictsorted(func):
    return sorted(func.items(), key=lambda x: x[1], reverse=True)

    
if __name__ == "__main__":
    searchkey = "apple+China"
    from get_data import get_dataset
    years, titles, urls, imgurls, snippets = get_dataset(option="google", searchkey=searchkey)
    ctitles, title_idx = clean_titles(titles, searchkey, light=False)
    displaytitles = clean_titles(titles, searchkey, light=True)[0]
#    print len(titles), len(displaytitles)

    # clustering using hashing
#    X = vectorization(titles, method="tfidf")[0]
#    ilabels = ml_kmeans(X, n_clusters=50)
#    ml_meanshift(X)

    # obtain features
#    X, featurefreqs = vectorization(ctitles, method="tfidf")
#    for featurefreq in featurefreqs[:100]:
#        print featurefreq
#    ilabels = ml_kmeans(X, n_clusters=50)
#    for i in ilabels:
#        print years[i], snippets[i] #[title_idx[i]] #displaytitles[title_idx[i]]#, urls[i]

    # topic extraction
    topics = topic_extraction(ctitles, n_features = 300, n_topics = 10, n_top_words=2)
    topic_sorted_idx = sortby_topic(topics, ctitles, titles, title_idx)

    no_distinct_titles = {idx:0 for idx in range(len(titles))}
    for topic in topics:
        print topic, len(topic_sorted_idx[topic])
        sortbyyear = dictsorted({item[0]: years[title_idx[item[0]]] for item in topic_sorted_idx[topic]})
        print topic, sortbyyear[0], years[title_idx[sortbyyear[0][0]]]
        print topic, sortbyyear[-1], years[title_idx[sortbyyear[-1][0]]]

        print topic, years[title_idx[topic_sorted_idx[topic][0][0]]]
#        for item in topic_sorted_idx[topic]:
#            idx, similarity = item
#            no_distinct_titles[title_idx[idx]] += 1
#            print topic, years[title_idx[idx]], displaytitles[title_idx[idx]], similarity


#    for i in range(len(titles)):
#        if no_distinct_titles[i] == 0:
#            print displaytitles[i]



