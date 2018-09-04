from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse



import sys
import os
import pandas as pd
import nltk
import re
import csv

pathsfile =  os.path.dirname(os.path.abspath('src/Pathsfile.py'))
sys.path.insert(0, pathsfile)
import Pathsfile as pf 

sys.path.insert(0, pf.path_SigmaSource)
sys.path.insert(0, pf.path_Sentiment)
sys.path.insert(0, pf.path_textAnalytics)
sys.path.insert(0, pf.path_textRetrieval)

import NewsRSS as news 
import ScrapeWebText as webscrape2
import pyGoogle as goog 
import LDA_Topic_Modeling as topmod
import wordnet_comparison as wordsim 
import textrank_summarization as textrank
import named_entity_recognition as ner
import sentiment_analysis_supervised_ml as sentiment_ml
import Ngram_Extraction as keyphrase
import word2vecSimilarity as w2v
import cosineSimilarity as cosine











def news_homepage(request):
	rssDict = request.session['rssDict']
	maintopics = request.session['maintopics']


	context = {
		'rssDict':rssDict,
		'trendingtopics':maintopics,
		'title':'Sigma News',
		'trendingbar':True,
	}

	return render(request, 'article_display.html', context)




#AJAX called
def get_summary(request):

	def search():
		if 'newsitem' in request.GET:
			x = request.GET['newsitem']
		else:
			x = 'Form is empty'
		return x
	article_link = search()

	webtext = webscrape2.init(article_link)
	out,thesissent = textrank.init(webtext, num_sentences=6)


	rssDict = request.session['rssDict']
	maintopics = request.session['maintopics']

	#extract quotes
	# text1 = 'Hi my name is "michael sands" and i want to "extract the quotes"'
	# print(re.findall(r'"(.*?)"', text1))

	data = {
        'summarytext': out,
        'thesis':thesissent,
        # 'similarArticles':similarArticleList,
        # 'anchorlist':anchorlist,
    }
	return JsonResponse(data)







def trending_topic(request):


	rssDict = request.session['rssDict']
	maintopics = request.session['maintopics']

	def search():
		if 'topic' in request.GET:
			x = request.GET['topic']
		else:
			x = 'Form is empty in trending topic'
		return x
	topic = search()
	print(topic)

	topic_dict = dict()
	for k,v in rssDict.items():
		wordtokens = nltk.word_tokenize(v[5])
		if topic in wordtokens or topic.capitalize() in wordtokens:
			topic_dict[k] = v

	#create one string containing all article fulltexts in the group (topic_dict) to summarize
	fulltextlist = []
	for k,v in topic_dict.items():
		fulltextlist.append(v[5])
	fulltextstring = ' '.join(fulltextlist)
	topic_summary,topic_thesis = textrank.init(fulltextstring, num_sentences=10)
		#each line in the summary needs to contain a href link to the article bubble that it is extracted from


	#compute similarity of an article
	

	

	context = {
		'rssDict':topic_dict,
		'title':topic.capitalize(),
		'topic_summary':topic_summary,
		'topic_thesis':topic_thesis,
		'trendingbar':False,
		'topicinfo':True,
	}

	return render(request, 'article_display.html', context)








def concensus(request):
	rssDict = request.session['rssDict']
	maintopics = request.session['maintopics']

	checkedArticles = request.POST.getlist('comparisonBox') #returns a list of the titles selected by checkbox


	def articleComparison(checkedArticles):
		alist = []
		for i in range(len(checkedArticles)):
			article = checkedArticles[i]
			dictionary = rssDict[checkedArticles[i]]
			#get summary
			webtext = webscrape2.init(dictionary[0])
			summary,thesissent = textrank.init(webtext)
			dictionary.append(summary)
			dictionary.append(thesissent)

			alist.append(dictionary)
		return alist
	dictList = articleComparison(checkedArticles)
	#get similarity score of specific sentences with in the articles being compared and display the most similar and different ones
	#knn for other recomended articles
	# fact check
	#similarity to entire topic corpus
	#querry google for facts / similarity
	#trending rating

	article0data = dictList[0]
	article1data = dictList[1]


	context = {
		'checkedArticles':checkedArticles,
		'article0data':article0data,
		'article1data':article1data,

		
	}
	return render(request, "concensus.html", context)









def organize_articles(request):
	newsDictByArticle = request.session['newsDictByArticle']
	newsDictByCorpus = request.session['newsDictByCorpus']
	sortby = ''
	def search():
		if 'sortby' in request.GET:
			x = request.GET['sortby']
		else:
			x = 'Form is empty'
		return x
	sortby = search()
	print(sortby)

	Desired_Dict = {}

#ORGANIZE BY SOURCE
	sources = ['CNN', 'NYT', 'Fox']
	if sortby in sources:
		for k,v in newsDictByArticle.items():
			if v[2] == sortby:
				Desired_Dict[k] = v
	else:
		for k,v in newsDictByArticle.items():
			if sortby in v[4]:
				Desired_Dict[k] = v

	data = {
		'title':sortby,
        'newsdata': Desired_Dict,
    }

	return render(request, 'article_display.html', data)




def newstree(request):
	newsDictByArticle = request.session['newsDictByArticle']
	newsDictByCorpus = request.session['newsDictByCorpus']


	TrendingTopics = newsDictByCorpus['TrendingTopics']
	allbigrams = newsDictByCorpus['Bigrams']
	similarity = w2v.init_word2vec_newstree(newsDictByArticle, TrendingTopics, allbigrams)


	context = {
		'trendingtopics':TrendingTopics,
	}
	return render(request, "newstree.html", context)


def graphics(request):





	context = {
		
	}
	return render(request, "graphics.html", context)







