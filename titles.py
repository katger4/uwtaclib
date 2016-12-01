import csv
from titlecase import titlecase
# import xlrd
# from pandas import *
# xls = ExcelFile('socialwork_pub_1.xls_Fri_Oct_14_16_14_19_2016part_1.xls')
# df = xls.parse(xls.sheet_names[0])
# reader = df.to_dict()
# data = []
# for row in reader:
# 	new_titles = {} 
# 	for k, v in row.items():
# 		if k == 'title':
# 			if v != '':
# 				new_titles['title'] = titlecase(v)
# 		if k == 'publisher':
# 			if v != '':
# 				new_titles['publisher'] = titlecase(v)
# 	row.update(new_titles)
# 	data.append(row)
# data.to_excel('xls_Fri_Oct_14_16_14_19_2016part_1.xls')

def load_file(filename):
	with open(filename, 'r') as file:
		data = []
		reader = csv.DictReader(file)
		for row in reader:
			new_titles = {} 
			for k, v in row.items():
				if k == 'title':
					if v != '':
						new_titles['title'] = titlecase(v)
				if k == 'publisher':
					if v != '':
						new_titles['publisher'] = titlecase(v)
			row.update(new_titles)
			data.append(row)
	return data

def write(data, output):
	# keys = data[0].keys()
	fieldnames = ['title', 'document_type', 'source_publication', 'abstract', 'publication_date', 'fpage', 'lpage', 'issnum', 'volnum', 'doi', 'fulltext_url', 'version', 'source_fulltext_url', 'keywords', 'create_openurl', 'custom_citation', 'author1_fname', 'author1_mname', 'author1_lname', 'author1_suffix', 'author1_email', 'author1_institution', 'author1_is_corporate', 'author2_fname', 'author2_mname', 'author2_lname', 'author2_suffix', 'author2_email', 'author2_institution', 'author2_is_corporate', 'author3_fname', 'author3_mname', 'author3_lname', 'author3_suffix', 'author3_email', 'author3_institution', 'author3_is_corporate', 'author4_fname', 'author4_mname', 'author4_lname', 'author4_suffix', 'author4_email', 'author4_institution', 'author4_is_corporate', 'author5_fname', 'author5_mname', 'author5_lname', 'author5_suffix', 'author5_email', 'author5_institution', 'author5_is_corporate', 'author6_fname', 'author6_mname', 'author6_lname', 'author6_suffix', 'author6_email', 'author6_institution', 'author6_is_corporate', 'author7_fname', 'author7_mname', 'author7_lname', 'author7_suffix', 'author7_email', 'author7_institution', 'author7_is_corporate', 'author8_fname', 'author8_mname', 'author8_lname', 'author8_suffix', 'author8_email', 'author8_institution', 'author8_is_corporate', 'author9_fname', 'author9_mname', 'author9_lname', 'author9_suffix', 'author9_email', 'author9_institution', 'author9_is_corporate']
	with open(output, 'w', encoding='WINDOWS-1252') as output_file:
		dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames, dialect='excel')
		# dict_writer = csv.DictWriter(output_file, dialect='excel')
		dict_writer.writeheader()
		dict_writer.writerows(data)

csv_filename = input("Enter the csv filename: ")
output = input("Enter the new filename: ")

# csv_filename = 'socialwork_pub_1.xls_Fri_Oct_14_16_14_19_2016part_1.csv'
# output = 'socialwork_pub_1.xls_Fri_Oct_14_16_14_19_2016part_1.csv'
data = load_file(csv_filename)
write(data, output)

# 