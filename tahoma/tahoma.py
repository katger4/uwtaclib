#! python3
import re
import csv

# instructions to prepare text files prior to code implementation: copy the table of contents text from the tahoma west pdf into a blank txt document. in this case, it was easiest to format two txt files, one containing alternating lines (title /n genre) and the other (author /n fpage). ensure authors with middle names stay on one line, double check special character translation in titles/author names.

# functions to extract even and odd lines separately from text files http://stackoverflow.com/questions/18047381/separate-odd-and-even-lines-in-a-generator-with-python
def oddlines(filename):
	odds = []
	f = open(filename)
	for index,line in enumerate(f):
		if index % 2:
			stripped_line = line.rstrip()
			odds.append(stripped_line)
	low_odds = [i.lower() for i in odds]
	low_odds = [w.replace('visual arts', 'visual-arts') for w in low_odds]
	return low_odds

def evenlines(filename):
	evens = []
	f = open(filename)
	for index,line in enumerate(f):
		if not index % 2:
			stripped_line = line.rstrip()
			evens.append(stripped_line)
	return evens
	# return (line for index,line in enumerate(fileobj) if not index % 2)

####################################################
# obtain a list of each of the following fields from the 2 txt files
authors = evenlines('aupg.txt')
fpages = oddlines('aupg.txt')
genres = oddlines('titgen.txt')
titles = evenlines('titgen.txt')

# convert fpage values to int type for sorting
fpages = [int(i) for i in fpages]
# determine the final page of the last entry from the pdf
finalpage = 93
# add the final page to the first page list
fpages.append(finalpage)
# create a list of last pages by subtracting 1 from each subsequent first page (remove the first first page after this bc it will just be zero)
lpages = [i - 1 for i in fpages]
lpages.remove(0)

# remove the fake finalpage (here, 92)
lpages.pop(-1)
# and append the real finalpage
lpages.append(finalpage)

# remove the final page that was added to the fpages list
fpages.pop(-1)

# split up the full author names into first, middle, and last name lists (middle names will be blank "" if no middle name listed)
fnames = []
mnames = []
lnames = []
for i in authors:
	namelist = i.split(" ")
	if len(namelist) == 2:
		fnames.append(namelist[0])
		mnames.append("")
		lnames.append(namelist[1])
	else:
		fnames.append(namelist[0])
		mnames.append(namelist[1])
		lnames.append(namelist[2])	

# create the list of fulltext_url's using the titles list and removing special characters, replacing whitespace with '_'
fulltext_url = []
lname_title = list(zip(lnames, titles))
for i in lname_title:
	alphatitle = re.sub("[^a-zA-Z\s]+", "", i[1])
	wordlist = alphatitle.split(" ")
	titlecombo = '_'.join(wordlist)
	url = '*\\2016_TW_'+i[0]+'_'+titlecombo+'.pdf'
	fulltext_url.append(url)

# print(len(lnames))
# print(len(mnames))
# print(len(fnames))

# link up all generated lists using the zip function
values = list(zip(titles, fulltext_url, fnames, mnames, lnames, genres, fpages, lpages))
# print(values[1])

# create a list of dicts (where each row is a dict) using headers as keys and values as list entries using zip
headers = ['title', 'fulltext_url', 'author1_fname', 'author1_mname', 'author1_lname', 'document_type', 'fpage', 'lpage']
data = []
for i in values:
	row = dict(zip(headers, i))
	data.append(row)
# print(data[1])
####################################################

# write each dict as a row in a csv called 'test.csv' (rename as necessary), using the full list of header values and the required encoding to translate unicode to excel-readable text
def write(data):
# with open(output, 'w') as output_file: 
	fieldnames = ["title", "fulltext_url", "keywords", "abstract", "author1_fname", "author1_mname", "author1_lname", "author1_suffix", "author1_email", "author1_institution", "author2_fname", "author2_mname", "author2_lname", "author2_suffix", "author2_email", "author2_institution", "author3_fname", "author3_mname", "author3_lname", "author3_suffix", "author3_email", "author3_institution", "author4_fname", "author4_mname", "author4_lname", "author4_suffix", "author4_email", "author4_institution", "disciplines", "cover_paste", "document_type", "erratum", "fpage", "lpage", "peer_reviewed"]
	with open('test.csv', 'w', encoding='WINDOWS-1252') as output_file: 
	# encoding needed to write unicode characters as excel preferred encoding (http://stackoverflow.com/questions/6588068/which-encoding-opens-csv-files-correctly-with-excel-on-both-mac-and-windows)
		dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames) # , dialect='excel'
		dict_writer.writeheader()
		dict_writer.writerows(data)
####################################################
write(data)
####################################################