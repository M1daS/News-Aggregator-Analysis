import nltk


from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string


import sys
import os

import analytic_normalization as norm

def init_topmod(webtext):

	doc_clean = nltk.word_tokenize(webtext) 
	topic_list = []
	def display_topics(model, feature_names, no_top_words):
	    for topic_idx, topic in enumerate(model.components_):
	    	for i in topic.argsort()[:no_top_words]:
	    		topic_list.append(feature_names[i])


	tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=15, stop_words='english')
	tf = tf_vectorizer.fit_transform(doc_clean)
	tf_feature_names = tf_vectorizer.get_feature_names()
	no_topics = 200
	lda = LatentDirichletAllocation(n_components=no_topics, max_iter=50, learning_method='online', learning_offset=50.,random_state=0).fit(tf)
	no_top_words = 5
	display_topics(lda, tf_feature_names, no_top_words)


	finalTopicList = []
	from collections import Counter
	counts = Counter(topic_list)
	for k,v in counts.items():
		finalTopicList.append(k)

	return finalTopicList




# from sklearn.decomposition import LatentDirichletAllocation

# norm_corpus = normalize_corpus(toy_corpus)
# vectorizer, tfidf_matrix = build_feature_matrix(norm_corpus, 
#                                     feature_type='tfidf')                     
# total_topics = 2
# lda = LatentDirichletAllocation(n_topics=total_topics, 
#                                 max_iter=1000,
#                                 learning_method='online', 
#                                 learning_offset=50.,
#                                 random_state=42)
# lda.fit(tfidf_matrix)

# feature_names = vectorizer.get_feature_names()
# weights = lda.components_

# topics = get_topics_terms_weights(weights, feature_names)
# print_topics_udf(topics=topics,
#                  total_topics=total_topics,
#                  num_terms=8,
#                  display_weights=True)