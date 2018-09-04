from django import template

register = template.Library()

import os
import sys
pathsfile =  os.path.dirname(os.path.abspath('src/Pathsfile.py'))
sys.path.insert(0, pathsfile)
import Pathsfile as pf 

import NewsRSS as news 
import ScrapeWebText as webscrape 


sys.path.insert(0, pf.path_SigmaSource)
sys.path.insert(0, pf.path_Sentiment)
sys.path.insert(0, pf.path_textAnalytics)
sys.path.insert(0, pf.path_textRetrieval)


import textrank_summarization as textrank



@register.filter()
def coffee(value,arg="muted"): 
	webtext = webscrape.init(link)
	out = textrank.init(webtext)
	return '<p>MICHAEL</p>'