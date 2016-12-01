import re
import csv
from titlecase import titlecase

# this python3 script takes in the Zotero export generated csv of all non-book publications and outputs a csv using the headers and text formatting necessary for upload to digital commons

# NOTE: the output csv should be opened in Excel and scanned for errors, then saved as a '.xls' file (NOT '.xlsx')

###############################################################################
# this function takes in the Zotero-export csv, represents the content as a list of python dicts (where headers are keys and row-content is each value), then changes the Zotero generated headers to DC headers. then, Zotero-generated content for the 'document_type' field is converted to the DC-mandated style, allowing for conditional content creation based on the document type (e.g. whether to create_openurl and special field manipulation for reports/presentations). then, conditionally edit the content of specific header-values (e.g. publication titles --> titlecase, splitting up the page ranges into two separate columns, formatting dates), update the dict with these new values, remove dummy columns, and add each new row (as a dict) to the list of dicts called 'data' 
def load_file(filename):
	# see baby-names for os stuff files_list = os.listdir(directory)
	# with open(filename, 'r') as file:
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
			newrow['issnum'] = newrow.pop('issue')
			newrow['document_type'] = newrow.pop('item type')
			newrow['lpage'] = newrow.pop('num pages')
			newrow['fpage'] = newrow.pop('pages')
			newrow['source_publication'] = newrow.pop('publication title')
			newrow['version'] = newrow.pop('rights')
			newrow['source_fulltext_url'] = newrow.pop('url')
			newrow['volnum'] = newrow.pop('volume')
			newrow['title'] = newrow.pop('\ufeff"title"')
			newrow['keywords'] = newrow.pop('extra')
			newrow['custom_citation'] = newrow.pop('archive')

			# change the document type values from Zotero --> UWT style and use the document type to fill in a value for the create_openurl column
			if newrow['document_type'] == 'bookSection':
				newrow['document_type'] = 'bookchapter'
				newrow['create_openurl'] = 'FALSE'
			elif newrow['document_type'] == 'journalArticle':
				newrow['document_type'] = 'article'
				newrow['create_openurl'] = 'TRUE'
				# get rid of url's if not linking to open access full text
				if newrow['version'] != 'open access':
					newrow['source_fulltext_url'] = ''
			elif newrow['document_type'] == 'conferencePaper':
				# fyi: 'proceedings title' zotero field --> 'source_publication'
				newrow['document_type'] = 'conference'	
				newrow['create_openurl'] = 'TRUE'		
			elif newrow['document_type'] == 'encyclopediaArticle':
				newrow['document_type'] = 'encyclopedia'
				newrow['create_openurl'] = 'FALSE'
			elif newrow['document_type'] == 'presentation':
				newrow['create_openurl'] = 'FALSE'
				# if the document is a presentation, use the entry in the 'meeting name' category as the source_publication entry and the entry in the 'language' category as the citation
				newrow['source_publication'] = newrow['meeting name']
				newrow['custom_citation'] = newrow['language']
			elif newrow['document_type'] == 'report':
				newrow['create_openurl'] = 'FALSE'
				# if the document is a report, use the entry in the 'publisher' category as the source_publication entry
				newrow['source_publication'] = newrow['publisher']

			# create a new blank dict to conditionally edit the values of some headers before updating the original dict with these new values
			newcontent = {} 
			for k, v in newrow.items():
				
				# convert case of publication (uses titlecase module)
				if k == 'source_publication':
					if v != '':
						newcontent['source_publication'] = titlecase(v)
				
				# convert case of pub title and replace weird characters with excel readable characters
				elif k == 'title':
					if v != '':
						newcontent['title'] = titlecase(v)
				
				# split the page range in the fpage column on the hyphen, place first value in fpage and second value in lpage (if split worked, if not, keep value in fpage column)
				elif k == 'fpage':
					if v != '':
						# dash = re.match()
						# pgs = v.split('-') '–'
						pgs = re.split('-|–|­-|-', v)
						newcontent['fpage'] = pgs[0]
						if len(pgs) == 2:
							newcontent['lpage'] = pgs[1]
				
				# find and replace semicolon separators in keywords column with commas, then save this list as the keywords value
				elif k == 'automatic tags':
					if v != '':
						cs = v.replace(';', ',')
						newcontent['keywords'] = cs

				# if the issue number is not blank, add a blank space in front of the value so that excel doesn't convert issue ranges to dates
				elif k == 'issnum':
					if v != '':
						s = " "+v
						newcontent['issnum'] = s

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
			newrow.pop('publisher')
			newrow.pop('meeting name')	
			newrow.pop('language')		

			# append the formatted dict (a row in the csv) to the full data list
			data.append(newrow)

	return data

