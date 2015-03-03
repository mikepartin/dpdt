#!/usr/bin/python3
# "dpdt.py" - 03-03-2015 - Modified By: Michael Partin
# Original Example From: http://www.pythoncentral.io/finding-duplicate-files-with-python/

# Description:
# List all the duplicate files on a file system. The orginal example above would simply
# create a dictionary using md5 sums as the indexs. I have modified the script so that
# it first creates a dictionary using the file sizes and then only the files with the
# same sizes need to have their md5 calculated. This hopefully will cut down on some
# of the time needed to execute the code. This scipt is ment to be ran with a BASH script
# dpdt.

import os, sys
import hashlib

def findSameSize(parentFolder):
	dups = {}
	listOf = []
	for dirName, subdirs, fileList in os.walk(parentFolder):
		print('Scanning %s...' % dirName)
		for filename in fileList:
			# Get the path to the file
			path = os.path.join(dirName, filename)
			try:
				currentFileSize = os.stat(path).st_size
				if os.path.islink(path) == False and currentFileSize != 0:
					# Add or append the file path
					if currentFileSize in dups:
						dups[currentFileSize].append(str(path))
					else:
						dups[currentFileSize] = [str(path)]
			except:
				dummy=5
	return dups

def hashfile(path, blocksize = 65536):
	try:	
		afile = open(path, 'rb')
		hasher = hashlib.md5()
		buf = afile.read(blocksize)
		while len(buf) > 0:
			hasher.update(buf)
			buf = afile.read(blocksize)
		afile.close()
		return hasher.hexdigest()
	except:
		return 0

def checkSumResults(dict1):
	cmDups = {}
	results = list(filter(lambda x: len(x) > 1, dict1.values()))
	if len(results) > 0:
		for result in results:
			for subresult in result:
				file_hash = hashfile(subresult)
				currentFileSize = os.stat(subresult).st_size
				if file_hash != 0:
					if file_hash in cmDups:
						cmDups[file_hash].append(str(subresult) + " [ Size: " + str(currentFileSize) + " | MD5: " + str(file_hash) + "]")
					else:
						cmDups[file_hash] = [str(subresult) + " [ Size: " + str(currentFileSize) + " | MD5: " + str(file_hash) + "]"]
	return cmDups

# Joins two dictionaries
def joinDicts(dict1, dict2):
	for key in dict2.keys():
		if key in dict1:
			dict1[key] = dict1[key] + dict2[key]
		else:
			dict1[key] = dict2[key]

def printResults(dict1):
	results = list(filter(lambda x: len(x) > 1, dict1.values()))
	if len(results) > 0:
		print('Duplicates Found:')
		print('The following files are identical. The name could differ, but the content is identical')
		print('------------------------------------------------------------------')
		for result in results:
			for subresult in result:
				print('\t\t%s' % subresult)
			print('------------------------------------------------------------------')
	else:
		print('No duplicate files found.')

if __name__ == '__main__':
	if len(sys.argv) > 1:
		dups = {}
		folders = sys.argv[1:]
		for i in folders:
			# Iterate the folders given
			if os.path.exists(1):
				# Find the duplicated files and append them to the dups
				print("***Scanning Please Wait...")
				joinDicts(dups, findSameSize(i))
			else:
				print('%s is not a valid path, please verify' % i)
				sys.exit()
		print("***Finding Duplicates...")
		printResults(checkSumResults(dups))
	else:
		print('Usage: python dpdt.py folder or df.py folder1 folder2 folder3')
