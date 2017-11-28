#coding:utf-8
import csv
import os

# get the stats on the last created measureFile
def statsOnActual():
	with open("./data/measureFile.csv","r") as f, open("./data/measureFile_log.txt","w") as g:
		spamreader = csv.reader(f, delimiter=",")
		spamreader.next()
		nodes = dict()
		i=0
		for row in spamreader:
			nodes[row.pop(0)] = row
			i+=1
		# We run through the keys in order
		ordred_keys = sorted(nodes,key=int)
		lost = 0
		cpt = 0
		for key in ordred_keys:
			if int(key) != len(ordred_keys): 
				list_distance = nodes[key]
				i = int(key)+1
				#~ print len(list_distance[i-1])
				for value in list_distance[int(key):]:
					cpt +=1
					value = value.strip()
					if value == "" or value == "2000":
						lost +=1
						g.write("Lost link between %s and %d\n"%(key,i))
					i += 1
		print "Lost link: %d over %d links(%d%%)"%(lost,cpt,int(float(lost)/float(cpt)*100))
		print "See the log file for details"

# get the stats on a usual measurement
def statsOnArchive(archiveName):
	if os.path_isdir("./%s"%archiveName):
		location = os.listdir()
		if len(location)>1:
			for element in location:
				if element.endswith(".csv"):
					# TODO
		else:
			print "Not enough data to have stats about the used probes"
	else:
		print "Error, the archive: %s should exist"%archiveName
	
statsOnActual()
			
