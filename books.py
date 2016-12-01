import re
import csv
from titlecase import titlecase

# this python3 script takes in the Zotero export generated csv of all BOOKs and outputs a csv using the headers and text formatting necessary for upload to digital commons

# NOTE: the output csv should be opened in Excel and scanned for errors, then saved as a '.xls' file (NOT '.xlsx')

###############################################################################
# this function takes in the Zotero-export csv, represents the content as a list of python dicts (where headers are keys and row-content is each value), then changes the Zotero generated headers to DC headers. then, conditionally edit the content of specific header-values (e.g. publication titles --> titlecase, splitting up the page ranges into two separate columns, formatting dates), update the dict with these new values, remove dummy columns, and add each new row (as a dict) to the list of dicts called 'data' 
def load_file(filename):
	# see baby-names for os stuff files_list = os.listdir(directory)
	with open(filename, 'r', encoding='utf-8') as file:
		# create empty array to hold each entry as a dict
		data = []

		reader = csv.DictReader(file)
		
		for row in reader:
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
			#newrow['library_location'] = newrow.pop('library catalog')

			# create a new blank dict to conditionally edit the values of some headers before updating the original dict with these new values
			newcontent = {} 
			for k, v in newrow.items():
				
				# use the dummy Zotero fields 'library catalog', 'archive location', and 'call number' to create the text for the 'library_location' field
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
				elif k == 'automatic tags':
					if v != '':
						cs = v.replace(';', ',')
						newcontent['keywords'] = cs

				# if the date format is yyyy-mm NOT yyyy or yyyy-mm-dd or NONE, add in '-01' to complete the date
				elif k == 'publication_date':
					# print(v)
					yr_mon = re.match(r'\d{4}-\d{2}(?!-)', v)
					if yr_mon != None:
						# print(yr_mon)
						dash = re.sub(r'(\d{4}-\d{2})(?!-)', r'\1-01', v)
						newcontent['publication_date'] = dash						
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
	
	nl = re.split("; ", row['author'])

	names_list = []

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
filename = input("Enter the filename: ")
data = load_file(filename)
uwt_name = input("Enter the UWT author's name: ")
uwt_email = input("Enter the UWT author's email: ")
output = input("Enter the name of the new file generated: ")
names = get_names(data)
write(names, output)
###############################################################################