# takes in the modified list of dicts from the 'load_file' function, iterates through each row/dict in the list, formats author names as a list of names using the helper functions below, then extends the list of names with empty strings so that the length of the names list matches the length of the author name headers, then zip the headers and author names as key-value pairs in order to update the row/dict with the new fields
def get_names(data):
	for row in data:
		names_list = parse_names(row)

		author_headers = ['author1_fname', 'author1_mname', 'author1_lname', 'author1_suffix', 'author1_email', 'author1_institution', 'author1_is_corporate', 'author2_fname', 'author2_mname', 'author2_lname', 'author2_suffix', 'author2_email', 'author2_institution', 'author2_is_corporate', 'author3_fname', 'author3_mname', 'author3_lname', 'author3_suffix', 'author3_email', 'author3_institution', 'author3_is_corporate', 'author4_fname', 'author4_mname', 'author4_lname', 'author4_suffix', 'author4_email', 'author4_institution', 'author4_is_corporate', 'author5_fname', 'author5_mname', 'author5_lname', 'author5_suffix', 'author5_email', 'author5_institution', 'author5_is_corporate', 'author6_fname', 'author6_mname', 'author6_lname', 'author6_suffix', 'author6_email', 'author6_institution', 'author6_is_corporate', 'author7_fname', 'author7_mname', 'author7_lname', 'author7_suffix', 'author7_email', 'author7_institution', 'author7_is_corporate', 'author8_fname', 'author8_mname', 'author8_lname', 'author8_suffix', 'author8_email', 'author8_institution', 'author8_is_corporate', 'author9_fname', 'author9_mname', 'author9_lname', 'author9_suffix', 'author9_email', 'author9_institution', 'author9_is_corporate', 'author10_fname', 'author10_mname', 'author10_lname', 'author10_suffix', 'author10_email', 'author10_institution', 'author10_is_corporate', 'author11_fname', 'author11_mname', 'author11_lname', 'author11_suffix', 'author11_email', 'author11_institution', 'author11_is_corporate', 'author12_fname', 'author12_mname', 'author12_lname', 'author12_suffix', 'author12_email', 'author12_institution', 'author12_is_corporate', 'author13_fname', 'author13_mname', 'author13_lname', 'author13_suffix', 'author13_email', 'author13_institution', 'author13_is_corporate', 'author14_fname', 'author14_mname', 'author14_lname', 'author14_suffix', 'author14_email', 'author14_institution', 'author14_is_corporate', 'author15_fname', 'author15_mname', 'author15_lname', 'author15_suffix', 'author15_email', 'author15_institution', 'author15_is_corporate', 'author16_fname', 'author16_mname', 'author16_lname', 'author16_suffix', 'author16_email', 'author16_institution', 'author16_is_corporate', 'author17_fname', 'author17_mname', 'author17_lname', 'author17_suffix', 'author17_email', 'author17_institution', 'author17_is_corporate', 'author18_fname', 'author18_mname', 'author18_lname', 'author18_suffix', 'author18_email', 'author18_institution', 'author18_is_corporate', 'author19_fname', 'author19_mname', 'author19_lname', 'author19_suffix', 'author19_email', 'author19_institution', 'author19_is_corporate', 'author20_fname', 'author20_mname', 'author20_lname', 'author20_suffix', 'author20_email', 'author20_institution', 'author20_is_corporate', 'author21_fname', 'author21_mname', 'author21_lname', 'author21_suffix', 'author21_email', 'author21_institution', 'author21_is_corporate', 'author22_fname', 'author22_mname', 'author22_lname', 'author22_suffix', 'author22_email', 'author22_institution', 'author22_is_corporate', 'author23_fname', 'author23_mname', 'author23_lname', 'author23_suffix', 'author23_email', 'author23_institution', 'author23_is_corporate', 'author24_fname', 'author24_mname', 'author24_lname', 'author24_suffix', 'author24_email', 'author24_institution', 'author24_is_corporate', 'author25_fname', 'author25_mname', 'author25_lname', 'author25_suffix', 'author25_email', 'author25_institution', 'author25_is_corporate', 'author26_fname', 'author26_mname', 'author26_lname', 'author26_suffix', 'author26_email', 'author26_institution', 'author26_is_corporate', 'author27_fname', 'author27_mname', 'author27_lname', 'author27_suffix', 'author27_email', 'author27_institution', 'author27_is_corporate', 'author28_fname', 'author28_mname', 'author28_lname', 'author28_suffix', 'author28_email', 'author28_institution', 'author28_is_corporate', 'author29_fname', 'author29_mname', 'author29_lname', 'author29_suffix', 'author29_email', 'author29_institution', 'author29_is_corporate']

		
		auth_tuples = []
		
		dif = len(author_headers) - len(names_list)
		empty = ['']*dif
		names_list.extend(empty)
		
		if len(names_list) == len(author_headers):
			z = list(zip(author_headers,names_list))
			auth_tuples.extend(z)
		else: 
			print("Over 29 authors! Adjust author_headers and fieldnames")
			break

		# print(auth_tuples[0])
		d = dict(auth_tuples)

		if "University of Washington Tacoma" in d.values():
			row.update(d)
			row.pop('author')
		else:
			print("One row contains no UWT affiliation for any authors listed, check author list to add UWT affiliation manually.")
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
		# split the variable on whitespace if there, if not fmlist = firstmid (e.g. ["Sarah"] or ["Evelyn", "M."])
		fmlist = re.split("\s", firstmid)
		
		# print(len(fmlist))
		# print(fmlist)
		
		# if fmlist has a first name and middle inital, add all three to the 7 item list of author identifiers
		if len(fmlist) > 1:
			first = fmlist[0]
			mid = fmlist[1]
			fullname = [first,mid,last,"","","",""]
			# use the input identifier variables to determine whether the author is affiliated with uwt, add that info to the list
			tac_name = label_tac_author(fullname, uwt_name, uwt_email)
			# fullname = (first,mid,last,"","","","")
			names_list.extend(tac_name)
		
		# if fmlist has just a first name, input an empty string in place of a middle inital
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
	#keys = data[0].keys() #this doesn't keep the fieldnames in any order, hence needing to manually do so below
	fieldnames = ['title', 'document_type', 'source_publication', 'abstract', 'publication_date', 'fpage', 'lpage', 'issnum', 'volnum', 'doi', 'fulltext_url', 'version', 'source_fulltext_url', 'keywords', 'create_openurl', 'custom_citation', 'author1_fname', 'author1_mname', 'author1_lname', 'author1_suffix', 'author1_email', 'author1_institution', 'author1_is_corporate', 'author2_fname', 'author2_mname', 'author2_lname', 'author2_suffix', 'author2_email', 'author2_institution', 'author2_is_corporate', 'author3_fname', 'author3_mname', 'author3_lname', 'author3_suffix', 'author3_email', 'author3_institution', 'author3_is_corporate', 'author4_fname', 'author4_mname', 'author4_lname', 'author4_suffix', 'author4_email', 'author4_institution', 'author4_is_corporate', 'author5_fname', 'author5_mname', 'author5_lname', 'author5_suffix', 'author5_email', 'author5_institution', 'author5_is_corporate', 'author6_fname', 'author6_mname', 'author6_lname', 'author6_suffix', 'author6_email', 'author6_institution', 'author6_is_corporate', 'author7_fname', 'author7_mname', 'author7_lname', 'author7_suffix', 'author7_email', 'author7_institution', 'author7_is_corporate', 'author8_fname', 'author8_mname', 'author8_lname', 'author8_suffix', 'author8_email', 'author8_institution', 'author8_is_corporate', 'author9_fname', 'author9_mname', 'author9_lname', 'author9_suffix', 'author9_email', 'author9_institution', 'author9_is_corporate', 'author10_fname', 'author10_mname', 'author10_lname', 'author10_suffix', 'author10_email', 'author10_institution', 'author10_is_corporate', 'author11_fname', 'author11_mname', 'author11_lname', 'author11_suffix', 'author11_email', 'author11_institution', 'author11_is_corporate', 'author12_fname', 'author12_mname', 'author12_lname', 'author12_suffix', 'author12_email', 'author12_institution', 'author12_is_corporate', 'author13_fname', 'author13_mname', 'author13_lname', 'author13_suffix', 'author13_email', 'author13_institution', 'author13_is_corporate', 'author14_fname', 'author14_mname', 'author14_lname', 'author14_suffix', 'author14_email', 'author14_institution', 'author14_is_corporate', 'author15_fname', 'author15_mname', 'author15_lname', 'author15_suffix', 'author15_email', 'author15_institution', 'author15_is_corporate', 'author16_fname', 'author16_mname', 'author16_lname', 'author16_suffix', 'author16_email', 'author16_institution', 'author16_is_corporate', 'author17_fname', 'author17_mname', 'author17_lname', 'author17_suffix', 'author17_email', 'author17_institution', 'author17_is_corporate', 'author18_fname', 'author18_mname', 'author18_lname', 'author18_suffix', 'author18_email', 'author18_institution', 'author18_is_corporate', 'author19_fname', 'author19_mname', 'author19_lname', 'author19_suffix', 'author19_email', 'author19_institution', 'author19_is_corporate', 'author20_fname', 'author20_mname', 'author20_lname', 'author20_suffix', 'author20_email', 'author20_institution', 'author20_is_corporate', 'author21_fname', 'author21_mname', 'author21_lname', 'author21_suffix', 'author21_email', 'author21_institution', 'author21_is_corporate', 'author22_fname', 'author22_mname', 'author22_lname', 'author22_suffix', 'author22_email', 'author22_institution', 'author22_is_corporate', 'author23_fname', 'author23_mname', 'author23_lname', 'author23_suffix', 'author23_email', 'author23_institution', 'author23_is_corporate', 'author24_fname', 'author24_mname', 'author24_lname', 'author24_suffix', 'author24_email', 'author24_institution', 'author24_is_corporate', 'author25_fname', 'author25_mname', 'author25_lname', 'author25_suffix', 'author25_email', 'author25_institution', 'author25_is_corporate', 'author26_fname', 'author26_mname', 'author26_lname', 'author26_suffix', 'author26_email', 'author26_institution', 'author26_is_corporate', 'author27_fname', 'author27_mname', 'author27_lname', 'author27_suffix', 'author27_email', 'author27_institution', 'author27_is_corporate', 'author28_fname', 'author28_mname', 'author28_lname', 'author28_suffix', 'author28_email', 'author28_institution', 'author28_is_corporate', 'author29_fname', 'author29_mname', 'author29_lname', 'author29_suffix', 'author29_email', 'author29_institution', 'author29_is_corporate']
	# with open(output, 'w') as output_file: 
	with open(output, 'w', encoding='WINDOWS-1252') as output_file: # encoding needed to write unicode characters as excel preferred encoding (http://stackoverflow.com/questions/6588068/which-encoding-opens-csv-files-correctly-with-excel-on-both-mac-and-windows)
		dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames) # , dialect='excel'
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