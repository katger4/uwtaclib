import requests
from bs4 import BeautifulSoup
import re
import csv

# https://www.dataquest.io/blog/web-scraping-tutorial-python/


def get_alphanum_text(any_list):
    alphanum_list = []
    for i in any_list:
        strlist = re.findall(r"[\w']+", i)
        strwt = ' '.join(strlist)
        alphanum_list.append(strwt)
    return alphanum_list

def get_authors(weblink):
    page = requests.get(weblink)
    soup = BeautifulSoup(page.content, 'html.parser')
    au_items = soup.select('div.artifact-info')
    au_text = [i.get_text() for i in au_items]
    alphanum_au = get_alphanum_text(au_text)
    aulist_list = [re.findall('[%A-Za-z]+', i) for i in alphanum_au]
    authors = [[i[0],i[1]] for i in aulist_list]
    return authors

p1au = get_authors("https://digital.lib.washington.edu/researchworks/handle/1773/20063/browse?rpp=20&sort_by=2&type=dateissued&offset=0&etal=-1&order=ASC")
p2au = get_authors("https://digital.lib.washington.edu/researchworks/handle/1773/20063/browse?rpp=20&sort_by=2&type=dateissued&offset=20&etal=-1&order=ASC")
web_aus = p1au + p2au
#web_aus

