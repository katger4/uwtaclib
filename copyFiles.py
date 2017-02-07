import shutil as sh 
import os

# Calling shutil.copy(source, destination) will copy the file at the path source to the folder at the path destination. (Both source and destination are strings.) If destination is a filename, it will be used as the new name of the copied file. This function returns a string of the path of the copied file.
os.chdir('C:\\')
shutil.copy('C:\\spam.txt', 'C:\\delicious')
# 'C:\\delicious\\spam.txt'
shutil.copy('eggs.txt', 'C:\\delicious\\eggs2.txt')
# 'C:\\delicious\\eggs2.txt'

# While shutil.copy() will copy a single file, shutil.copytree() will copy an entire folder and every folder and file contained in it. Calling shutil.copytree(source, destination) will copy the folder at the path source, along with all of its files and subfolders, to the folder at the path destination. The source and destination parameters are both strings. The function returns a string of the path of the copied folder.
os.chdir('C:\\')
shutil.copytree('C:\\bacon', 'C:\\bacon_backup')

for folderName, subfolders, filenames in os.walk('C:\\delicious'):
	print('The current folder is ' + folderName)

	for subfolder in subfolders:
		print('SUBFOLDER OF ' + folderName + ': ' + subfolder)
	for filename in filenames:
		print('FILE INSIDE ' + folderName + ': '+ filename)

	print('')