import re
import csv
from titlecase import titlecase

# this python3 script takes in the Zotero export generated csv of all BOOK publications and outputs a csv using the headers and text formatting necessary for upload to digital commons

###### WILL ONLY WORK if each author name is in "last name, first name" format when exported from Zotero ######

# NOTE: since Zotero lacks some fields that we require, some 'dummy' categories are used to store information in Zotero (if they are left blank, the script will still run). in order to utilize this script most effectively (and to reduce the amount of manual entry required), make use of the following fields in Zotero (see Anne Bartlett's books in Zotero/SIAS for an example):

	# 1. URL - this field should contain the link to the e-book version of this book in the UW libraries (if available)
	# 2. Archive - this field should contain the link to the cover image of this book (if available)
	# 3. Loc. in Archive - this field should contain the link to the print copy of this book in the UW libraries (if available)
	# 4. Library Catalog - this field should contain the location of the print copy of the book in the UW Libraries (e.g. 'UW Tacoma Library Faculty Publications' or 'Summit libraries')
	# 5. Call Number - if the print copy of this book is in the UW Libraries, this field should contain its call number (e.g. 'PR275.R4 B37 1995')
	# 6. Rights - this field should contain the link to purchase a copy of this book (if available)
	# 7. Extra - this field should contain a comma separated list of keywords (if available)

# NOTE: the output csv should be opened in Excel and scanned for errors (manually formatting dates to be in yyyy-mm-dd format if all date fields are present, if just yyyy - do not re-format), then saved as a '.xls' file (NOT '.xlsx')

###############################################################################

# this function takes in the Zotero-export csv, represents the content as a list of python dictionaries, a.k.a. 'dicts', (where headers are keys and row-content is each value), then changes the Zotero generated headers to DC headers. then, Zotero-generated content for the 'document_type' field is converted to the DC-mandated style, allowing for conditional content creation based on the document type (e.g. whether to create_openurl and special field manipulation for reports/presentations). then, conditionally edit the content of specific header-values (e.g. publication titles --> titlecase, splitting up the page ranges into two separate columns, formatting dates), update the dict with these new values, remove dummy columns, and add each new row (as a dict) to the list of dicts called 'data' 
def load_file(filename):
	# open the Zotero export as a file object (note the utf-8 encoding to properly read the text encoding of the zotero output)
	with open(filename, 'r', encoding='utf-8') as file:
		# create empty array to hold each entry as a dict
		data = []
		
		# create a csv-reader object
		reader = csv.DictReader(file)
		
		# loop through each row in the csv-reader object...
		for row in reader:

			newrow = convert_headers(row)						
			
			newcontent = edit_content(newrow)

			# update the dict with the newly edited values
			newrow.update(newcontent)
			
			# remove extra columns
			newrow.pop('automatic tags')
			newrow.pop('library catalog')		
			newrow.pop('call number')
			newrow.pop('archive location')
			# append the formatted dict (a row in the csv) to the full data list
			data.append(newrow)

	return data

################### begin load_file helper functions #########################
def convert_headers(row):
	# iterate through each entry in the csv, convert headers (keys) to lowercase
	newrow = {k.lower():v for k, v in row.items()}

	# then change the names of the headers from Zotero --> UWT style
	newrow['abstract'] = newrow.pop('abstract note')
	newrow['publication_date'] = newrow.pop('date')
	newrow['identifier'] = newrow.pop('isbn')
	newrow['city'] = newrow.pop('place')
	# source_fulltext_url points to e-book; 'archive location' points to print copy
	newrow['source_fulltext_url'] = newrow.pop('url')
	newrow['buy_link'] = newrow.pop('rights')
	newrow['cover_image_url'] = newrow.pop('archive')
	newrow['title'] = newrow.pop('\ufeff"title"')
	newrow['keywords'] = newrow.pop('extra')	
	
	return newrow

