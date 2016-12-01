
def get_titles(data):
	titles = []
	for i in data:
		title = i['title']
		alphatitle = re.sub("[^a-zA-Z\s]+", "", title)
		titles.append(alphatitle)
	return titles

pdfFileObj = open('meetingminutes.pdf', 'rb')

pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pdfReader.numPages
pageObj = pdfReader.getPage(0)
pageObj.extractText()

pdfWriter = PyPDF2.PdfFileWriter()
for pageNum in range(pdf1Reader.numPages):
	pageObj = pdf1Reader.getPage(pageNum)
	pdfWriter.addPage(pageObj)

pdfOutputFile = open('combinedminutes.pdf', 'wb')
pdfWriter.write(pdfOutputFile)

for i, j in zip(oldname, newname):
	os.rename(i, j)


load each pdf in dir, if it has the name structure 'Tahoma_West_2016_Inside_Final (dragged) NUM.pdf', search for the title text on page 0, then rename it using the url name from the csv
def load_pdf_text(pdf):
	with open(pdf, 'rb') as file:
		pdfReader = PyPDF2.PdfFileReader(file)
		pdftext = pdfReader.extractText()
	return pdftext

def load_pdf_names(directory): 
	pdfFiles = []
	for filename in os.listdir(directory):
		if filename.endswith('.pdf'):
			pdfFiles.append(filename)
	return pdfFiles

pdfFiles = load_pdf_names('.')

def extract_rename(pdfFiles, titles): 
	pdfFiles.sort(key=str.lower)

	for filename in pdfFiles:
		pdfFileObj = open(filename, 'rb')
		pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
		pageObj = pdfReader.getPage(0)

		pagetext = pageObj.extractText()
		alphatext = re.sub("[^a-zA-Z\s]+", "", pagetext)
		alphatext = re.sub("[\n]+", "", nt)

		for i in titles:
			if i in alphatext:
				wordlist = i.split(" ")
				combo = '_'.join(wordlist)
				newname = combo+'.pdf'
				os.rename(filename, newname)

extract_rename(pdfFiles, titles)

def get_fpages(data):
	fpages = []
	for i in data:
		fpage = i['fpage']
		fpages.append(fpage)
	return fpages

fpages = get_fpages(data)
print(titles)
def fixPdf(pdfFile):
	try:
    	fileOpen = file(pdfFile, "a")
        fileOpen.write("%%EOF")
        fileOpen.close()
        return "Fixed"
    except Exception, e:
    	return "Unable to open file: %s with error: %s" % (pdfFile, str(e))

fixPdf()


def write_pdfs(data):
		pdfWriter = PyPDF2.PdfFileWriter()
		for pageNum in range(fpage, lpage):
			pageObj = pdf1Reader.getPage(pageNum)
			pdfWriter.addPage(pageObj)

s = filter(text.isalnum, s)
''.join([i for i in text if i.isalpha()])
re.sub("[^a-zA-Z\s]+", "", text)
re.sub("[\n]+", "", nt)
text = '1A Dawning of \nDreams\nVirginia Soileau\nﬁAlways keep dreaming the dreams of your past. \nLike a child that plays as the early dawn rises,\nthey will grow with the shadows the morning sun casts.ﬂ\n˜e fairies that frolic through a little girl™s head\ngently lead her feet as she slips o˛ to bed.\n ﬁAlways keep dreaming, for children grow fast...ﬂ\nCentaurs, mermaids, and unicorns too,\nlaze in so˙ ˚owers that shimmer with dew.\n ﬁFreed from the shadows the noon sun casts–ﬂ\nShe rides on dragons that dive through the skies\nwhile Father Time watches with a tear in his eye.\n ﬁAlways keep dreaming your dreams ‚til the last–ﬂ\nPaladins ˝ght horned heathens from Hell,\nas life slowly slips from Youth™s emptying well.\n ﬁWhispering in the shadows the evening sun casts–ﬂ\nI could lay these to rest, with my ebbing age,\nbut I remember the whispers of a wizardly sage:\n ﬁNever stop dreaming the dreams of your past,\n or they will die in the shadows the full moon casts.ﬂ\n'