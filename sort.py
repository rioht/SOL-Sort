import os
import csv
import re
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
"Label", # R/Y
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
			os.makedirs(os.path.split(os.getcwd())[1] + " Vol. 0" + str(i))
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
		sorted_list = sorted(filelist, key=os.path.getmtime)

		return sorted_list

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def copy_files(foo):
	count = 0
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
		if " Vol. 01" in errorcheck[1]:
			return

	for i in xrange(0, len(foo), 1):
		for ii in xrange(0, len(foo[i]), 1):
			if str(foo[i][ii]).lower().endswith('.mp3'):
				count = count + 1
				if count < 10:
					shutil.copy2(str(foo[i][ii]), dirs[i] + "/" + "0" + str(count) + " " + str(foo[i][ii]))
				else:
					shutil.copy2(str(foo[i][ii]), dirs[i] + "/" + str(count) + " " + str(foo[i][ii]))	

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
				if str(foo[i][ii]).lower().endswith('.mp3'):
					
					count = count + 1
					y = os.path.join(dirName, filename)
					af = eyed3.load(y)
					splitstring = str.split(filename, '_')
					if '.mp3' in splitstring[0]:
						splitstring = str.split(splitstring[0], '-')
					sourceData.append("WW") #territory
					sourceData.append(str.split(os.path.split(os.getcwd())[1])[0]) #genre
					sourceData.append("Songs of Love: " + str.replace(os.path.split(os.getcwd())[1], ' Vol.', ', Vol.')) #album title
					sourceData.append("Various Artists") #album artist
					capital = re.findall('[A-Z][^A-Z]*', splitstring[0])
					try:
						randomizer = random.sample(range(0, len(keywords)), 3)
						sourceData.append(capital[0] + " Loves " + keywords[(randomizer[0])] \
						+ "," + " " + keywords[(randomizer[1])] + "," + " " + \
						"and " + keywords[(randomizer[2])]) #track title
					except:
						sourceData.append("TITLE ERROR")
					try: #track artist
						splitstring2 = str.split(splitstring[1], '.mp3')
						singlestring = re.findall('[' '][aA-zZ]*', filename)
						if splitstring2[0][0].isupper() and splitstring2[0][1].isupper():
							sourceData.append(splitstring2[0][0] + '. ' + splitstring2[0][1:])

						elif splitstring2[0][0].isupper() and splitstring2[0][1] == '.':
							sourceData.append(splitstring2[0][0] + '. ' + splitstring2[0][2:])

						else:
							sourceData.append(splitstring2[0])

					except IndexError:
						# this section below to handle a few specific cases.
						try:

							if re.search(r'__', filename):
								double__split = re.findall('[' '][aA-zz]*', filename)
								double__split2 = str.split(double__split[3],'__')
								sourceData.append(double__split2[1])

							elif 'Wolfert' in filename:
								sourceData.append("Wolfert")

							elif '_' and '__' and '-' not in filename:
								nosymbolsplit = str.split(filename, '.')
								nosymbolsplit2 = re.findall('[A-Z][^A-Z]*', nosymbolsplit[0])
								sourceData.append(nosymbolsplit2[1])

							else:
								sourceData.append("TrackArtistPH")
								print "exception1"
								print filename
								print splitstring
								print splitstring2

						except:
							sourceData.append("TrackArtistPH")
							print "exception2"
							print filename
							print splitstring
							print splitstring2

					except:	
						sourceData.append("TrackArtistPH")
						print "exception3"

					sourceData.append(count) #sequence
					try:
						sourceData.append(af.info.time_secs) # duration
					except Exception as e:
						sourceData.append(0)
						print e
					sourceData.append("The Medicine of Music") # label
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
	z = os.getcwd()
	os.chdir(z + "/../../..")
	keywords = load_keywords()
	organize()
	print "job done"