def edit_content(newrow):
	# create an empty dict to store the edited content
	newcontent = {} 
	for k, v in newrow.items():
		
		# use the dummy Zotero fields 'library catalog', 'archive location', and 'call number' to create the text for the 'library_location' field (only works if the 'library catalog' field is filled in)
		if k == 'library catalog':
			if v != '':
				newcontent['library_location'] = '<p><a href="'+newrow['archive location']+'"><strong>Location: '+newrow['library catalog']+' - '+newrow['call number']+'</strong></a></p>'

		# convert case (uses titlecase module)
		elif k == 'publisher':
			if v != '':
				newcontent['publisher'] = titlecase(v)

		elif k == 'title':
			if v != '':
				newcontent['title'] = titlecase(v)

		# find and replace semicolon separators in keywords column with commas, then save this list as the keywords value
		elif k == 'keywords':
			if v != '':
				cs = v.replace(';', ',')
				newcontent['keywords'] = cs
		
		# find and replace semicolon separators in keywords column with commas, then save this list as the keywords value
		elif k == 'automatic tags':
			if v != '':
				cs = v.replace(';', ',')
				newcontent['keywords'] = cs

		# if the date format is yyyy-mm NOT yyyy or yyyy-mm-dd or NONE, add in '-01' to complete the date for excel readability
		elif k == 'publication_date':
			# print(v)
			yr_mon = re.match(r'\d{4}-\d{2}(?!-)', v)
			if yr_mon != None:
				# print(yr_mon)
				dash = re.sub(r'(\d{4}-\d{2})(?!-)', r'\1-01', v)
				newcontent['publication_date'] = dash	
	return newcontent
################### end load_file helper functions #########################

# takes in the modified list of dicts from the 'load_file' function, iterates through each row/dict in the list, formats author names as a list of names using the helper functions below, then extends the list of names with empty strings so that the length of the names list matches the length of the author name headers, then zip the headers and author names as key-value pairs in order to update the row/dict with the new fields
def get_names(data):
	for row in data:
		names_list = parse_names(row)

		author_headers = ['author1_fname', 'author1_mname', 'author1_lname', 'author1_suffix', 'author1_email', 'author1_institution', 'author1_is_corporate', 'author2_fname', 'author2_mname', 'author2_lname', 'author2_suffix', 'author2_email', 'author2_institution', 'author2_is_corporate', 'author3_fname', 'author3_mname', 'author3_lname', 'author3_suffix', 'author3_email', 'author3_institution', 'author3_is_corporate', 'author4_fname', 'author4_mname', 'author4_lname', 'author4_suffix', 'author4_email', 'author4_institution', 'author4_is_corporate', 'author5_fname', 'author5_mname', 'author5_lname', 'author5_suffix', 'author5_email', 'author5_institution', 'author5_is_corporate', 'author6_fname', 'author6_mname', 'author6_lname', 'author6_suffix', 'author6_email', 'author6_institution', 'author6_is_corporate', 'author7_fname', 'author7_mname', 'author7_lname', 'author7_suffix', 'author7_email', 'author7_institution', 'author7_is_corporate', 'author8_fname', 'author8_mname', 'author8_lname', 'author8_suffix', 'author8_email', 'author8_institution', 'author8_is_corporate', 'author9_fname', 'author9_mname', 'author9_lname', 'author9_suffix', 'author9_email', 'author9_institution', 'author9_is_corporate']

		
		auth_tuples = []
		
		dif = len(author_headers) - len(names_list)
		empty = ['']*dif
		names_list.extend(empty)
		
		if len(names_list) == len(author_headers):
			z = list(zip(author_headers,names_list))
			auth_tuples.extend(z)
		else: 
			print("Too many authors!")
			break

		# print(auth_tuples[0])
		d = dict(auth_tuples)

		row.update(d)
		row.pop('author')
		# print(d['author1_fname']+" "+d['author2_fname']+" "+d['author3_fname'])

	# print(data[0])
	return data

# this is a helper function, called in the "get_names" function above
# author name lists are exported from Zotero come in the form: "Hampson, Sarah; Simien, Evelyn M.; Kelly, Kristin; Huff, Jamie Cote", and need to be split up into separate columns for each firstname, middlename, and lastname. uwt affiliation/email addresses are added for one UWT author via the label_tac_author helper function below
###### WILL ONLY WORK if each author name is in "last name, first name" format when exported from Zotero ######
def parse_names(row):
	# split the csv row/dict category 'author' into a list of individual author names (e.g. ["Hampson, Sarah", "Simien, Evelyn M.", "Kelly, Kristin", "Huff, Jamie Cote"])	
	nl = re.split("; ", row['author'])

	names_list = []
	
	# for each name in the list of all author names, split the name into "last name", "first name [middle initial, if there]" (e.g. ["Hampson", "Sarah"] or ["Simien", "Evelyn M."])
	for i in nl:
		name = re.split(", ", i)

		last = name[0]
		firstmid = name[1]
		fmlist = re.split("\s", firstmid)
		
		# print(len(fmlist))
		# print(fmlist)
		
		if len(fmlist) > 1:
			first = fmlist[0]
			mid = fmlist[1]
			fullname = [first,mid,last,"","","",""]
			tac_name = label_tac_author(fullname, uwt_name, uwt_email)
			# fullname = (first,mid,last,"","","","")
			names_list.extend(tac_name)
		else:
			first = fmlist[0]
			# mid = ""
			# fullname = (first,mid,last,"","","","")
			fullname = [first,"",last,"","","",""]
			tac_name = label_tac_author(fullname, uwt_name, uwt_email)
			names_list.extend(tac_name)

	return names_list

