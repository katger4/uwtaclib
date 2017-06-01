# Tacoma Library: Digital Commons and Streaming Media

Scripts to automate uwt digital commons faculty publication metadata, swank html tables, pdf splitting for tahoma west, and mais metadata 

**Overall Process To Automate UWT Digital Commons Faculty Publication Metadata****:**

1. Obtain publication record

2. Extract metadata using Zotero and add book information to the UWT Faculty Books for purchase spreadsheet

3. Send publication report to request post-print/publisher’s pdf copies of articles (if applicable)

4. Export publications (separate export for books and all other publications) from Zotero using custom translators

5. Use custom python script (1 for books, 1 for all other publications) to convert the Zotero-export-csv to a digital-commons-formatted-csv

6. Open the csv in Excel:

    1. edit the format of the date field (yyyy-mm-dd) 

    2. enter 'fulltext_url' links to pdf/word docs hosted by UWT, generated using FileZilla (if applicable)

    3. check for errors

    4. save as a '.xls'

7. Upload the '.xls' file to the appropriate collection in digital commons and update the digital commons site when prompted

8. Create a SelectedWorks profile using faculty information (via form or UWT directory)

9. Import the publication metadata to SelectedWorks

10. Make profile public

**How to Use the Digital Commons Metadata Formatting Scripts**:

* If using python3 for the first time on a new computer:

    * Download the scripts (**pubs.py** and **books.py** from the shared Dropbox in the Scripts/Zotero Export Processing Folder) and add them to them same folder that you plan to export your zotero metadata into

    * Install python3 ([https://www.python.org/downloads/](https://www.python.org/downloads/))

    * Open Terminal (on a Mac, click on the "Search" icon, type in “terminal”)

    * Install the titlecase module by typing `pip install titlecase`, press enter

* **If python3 is already installed and ready to go** (as it should be on the Digital Commons/Streaming Media iMac):

    * Open Terminal (on a Mac, click on the "Search" icon, type in “terminal” or click on the Application icon in the dock)

    * Blank terminal window:

    * Type in `cd desktop/scripts` to change your working directory to the folder containing both the python scripts and the zotero export file press enter

    * If preparing metadata for Books, type `python3 books.py`, press enter, follow the prompts

    * If preparing metadata for all other publication types, type `python3 pubs.py`, press enter, follow the prompts (**Note**: prompts are identical for `books.py` and `pubs.py`)

        * Prompt 1 "Enter the Zotero-export filename" (**Be sure to include the “.csv” in the filename ** - e.g. faculty_export.csv)

        * Prompts 2 and 3 "Enter the UWT author's name" and “Enter the UWT author's email”:

        * Prompt 4 "Enter the name of the new file generated" (**Be sure to include the “.csv” in the filename ** - e.g. miller.csv):

* If you see this error: `IndexError: list index out of range` then there has been an error with the author-names field from the Zotero export. This probably indicates that book-authors were exported as book-editors, so change this in Zotero, re-export, and try again.

**How to Use the Swank Update Scripts**:

1. Download Swank data:
a. Click on "Links" in the left-hand menu
b. Click "Select All"
c. Click "Export Selected"
2. Add the newly downloaded `digcampus_export.csv` file to the same folder on your computer as the `swank.py` script file (download from Dropbox if not currently on your computer).
3. Open Terminal, type in `cd [path/to/thatFolder]` to change your working directory to the folder containing both files
4. Now type `python3 swank.py`, follow the prompts. When you see the text `New Swank table generated!`, open the new file `swanktable.html` in a text editor (TextEdit, SublimeText, etc).
5. Update the Swank page on the LibGuide by copying the text from the html file into the LibGuide html editor and clicking ‘Save and Close’.

Note: swank.py requires 
- Python3 [download here](https://www.python.org/downloads/)
- BeautifulSoup: install by typing `pip install beautifulsoup4` into Terminal (on a Mac)


**How to Use the PDF splitting and metadata formatting scripts**:

Duplicating and Cropping the Tahoma West pdf:
===============================

Note: instruction adapted from [this blog post](http://ciantic.blogspot.com/2011/09/duplicate-all-pages-in-acrobat-x.html)

1. Open the full Tahoma West pdf in Adobe Acrobat X Pro 
2. Select only the pages in the document that contain publication content and create a new pdf from these pages. 
3. Right click on document, and choose "Page Display Preferences" 
4. Choose "JavaScript" from the left. 
5. Check the "Enable menu items JavaScript execution privileges". 
6. Open the folder `Applications/Adobe Acrobat X Pro/Adobe Acrobat Pro.app/Contents/Resources/JavaScripts` 
7. Download the file `duplicate.js` from the taclibdc dropbox, and drag it into that folder. 
8. Quit and reopen Acrobat if "Duplicate all pages (in-place)" does not appear in the "Edit" menu 
9. Once "Duplicate all pages (in-place)" appears in the edit menu, select it and run it. 
10. Now, run the “crop pages tool” twice: once on odd pages, starting with the left hand pages and then again on the even pages, on the right hand pages 
11. If successful, you should now have a document containing only the Tahoma West publications, one pdf page per Tahoma West page (in order). 
  

Creating/Renaming Individual Tahoma West Publication Files:
===============================

1. Create a new folder to store your individual tahoma west publication files (e.g. ‘tw’) the folder containing your files and scripts  
2. Select the pages corresponding to the first TW publication, drag these pages into the folder you just created (on a mac, this file will be named “Tahoma_West_2016 (dragged).pdf”) 
3. Select the pages corresponding to the second TW publication, drag these pages into this same folder (this file will be named “Tahoma_West_2016 (dragged) 1.pdf” 
4. Repeat this process for all subsequent publications. 
5. Rename the first publication to add a 0: “Tahoma_West_2016 (dragged) 0.pdf” so that your pdfs will stay ordered (Note: you have to do this after ALL other publications have been added to the folder to ensure the filenames correspond to the publication order) 
6. Important: Make a backup copy of the folder containing all the unnamed, dragged pdfs (e.g. ‘tw-backup’). Otherwise, if the python script fails, you will have to drag all the pdf’s again! 
7. Download the `namepdfs.py` script from dropbox and put it into the same folder where your **completed tahoma west metadata csv** is. 
8. Open terminal, type in ```cd [path/to/thatFolder]``` to change your working directory to the folder containing your metadata csv, as well as the dragged pdfs subfolder. 
9. Now type ```python3 namepdfs.py```, follow the prompts. When you see the text ```files renamed!```, open the folder containing your dragged pdfs. They should all be renamed appropriately, if not, good thing you made that backup folder!


**How to Use the MAIS Metadata Web Scraping scripts**:

1. Open the `maisWeb.py` script in your preferred text editor.
2. Replace the links in lines 27, 28, 76, and 78 to reflect the links to the ResearchWorks archive pages containing the MAIS capstones you will be obtaining the metadata for (e.g. [line 27](https://digital.lib.washington.edu/researchworks/handle/1773/20063/browse?rpp=20&sort_by=2&type=dateissued&offset=0&etal=-1&order=ASC)).
3. Download the csv file containing the list of MAIS capstones currently in Digital Commons, rename line 44 to reflect that file name.
4. Save the script with this updated information, open terminal and enter `python3 maisWeb.py` to get a csv output of capstones that have not yet been added to Digital Commons, formatted for upload.

Note: maisWeb.py requires 
- Python3 [download here](https://www.python.org/downloads/)
- BeautifulSoup: install by typing `pip install beautifulsoup4` into Terminal (on a Mac)
- requests: install by typing `pip install requests` into Terminal (on a Mac)
