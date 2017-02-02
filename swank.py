import csv
from bs4 import BeautifulSoup

# Open the CSV file for reading
reader = csv.reader(open('digcampus_export.csv'))

# Create the HTML file for output
htmlfile = open('swank-table.html',"w")

# initialize rownum variable
# rownum = 0

header = '<table class="table table-bordered table-striped table-hover" style="width: 385px; border-spacing: 0px; border-collapse: separate; border: 1px solid rgb(221, 221, 221);" width="386"><colgroup><col /><col /><col /></colgroup><tbody><tr height="21"><td class="ck_border" height="21" style="height: 21px; width: 163px; padding: 2px; border: 1px solid rgb(221, 221, 221);"><strong>Title</strong></td><td class="ck_border" style="width: 87px; padding: 2px; border: 1px solid rgb(221, 221, 221);"><strong>Release Year</strong></td><td class="ck_border" style="width: 136px; padding: 2px; border: 1px solid rgb(221, 221, 221);"><strong>License - Valid To</strong></td></tr>'

# write header
htmlfile.write(header)

# generate table contents
# skip header row
next(reader)
# Read a single row from the CSV file
for row in reader:
	htmlfile.write('<tr height="21">')
	
	TITLE = row[0]
	YEAR = row[1]
	LINK = row[2]
	DATE = row[6]

	htmlfile.write('<td class="ck_border" height="21" style="height: 21px; padding: 2px; border: 1px solid rgb(221, 221, 221);"><a href="'+LINK+'</td>''">'+TITLE+'</a></td><td align="right" class="ck_border" style="padding: 2px; border: 1px solid rgb(221, 221, 221);">'+YEAR+'</td><td align="right" class="ck_border" style="padding: 2px; border: 1px solid rgb(221, 221, 221);">'+DATE+'</td>')

	htmlfile.write('</tr>')

TODAY = str(input("Enter today's date: "))
footer = '</tbody></table><p style="line-height: 20.8px;">Updated '+TODAY+'</p>'
htmlfile.write(footer)

# # pretty print the html file using BeautifulSoup (install with 'pip3 install beautifulsoup4' if module not found)
# soup = BeautifulSoup(open('swank-table.html'), "html.parser")
# prettyHTML = soup.prettify()
# # Opening a file creates it and (unless append ('a') is set) overwrites it with emptyness
# htmlfile.close()
# prettyfile = open('swank-table.html',"w")
# prettyfile.write(prettyHTML)
print('New Swank table generated!')