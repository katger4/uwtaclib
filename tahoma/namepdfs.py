#! python3
import csv
import re
import os

# drag each tahoma west work into a new folder in the cwd IN ORDER based on page number (add a 0 to the first work so the nautral sort will work & make sure there is one file per title), create the tahoma west metadata using the tahoma.py script

# BE SURE TO COPY THE UNNAMED FILES INTO A SEPARATE FOLDER PRIOR TO RUNNING THIS SCRIPT (there is no 'undo' once files are renamed, so if errors are made you will have to re-drag all the files unless you make backup copies)

# load the csv file containing tahoma west metadata, store that information as a dict
def load_csv(filename):
	with open(filename, 'r', encoding='WINDOWS-1252') as file:
		data = []
		reader = csv.DictReader(file)
		for row in reader:
			data.append(row)
	return data

# create a sorted list of titles (using page numbers as a reference), with non-alpha characters removed and spaces replaced with '_', then store the sorted titles (without corresponding page numbers) in a new list
def get_num_titles(data):
	
	num_title = []
	
	for i in data:
		pg = int(i['fpage'])
		full_url = i['fulltext_url']
		url = full_url[2:]
		title_file = (pg,url)
		num_title.append(title_file)
	
	num_title.sort()
	# print(num_title)
	# return num_title

	stitles = []
	# only need this titles for now...
	# for i in num_title[12:-1]:
	for i in num_title:
		stitles.append(i[1])
	return stitles
# print(num_title)
####################################################
filename = input("Enter the Tahoma West metadata filename: ")
print("loading the file and obtaining filenames...")
data = load_csv(filename)
# data = load_csv('test.csv')
# print(data[0])
stitles = get_num_titles(data)
# print(stitles)
####################################################

# function to sort filenames in a directory using integer values, rather than string sorting http://stackoverflow.com/questions/4836710/does-python-have-a-built-in-function-for-string-natural-sort
def natural_sort(l): 
	convert = lambda text: int(text) if text.isdigit() else text.lower() 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	return sorted(l, key = alphanum_key)

# using a directory of pdf's named 'Tahoma_West_2016_Inside_Final (dragged) 0.pdf' : 'Tahoma_West_2016_Inside_Final (dragged) NUM.pdf', create a list of all the current file names, sorted naturally, then create a list of new file names using the sorted title list, then iterate through both lists, using 'zip' rename each filein order
def rename_pdfs(root):
	directory = os.listdir(root)

	oldnames = []
	for filename in natural_sort(directory):
		if filename.endswith('.pdf'):
			oldname = os.path.join(root, filename)
			oldnames.append(oldname)
	newnames = []
	for i in stitles:
		newname = os.path.join(root, i)
		newnames.append(newname)
	# http://stackoverflow.com/questions/37057128/rename-files-from-several-folders-oserror-errno-2-no-such-file-or-directory
	for i, j in zip(oldnames, newnames):
		os.rename(i, j)
####################################################
directory = input("Enter the folder name containing dragged pdfs: ")
print("sorting the files, renaming according to metadata...")
rename_pdfs(directory)
# rename_pdfs('twb2')
print("files renamed!")
####################################################
