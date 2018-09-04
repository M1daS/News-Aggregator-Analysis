from __future__ import unicode_literals
from django.shortcuts import render
from django.db import models
import django


#External Imports
import pandas as pd
import csv


import datetime
import os
import sys
pathsfile =  os.path.dirname(os.path.abspath('src/Pathsfile.py'))
sys.path.insert(0, pathsfile)

#Custom Imports
import Pathsfile as pf 
sys.path.insert(0, pf.path_SigmaSource)
sys.path.insert(0, pf.path_Sentiment)
sys.path.insert(0, pf.path_textAnalytics)
sys.path.insert(0, pf.path_textRetrieval)
import NewsRSS as news 
import ScrapeWebText as webscrape2 #using news3k instead
import LDA_Topic_Modeling as topmod
import wordnet_comparison as wordsim 
import textrank_summarization as textrank
import named_entity_recognition as ner
import sentiment_analysis_supervised_ml as sentiment_ml
import Ngram_Extraction as keyphrase
import normalization as norm
import Newspaper3k as news3k


def sigma_homepage(request):

	#RETRIEVE RSS Articles
	def retrieve_rss_articles():
		# rssOutput = news.start_rss()
		# rssOutputPath = pf.path_Data + '/rssArticles.csv'

		rssDict = dict()
		title,link,source,publisher = news.start_rss()
		for i in range(len(title)):
			authors, date, fulltext, image = news3k.init_news3k(link[i]) 	#Parse additional information using newspaper3k
			# topics = topmod.init_topmod(fulltext)
			topics = []
			rssDict[title[i]] = [link[i], source[i], publisher[i], authors, str(date), fulltext, image, topics]


		#GET LDA TOPICS FROM All ARTICLES CORPUS
		def find_main_topics(rssDict):
			fulltextToString = []
			titlesToString = []
			for k,v in rssDict.items():
				titlesToString.append(k)
				fulltextToString.append(v[5])
			titles = ' '.join(titlesToString)
			fulltext = ' '.join(fulltextToString)
			topics = topmod.init_topmod(fulltext)
			return topics
		maintopics = find_main_topics(rssDict)
		
		return (rssDict, maintopics)



	rssDict,maintopics = retrieve_rss_articles()
	maintopics = [topic.capitalize() for topic in maintopics]

	request.session['rssDict'] = rssDict
	request.session['maintopics'] = maintopics


	context = {
		'rssDict':rssDict,
		'maintopics':maintopics,
	}

	return render(request, 'sigma_homepage.html' , context)
	


from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('midasroot')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form,})



















# 	newsDictByArticle = dict()
# 	titlelist = []
# 	sentimentlist = []
# 	fullTextList = []
# 	bigramsList = []
# 	nersList = []
# 	topicsList = []

# 	for i in range(len(title)):
# 		newsDictByArticle[title[i]] = [link[i], source[i], publisher[i]]
# 		titlelist.append(str(title[i]))
# 		sentimentlist.append('positive')
# 		fullTextList.append(webscrape2.init(link[i]))
# 		#normalize the fulltext before finding bigrams and ners etc from it
# 		bigramsList.append(keyphrase.init_ngram_keyphrases(2, [fullTextList[i]]))
# 		#NER
# 		nerdict = ner.init_ner(fullTextList[i])
# 		tempners = []
# 		for k,v in nerdict.items():		# {MichaelSands:PERSON}
# 			tempners.append(k)
# 		nersList.append(tempners)
# 		topicsList.append(topmod.init_topmod(fullTextList[i]))


# 	#RETRIEVE SENTIMENT ANALYSIS
# 	sentiment_df = pd.DataFrame()
# 	datapath = pf.path_Data
# 	sentiment_path = datapath + '/news.csv'
# 	sentiment_training_path = datapath + '/news_training.csv'
# 	movie_training = 'C:/Users/sands/Desktop/movie_reviews_short.csv'
# 	sentiment_df['review'] = titlelist
# 	sentiment_df['sentiment'] = sentimentlist
# 	sentiment_df.to_csv(sentiment_path, index=False)
# 	sentiment = sentiment_ml.init_sentiment(movie_training, sentiment_path)


# 	#TRENDING TOPICS -  find the most frequent NERS amoung the entire Corpus
# 	trendingTopicsList = []
# 	TrendingTopicsFull = []
# 	flat_list_ners = [item for sublist in nersList for item in sublist]
# 	def wordListToFreqDict(wordlist):
# 		wordfreq = [wordlist.count(p) for p in wordlist]
# 		return dict(zip(wordlist,wordfreq))
# 	trendingTopicDict = wordListToFreqDict(flat_list_ners)
# 	import operator #sort dictionary from lowest freq words to highest


# 	#Get the most trending topics and the 21 most frequent trending topics
# 	sorted_full = sorted(trendingTopicDict.items(), key=operator.itemgetter(1))
# 	for item in sorted_full:
# 		k,v = item
# 		TrendingTopicsFull.append(k.strip())
# 	sorted_x = sorted(trendingTopicDict.items(), key=operator.itemgetter(1))[-21:] #get the 10 items with the highest values
# 	for item in sorted_x:
# 		k,v = item
# 		trendingTopicsList.append(k.strip())


# 	#COMPILE ALL DATA FOR MAIN NEWS DICTIONARYS
# 	ngrams_and_topics_list = []
# 	for i in range(len(title)):
# 		ngrams_and_topics = bigramsList[i] + topicsList[i]
# 		anchorTitle = title[i].replace(" ", "-")
# 		newsDictByArticle[title[i]] = [link[i], source[i], publisher[i], sentiment[i], fullTextList[i], bigramsList[i], nersList[i], topicsList[i], ngrams_and_topics, anchorTitle]
# # 




# 	newsDictByCorpus = {}
# 	newsDictByCorpus['TrendingTopics'] = trendingTopicsList
# 	newsDictByCorpus['TrendingTopicsFull'] = TrendingTopicsFull
# 	allbigramslist = []
# 	for k,v in newsDictByArticle.items():
# 		allbigramslist.append(v[5])
# 	newsDictByCorpus['Bigrams'] = allbigramslist



# 	request.session['newsDictByArticle'] = newsDictByArticle
# 	request.session['newsDictByCorpus'] = newsDictByCorpus

