import os
import csv
import shutil
import eyed3
import random

# Variables #

keys = [

"Territory", # R/Y: Always "WW"
"Genre", # R/N: Supplied by SOL
"Album Title", # R/Y
"Album Artist", # R/Y
"Track Title", # R/Y
"Track Artist", # R/Y
"Sequence", # R/Y
"Duration", # R/Y
"Label", # R/N: Blank
"UPC", # R/Y: Blank for Tunecore
"Release", # R/N: Blank
"ISRC", # R/Y: Blank for Tunecore
"Songwriter", # R/N: Blank
"Publisher", # R/N: Blank
"Cline" # R/N: Blank

]

# Functions - Assisting Functions #

def load_keywords():
	keywords = []
	with open("keywords.csv") as f:
		reader = csv.reader(f)
		for row in reader:
			keywords.append(row[0].lstrip())
			if '' in keywords:
				keywords.remove('')

	return keywords

def open_catalog_csv(foo):
	with open(foo + '.csv', 'wb') as f:
		writer = csv.writer(f, delimiter = ',')
		writer.writerow(keys)

def append_csv(foo, source):
	with open(foo + '.csv', 'a') as f:
		writer = csv.writer(f, delimiter = ',')
		writer.writerow(source)
		source = []

def get_folders_count(foo):

	if foo <= 20:
		var_folders = 1
	else:
		if foo % 20 == 0:
			var_folders = foo / 20
		else:
			var_folders = (foo / 20) + 1

	return var_folders

def makedirs(foo):
	try:
		for i in xrange(1, foo, 1):
			os.makedirs(os.path.split(os.getcwd())[1] + " Vol 0" + str(i))
	except Exception as e:
		print e
		pass

def sort_filelist():
	for dirName, subdirList, fileList in os.walk(os.getcwd()):
		filelist = [f for f in fileList if not f[0] == '.']
		if 'sort.csv' in fileList:
			fileList.remove('sort.csv')
		if 'sort.py' in fileList:
			fileList.remove('sort.py')
		if 'sort.app' in subdirList:
			subdirList.remove('preprocess.app')
		sorted_list = sorted(filelist, key=os.path.getmtime)

		return sorted_list

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def copy_files(foo):
	dirs = []
	errorcheck = os.path.split(os.getcwd())
	for dirName, subdirList, fileList in os.walk(os.getcwd()):
		dirs.append(dirName)
		if os.getcwd() in dirs:
			dirs.remove(os.getcwd())
			"""
			To prevent files from being copied recursively,
			the following control flow stops the function.
			However, a folder is still created.
			"""
		if " Vol 01" in errorcheck[1]:
			return

	for i in xrange(0, len(foo), 1):
		for ii in xrange(0, len(foo[i]), 1):
			shutil.copy2(str(foo[i][ii]), dirs[i])

# Functions - Main Functions #

def catalog():
	count = 0
	dirs = []
	sourceData = []

	for dirName, subdirList, fileList in os.walk(os.getcwd()):
		dirs.append(dirName)
		if os.getcwd() in dirs:
			dirs.remove(os.getcwd())

	for directory in dirs:
		os.chdir(directory)
		open_catalog_csv(os.path.split(os.getcwd())[1])
		for dirName, subdirList, fileList in os.walk(os.getcwd()):
			fileList = [f for f in fileList if not f[0] == '.']
			for filename in fileList:
				if filename.endswith('.mp3') or filename.endswith('.MP3') \
				or filename.endswith('.Mp3') or filename.endswith('.mP3'):
					
					count = count + 1
					y = os.path.join(dirName, filename)
					af = eyed3.load(y)
					splitstring = str.split(filename, '_')
					if '.mp3' in splitstring[0]:
						splitstring = str.split(splitstring[0], '-')
					sourceData.append("WW") #territory
					sourceData.append(str.split(os.path.split(os.getcwd())[1])[0]) #genre
					sourceData.append("Songs of Love: " + os.path.split(os.getcwd())[1]) #album title
					sourceData.append("Songs of Love") #album artist
					sourceData.append(splitstring[0] + " Loves " + random.choice(keywords) \
					+ "," + " " + random.choice(keywords) + "," + " " + \
					"and " + random.choice(keywords)) #track title
					try: #track artist
						splitstring2 = str.split(splitstring[1], '.mp3')
						if splitstring2[0][0].isupper() and splitstring2[0][1].isupper():
							sourceData.append(splitstring2[0][0] +'.' + splitstring2[0][1:])

						else:
							sourceData.append(splitstring2[0])
					except:
						sourceData.append("TrackArtistPH")

					sourceData.append(count) #sequence
					try:
						sourceData.append(af.info.time_secs) # duration
					except Exception as e:
						sourceData.append(0)
						print e
					sourceData.append("")
					sourceData.append("")
					sourceData.append("")
					sourceData.append("")
					sourceData.append("")
					sourceData.append("")
					sourceData.append("")
					append_csv(os.path.split(os.getcwd())[1], sourceData)
					sourceData = []

def organize():

	for dirName, subdirList, fileList in os.walk(os.getcwd()):
		fileList = [f for f in fileList if not f[0] == '.']
		if 'sort.csv' in fileList:
			fileList.remove('sort.csv')
		if 'sort.py' in fileList:
			fileList.remove('sort.py')
		if 'keywords.csv' in fileList:
			fileList.remove('keywords.csv')
		if os.getcwd() != dirName:
			os.chdir(dirName)
			if os.path.split(os.getcwd())[1] + '.csv' in fileList:
				fileList.remove(os.path.split(os.getcwd())[1] + '.csv')

			var_folders = get_folders_count(len(fileList))
			
			try:
				makedirs(var_folders + 1)
			except Exception as e:
				print e
				pass
			
			sorted_list = sort_filelist()
			chunked_list = list(chunks(sorted_list, 20))

			try:
				copy_files(chunked_list)
			except Exception as e:
				print e
				pass
			
			catalog()

# Main #

if __name__ == '__main__':
	#comment the two lines below for dev/actual vers
	#z = os.getcwd()
	#os.chdir(z + "/../../..")
	keywords = load_keywords()
	organize()
	print "job done"
