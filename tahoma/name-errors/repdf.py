import re
import os
def re_pdfs(root):
	directory = os.listdir(root)

	oldnames = []
	for filename in directory:
		if filename.endswith('.pdf'):
			oldname = os.path.join(root, filename)
			oldnames.append(oldname)
	oldnames.sort()

	newnames = []
	for filename in directory:
		if filename.endswith('.pdf'):
			filename = filename[:-4]
			newname = os.path.join(root, filename)
			newnames.append(newname)
	# http://stackoverflow.com/questions/37057128/rename-files-from-several-folders-oserror-errno-2-no-such-file-or-directory
	for i, j in zip(oldnames, newnames):
		os.rename(i, j)
####################################################
re_pdfs('tw2')