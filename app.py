from bs4 import BeautifulSoup as bs
from alchemyapi import AlchemyAPI
import time
from operator import itemgetter
import requests
import itertools
import code
import wikipedia
#import indicoio

##### SET UP URLS #####
alchemyapi = AlchemyAPI()
BASE_URL = 'https://en.wikipedia.org'

def setup(query):	
	try:
		page = wikipedia.page(query, auto_suggest=True)
	except Exception as e:
		print(e)
	origin_url = page.url
	title = page.title
	r = requests.get(origin_url)
	soup = bs(r.text)
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
	return (title, origin_url, urls, count) # count is num of links. By our assumption,
									 # it is limited at 30 for time constraint.

##### RANKING LINKS #####

def rank_links(origin_url, urls, count):
	origin_keywords = [word['text'] for word in alchemyapi.keywords('url', origin_url)['keywords']]
	output = []
	link_lst = []
	keyw_list = []
	rank = dict()
	for url in urls:
		try:
			count1 = 0
			r = requests.get(url)
			soup1 = bs(r.text)
			links = [BASE_URL + a['href'] for a in soup1.select('p a') if '#' not in a['href']]
			f = lambda x: 1 if x in urls else 0
			count1 += sum(f(x) for x in links)
			keywords = [word['text'] for word in alchemyapi.keywords('url', url)['keywords'] if word['text'] in origin_keywords]
			link_score = float(count1)/float(count)
			keyw_score = float(len(keywords))/float(len(origin_keywords))
			value = link_score + keyw_score
			title = soup1.title.text[:-35]
			summary = wikipedia.summary(title, sentences=1, auto_suggest=True)
			rank[url] = (title, value, summary, link_score, keyw_score, url)
		except:
			pass
	sorted_rank = sorted(rank.values(), key=itemgetter(1), reverse=True)
	max_val = sorted_rank[0][1]
	for i in sorted_rank[:8]:
		output.append((i[0], i[1]/max_val, i[2], i[5]))
		link_lst.append(i[3])
		keyw_list.append(i[4])
	return output, link_lst, keyw_list

#code.interact(local=locals())

def main():
	start=time.time()
	title, origin_url, urls, count = setup('bush')
	print(rank_links(origin_url, urls, count)[0])
	end=time.time()
	print('time: {}'.format(end-start))

if __name__ == '__main__':
	main()