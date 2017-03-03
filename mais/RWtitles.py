import requests
from bs4 import BeautifulSoup
import re
# https://www.dataquest.io/blog/web-scraping-tutorial-python/
def get_titles(weblink):
	page = requests.get(weblink)
	soup = BeautifulSoup(page.content, 'html.parser')
	title_items = soup.select('h4.artifact-title a')
	title_names = [i.get_text() for i in title_items]
	return title_names

p1titles = get_titles("https://digital.lib.washington.edu/researchworks/handle/1773/20063/browse?rpp=20&sort_by=2&type=dateissued&offset=0&etal=-1&order=ASC")
p2titles = get_titles("https://digital.lib.washington.edu/researchworks/handle/1773/20063/browse?rpp=20&sort_by=2&type=dateissued&offset=20&etal=-1&order=ASC")

web_titles = p1titles + p2titles

# print(len(web_titles))


def get_alpha_titles(titleslist):
	alpha_t = []
	for i in titleslist:
		strlist = re.findall(r"[\w']+", i)
		strwt = ' '.join(strlist)
		alpha_t.append(strwt)
	return alpha_t


import csv
def load_csv_titles(filename):
	with open(filename, 'r', encoding='utf-8') as file:
		# create empty array to hold each entry as a dict
		data = []
		
		# create a csv-reader object
		reader = csv.DictReader(file)
		
		# loop through each row in the csv-reader object...
		for row in reader:
			
			data.append(row['title'])

	return data

csv_titles = load_csv_titles('./data/mais.csv')

alpha_wt = get_alpha_titles(web_titles)
alpha_ct = get_alpha_titles(csv_titles)

missing_titles = []
for i in alpha_wt:
	if i not in alpha_ct:
		missing_titles.append(i)
# print(missing_titles)



# def find_titles(weblink,missing_titles):
def get_web_info(weblink):
	page = requests.get(weblink)
	soup = BeautifulSoup(page.content, 'html.parser')
	
	title_items = soup.select('h4.artifact-title a')
	title_names = [i.get_text() for i in title_items]
	
	link_items = soup.select('h4.artifact-title a[href]')
	link_text = [i['href'] for i in link_items]
	full_link_text = ['https://digital.lib.washington.edu'+i for i in link_text]

	au_items = soup.select('div.artifact-info')
	au_text = [i.get_text() for i in au_items]
	alphanum_au = get_alpha_titles(au_text)
	aulist_list = [re.findall('[%A-Za-z]+', i) for i in alphanum_au]

	keys = ['title','link','author']
	values = list(zip(title_names,full_link_text,aulist_list))
	web_info = [dict(zip(keys, v)) for v in values]
	return web_info
print(get_web_info("https://digital.lib.washington.edu/researchworks/handle/1773/20063/browse?rpp=20&sort_by=2&type=dateissued&offset=0&etal=-1&order=ASC"))