from bs4 import BeautifulSoup as bs
from alchemyapi import AlchemyAPI
import time
from operator import itemgetter
import requests
import itertools
import code
import wikipedia

##### SET UP URLS #####

def setup(query):
	alchemyapi = AlchemyAPI()
	while 
	try:
		page = wikipedia.page(query, auto_suggest=True)
		found = True
	except Exception as e:
		print(e)
	origin_url = page.url
	r = requests.get(origin_url)

	soup = bs(r.text)
	BASE_URL = 'https://en.wikipedia.org'

urls, count = set(), 0
p_a = soup.select('p a')
div_a = soup.select('div[class~=hatnote] a')
for lst in [p_a, div_a]:
	for a in lst:
		count += 1
		if '#' not in a['href']:
			urls.add(BASE_URL + a['href'])
		if count > 30:
			break

##### RANKING LINKS #####

def rank_links():
	origin_keywords = [word['text'] for word in alchemyapi.keywords('url', origin_url)['keywords']]
	output = []
	rank = dict()
	for url in urls:
		count1 = 0
		r = requests.get(url)
		soup1 = bs(r.text)
		links = [BASE_URL + a['href'] for a in soup1.select('p a') if '#' not in a['href']]
		f = lambda x: 1 if x in urls else 0
		count1 += sum(f(x) for x in links)
		keywords = [word['text'] for word in alchemyapi.keywords('url', url)['keywords'] if word['text'] in origin_keywords]
		value = count1/count + float(len(keywords))/float(len(origin_keywords))
		title = soup1.title.text[:-35]
		summary = wikipedia.summary(title, sentences=1, auto_suggest=True)
		rank[url] = (title, value, summary)
	sorted_rank = sorted(rank.values(), key=itemgetter(1), reverse=True)
	c = 0
	max_val = sorted_rank[0][1]
	for i in sorted_rank:
		output.append((i[0], i[1]/max_val, i[2]))
	return output

#code.interact(local=locals())

def main():
	setup()
	rank_links()

if __name__ == '__main__':
	main()