# this is a helper function, called in the 'parse_names' function above, and works best when only 1 UWT author's publications are being processed in the csv (other UWT author's affiliation/email will need to be manually entered otherwise)
# this function takes in the UWT author's name and email address (input by the user), as well as the list of author names from the Zotero export, partially processed in parse_names, then adds the input email address and UWT affiliation to each author to each name partially matching the input UWT author name (only the first initial and lastname must match)
def label_tac_author(fullname, uwt_name, uwt_email):
	# create a 3 item list from the input author name, using a blank space placeholder for the middle initial if none provided
	uwt_list = uwt_name.split()
	if len(uwt_list) == 2:
		uwt_list.insert(1, '')

	# if the first letter of the first name in each list matches and the last name in each list matches, add the UWT email address and institution fields
	if fullname[0][0] == uwt_list[0][0] and fullname[2] == uwt_list[2]:
		fullname[4] = uwt_email
		fullname[5] = "University of Washington Tacoma"
	# print(fullname)
	return fullname

# use the dictwriter function from the csv module to export the list of dicts as a csv using the headers/fieldnames list and a character encoding that can be read by excel
# NOTE: if terminal ouputs a weird utf-8 error, then some extreme character has been encoded by zotero, and manual utf-8 characters will need to be loaded by excel separately
def write(data, output):
	# keys below outputs header row in random order
	#keys = data[0].keys()
	# specifying fieldnames below outputs header row in exact order
	fieldnames = ['title', 'publisher', 'identifier', 'abstract', 'publication_date', 'city', 'library_location', 'fulltext_url', 'buy_link', 'cover_image_url', 'source_fulltext_url', 'keywords', 'author1_fname', 'author1_mname', 'author1_lname', 'author1_suffix', 'author1_email', 'author1_institution', 'author1_is_corporate', 'author2_fname', 'author2_mname', 'author2_lname', 'author2_suffix', 'author2_email', 'author2_institution', 'author2_is_corporate', 'author3_fname', 'author3_mname', 'author3_lname', 'author3_suffix', 'author3_email', 'author3_institution', 'author3_is_corporate', 'author4_fname', 'author4_mname', 'author4_lname', 'author4_suffix', 'author4_email', 'author4_institution', 'author4_is_corporate', 'author5_fname', 'author5_mname', 'author5_lname', 'author5_suffix', 'author5_email', 'author5_institution', 'author5_is_corporate', 'author6_fname', 'author6_mname', 'author6_lname', 'author6_suffix', 'author6_email', 'author6_institution', 'author6_is_corporate', 'author7_fname', 'author7_mname', 'author7_lname', 'author7_suffix', 'author7_email', 'author7_institution', 'author7_is_corporate', 'author8_fname', 'author8_mname', 'author8_lname', 'author8_suffix', 'author8_email', 'author8_institution', 'author8_is_corporate', 'author9_fname', 'author9_mname', 'author9_lname', 'author9_suffix', 'author9_email', 'author9_institution', 'author9_is_corporate']
	# encoding specification converts utf-8 to excel readable format
	with open(output, 'w', encoding='WINDOWS-1252') as output_file:
		dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames, dialect='excel')
		dict_writer.writeheader()
		dict_writer.writerows(data)

###############################################################################

# get data from user and run each function
filename = input("Enter the Zotero-export filename: ")
data = load_file(filename)
print("loading the file and renaming headers...")
uwt_name = input("Enter the UWT author's name: ")
uwt_email = input("Enter the UWT author's email: ")
print("processing author names...")
names = get_names(data)
output = input("Enter the name of the new file generated: ")
print("writing the new csv file...")
write(names, output)

###############################################################################