
from __future__ import unicode_literals
from django.shortcuts import render
import django

from django.db import models

from django.shortcuts import render

from django.http import Http404



import sys
import os
import csv
import datetime
import pandas as pd

pathsfile =  os.path.dirname(os.path.abspath('src/Pathsfile.py'))
sys.path.insert(0, pathsfile)
import Pathsfile as pf 


sys.path.insert(0, pf.path_SigmaSource)
sys.path.insert(0, pf.path_Sentiment)
sys.path.insert(0, pf.path_textAnalytics)
sys.path.insert(0, pf.path_textRetrieval)

import textrank_summarization as textrank
import lsa_summarization as lsa_sum
import gensim_summarization as gensim_sum
import textrank_summarization as textrank_sum
import NewsRSS as news
import ScrapeWebText as webscrape

def text_homepage(request):
	time = datetime.datetime.now()

	context = {
		'time':time

	}

	return render(request, 'text_homepage.html', context)



def summarization(request):
	context = {


	}

	return render(request, 'summarization.html', context)



def sumdisp(request):
	def search():
		if 'textbox' in request.GET:
			x = request.GET['textbox']
		else:


			x = 'Form is empty'
		return x
	usertext = search()
	sumtype = request.GET.get('checkbox')
	output = ''

	if sumtype == 'Gensim':
		output = gensim_sum.init(usertext)
	elif sumtype == 'LSA':
		output = lsa_sum.init(usertext)
	elif sumtype == 'TextRank':
		output = textrank_sum.init(usertext)


	context = {
		'output':output,
		'usertext':usertext

	}

	return render(request, 'sumdisp.html', context)




def sentanal(request):
	context = {


	}

	return render(request, 'sentimentanalysis.html', context)

