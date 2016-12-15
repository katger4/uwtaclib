#! python3
# import PyPDF2
import csv
import re
import os

# drag each tahoma west work into a new folder in the cwd IN ORDER based on page number (add a 0 to the first work so the nautral sort will work & make sure there is one file per title), create the tahoma west metadata using the tahoma.py script

# load the csv file containing tahoma west metadata, store that information as a dict
def load_csv(filename):
	with open(filename, 'r', encoding='WINDOWS-1252') as file:
		data = []
		reader = csv.DictReader(file)
		for row in reader:
			data.append(row)
	return data

# create a sorted list of titles (alphabetically), with non-alpha characters removed and spaces replaced with '_', then store the sorted titles in a new list
def get_titles(data):
	title_file_list = []
	for i in data:
		title = i['title']

		alphatitle = re.sub("[^a-zA-Z\s]+", "", title)
		wordlist = alphatitle.split(" ")
		combo = '_'.join(wordlist)
		# title_list.append(combo)
		full_url = i['fulltext_url']
		url = full_url[2:]

		title_file = (combo,url)
		title_file_list.append(title_file)

	# lname_list = []
	# for i in data:
	# 	lname_list.append(i['author1_lname'])

	# lname_title = list(zip(lname_list, title_list))
	
	# title_file_list = []
	# for i in lname_title:
	# 	url = '2016_TW_'+i[0]+'_'+i[1]+'.pdf'
	# 	title_file = (i[1],url)
	# 	title_file_list.append(title_file)


	title_file_list.sort()
	# print(title_list)
	# return num_title

	stitles = []
	# only need this titles for now...
	# for i in num_title[12:-1]:
	for i in title_file_list:
		stitles.append(i[1])
	return stitles
# print(num_title)
####################################################
data = load_csv('test.csv')
# print(data[0])
stitles = get_titles(data)
print(stitles)
####################################################

# using a directory of pdf's named with each title only, create a list of all the current file names, sorted by title, then create a list of new file names using the sorted title list, then iterate through both lists, using 'zip' rename each filein order
def rename_pdfs(root):
	directory = os.listdir(root)

	oldnames = []
	for filename in directory:
		if filename.endswith('.pdf'):
			oldname = os.path.join(root, filename)
			oldnames.append(oldname)
	oldnames.sort()
	print(oldnames)
	newnames = []
	for i in stitles:
		newname = os.path.join(root, i)
		newnames.append(newname)
	# http://stackoverflow.com/questions/37057128/rename-files-from-several-folders-oserror-errno-2-no-such-file-or-directory
	for i, j in zip(oldnames, newnames):
		os.rename(i, j)
####################################################
# rename_pdfs('tw')
####################################################
