#Newspaper3k
from newspaper import Article

def init_news3k(url):
	try:
		article = Article(url)
		article.download()
		html = article.html

		article.parse()
		authors = article.authors
		date = article.publish_date

		fulltext = article.text
		image = article.top_image
		movies = article.movies

		# article.nlp()
		# keywords = article.keywords
		# summary = article.summary

		output = (authors, date, fulltext, image)
	except:
		output = ('null', 'null', 'null', 'null')

	return output