def load_csv_aus(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        # create empty array to hold each entry as a dict
        data = []
        # create a csv-reader object
        reader = csv.DictReader(file)
        # loop through each row in the csv-reader object...
        for row in reader:
            author = [row['author1_lname'],row['author1_fname']]
            data.append(author)
    return data

csv_aus = load_csv_aus('./data/m.csv')
#csv_aus

missing_au = [i for i in web_aus if i not in csv_aus]
# print(missing_au)
# print(len(missing_au))
# print(len(missing_titles))


def get_web_info(weblink):
    page = requests.get(weblink)
    soup = BeautifulSoup(page.content, 'html.parser')

    title_items = soup.select('h4.artifact-title a')
    title_names = [i.get_text() for i in title_items]
    alpha_titles = get_alphanum_text(title_names)

    link_items = soup.select('h4.artifact-title a[href]')
    link_text = [i['href'] for i in link_items]
    full_link_text = ['https://digital.lib.washington.edu'+i+'?show=full' for i in link_text]

    au_items = soup.select('div.artifact-info')
    au_text = [i.get_text() for i in au_items]
    alphanum_au = get_alphanum_text(au_text)
    aulist_list = [re.findall('[%A-Za-z]+', i) for i in alphanum_au]
    authors = [[i[0],i[1]] for i in aulist_list]

    keys = ['alphatitle','title','link','author','sm_auth']
    values = list(zip(alpha_titles,title_names,full_link_text,aulist_list,authors))
    web_info = [dict(zip(keys, v)) for v in values]
    return web_info

p1 = get_web_info("https://digital.lib.washington.edu/researchworks/handle/1773/20063/browse?rpp=20&sort_by=2&type=dateissued&offset=0&etal=-1&order=ASC")
p2 = get_web_info("https://digital.lib.washington.edu/researchworks/handle/1773/20063/browse?rpp=20&sort_by=2&type=dateissued&offset=20&etal=-1&order=ASC")
web_info = p1 + p2

missing_info2 = [i for i in web_info if i['sm_auth'] in missing_au]

def get_dc_info(weblink):
    page = requests.get(weblink)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find("table", attrs={"class":"ds-includeSet-table detailtable table table-striped table-hover"})
    #table_rows = table.find_all("tr")
    table_heads = [h.get_text() for h in table.find_all("td", attrs={'class':'label-cell'})]
    table_info = [i.get_text() for i in table.find_all("td", attrs={'class':'word-break'})]
    # if do dict zip, removes duplicate keys! so get a list of tuple
    all_heads_info = list(zip(table_heads,table_info))
    # then create a new dict where each value is a list
    dict_heads_info = {}
    for x, y in all_heads_info:
        dict_heads_info.setdefault(x, []).append(y)
    # then, flatten 1 item lists
    for k,v in dict_heads_info.items():
        if len(v) == 1:
            dict_heads_info[k] = v[0]
            #print(v)
    return dict_heads_info
# get_dc_info('https://digital.lib.washington.edu/researchworks/handle/1773/38049?show=full')

def create_ex_data(missing_info):
    spreadsheet = []
    for row in missing_info:
        full_info = get_dc_info(row['link'])
        ex_row = {}

        ex_row['title'] = row['title']
        ex_row['author1_fname'] = row['author'][1]
        if len(row['author']) == 3:
            ex_row['author1_mname'] = row['author'][2]
        else:
            ex_row['author1_mname'] = ''
        ex_row['author1_lname'] = row['author'][0]
        ex_row['author1_institution'] = 'University of Washington Tacoma'
        ex_row['author1_email'] = ''
        ex_row['fulltext_url'] = full_info['dc.identifier.uri']
        ex_row['author1_suffix'] = ''
        ex_row['season'] = ''
        ex_row['comments'] = ''
        ex_row['degree_name'] = 'Master of Arts in Interdisciplinary Studies (MAIS)'
        ex_row['abstract'] = full_info['dc.description.abstract']
        ex_row['publication_date'] = full_info['dc.date.accessioned']
        ex_row['department'] = 'Interdisciplinary Arts and Sciences'

        if '1 year' in full_info['dc.embargo.terms']:
            ex_row['document_type'] = 'restrict_1yr'
        elif '2 years' in full_info['dc.embargo.terms']:
            ex_row['document_type'] = 'restrict_2yr'
        elif '5 years' in full_info['dc.embargo.terms']:
            ex_row['document_type'] = 'restrict_5yr'
        else:
            ex_row['document_type'] = 'open_access'

        if 'dc.embargo.lift' in full_info:
            ex_row['date_avail'] = full_info['dc.embargo.lift']
        else:
            ex_row['date_avail'] = ''

        if isinstance(full_info['dc.contributor.advisor'], str):
            #for name in full_info['dc.contributor.advisor']:
            namelist = full_info['dc.contributor.advisor'].split(', ')
            ex_row['advisor1'] = namelist[1]+' '+namelist[0]
            ex_row['advisor2'] = ''
            ex_row['advisor3'] = ''
            ex_row['advisor4'] = ''
        elif len(full_info['dc.contributor.advisor']) == 2:
            names = full_info['dc.contributor.advisor']
            namelist1 = names[0].split(', ')
            #print(full_info['dc.contributor.advisor'])
            ex_row['advisor1'] = namelist1[1]+' '+namelist1[0]
            namelist2 = names[1].split(', ')
            ex_row['advisor2'] = namelist2[1]+' '+namelist2[0]
            ex_row['advisor3'] = ''
            ex_row['advisor4'] = ''
        elif len(full_info['dc.contributor.advisor']) == 3:
            names = full_info['dc.contributor.advisor']
            namelist1 = names[0].split(', ')
            ex_row['advisor1'] = namelist1[1]+' '+namelist1[0]
            namelist2 = names[1].split(', ')
            ex_row['advisor2'] = namelist2[1]+' '+namelist2[0]
            namelist3 = names[2].split(', ')
            ex_row['advisor3'] = namelist3[1]+' '+namelist3[0]
            ex_row['advisor4'] = ''
        elif len(full_info['dc.contributor.advisor']) == 4:
            names = full_info['dc.contributor.advisor']
            namelist1 = names[0].split(', ')
            ex_row['advisor1'] = namelist1[1]+' '+namelist1[0]
            namelist2 = names[1].split(', ')
            ex_row['advisor2'] = namelist2[1]+' '+namelist2[0]
            namelist3 = names[2].split(', ')
            ex_row['advisor3'] = namelist3[1]+' '+namelist3[0]
            namelist4 = names[3].split(', ')
            ex_row['advisor4'] = namelist4[1]+' '+namelist4[0]

        if full_info['dc.type'] == 'Thesis':
            ex_row['work_type'] = 'Masters Thesis'
        else:
            ex_row['work_type'] = 'Masters Capstone Project'

        if isinstance(full_info['dc.subject'], str):
            ex_row['keywords'] = full_info['dc.subject'].replace(';',',')
            #print(ex_row['keywords'])
        else:
            #print(full_info['dc.subject'].type())
            ex_row['keywords'] = ', '.join(full_info['dc.subject'])


        if 'interdisciplinary arts and sciences - tacoma' in full_info['dc.subject.other']:
            full_info['dc.subject.other'].remove('interdisciplinary arts and sciences - tacoma')
            ex_row['disciplines'] = '; '.join(full_info['dc.subject.other'])
        elif 'Interdisciplinary arts and sciences - Tacoma' in full_info['dc.subject.other']:
            full_info['dc.subject.other'].remove('Interdisciplinary arts and sciences - Tacoma')
            ex_row['disciplines'] = '; '.join(full_info['dc.subject.other'])
        else:
            ex_row['disciplines'] = '; '.join(full_info['dc.subject.other'])

        spreadsheet.append(ex_row)
    return spreadsheet

spreadsheet = create_ex_data(missing_info2)

def write(data, output):
    fieldnames = ['title', 'publication_date', 'season', 'document_type', 'date_avail', 
              'work_type', 'degree_name', 'department', 'advisor1', 'advisor2',
              'advisor3', 'advisor4', 'keywords', 'disciplines', 'abstract', 
              'comments', 'fulltext_url', 'author1_fname', 'author1_mname', 'author1_lname', 
              'author1_suffix', 'author1_email', 'author1_institution']
    with open(output, 'w', newline='',encoding='utf-8-sig') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows(data)

write(spreadsheet, './data/mais_update.csv')
