#coding:utf-8
import csv
import os

def setRtt(source_prob, dest_prob, rtt):
	source_prob = "%d" %source_prob
	copy = "measureFile2.csv"
	measureFile = "measureFile.csv"
	with open(measureFile,"r") as csvfile1, open(copy,"w") as csvfile2:
		spamreader = csv.reader(csvfile1,delimiter=",")
		spamwriter = csv.writer(csvfile2,delimiter=",")
		for row in spamreader:
			print source_prob
			print row[0] == source_prob
			if row[0] == source_prob:
				row[dest_prob] = rtt
			spamwriter.writerow(row)
		# we suppress the ancient file
		os.remove(measureFile)
		os.rename(copy,measureFile)

setRtt(1,2,50)
