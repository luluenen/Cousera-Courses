# coding:utf-8
# basic librairies
import csv
import os
import time
import json
import sys
from datetime import datetime
import Queue
import shutil
# ~ import pdb; pdb.set_trace()

# project classes
from Measure import Measure
from ThreadAtlas import Thread_makeMeasure
from ThreadAtlas import Thread_writeMeasure
from ThreadAtlas import Thread_stats

# cousteau librairie
from ripe.atlas.cousteau import (Ping, AtlasSource, AtlasCreateRequest)
from ripe.atlas.cousteau import (AtlasStream, ProbeRequest, AtlasResultsRequest)


class AtlasMeasure(Measure):

    def __init__(self):
        Measure.__init__(self)
        # Code for authFile made my Stéphane Bortzmeyer <bortzmeyer+ripe@nic.fr>
        # https://github.com/RIPE-Atlas-Community/ripe-atlas-community-contrib/blob/master/RIPEAtlas.py
        authfile = "%s/.atlas/auth" % os.environ['HOME']
        if not os.path.exists(authfile):
            raise AuthFileNotFound("Authentication file %s not found" % authfile)
        auth = open(authfile)
        key = auth.readline()
        if key is None or key == "":
            raise AuthFileEmpty("Authentication file %s empty or missing a end-of-line at the end" % authfile)
        key = key.rstrip('\n')
        auth.close()
        self.measureFile = "./data/measureFile"
        self.linksFile = "./data/links.csv"
        self.linksFile2 = "./data/links2.csv"
        self.ATLAS_API_KEY_CREATE = key

    # Make a measure of rtt between a list of probe to one probe
    def makeMeasure(self, target_prob, probe_list):
        # we take the id of the probe in the measure file
        id_target = self.getProbeId(target_prob)
        id_probe_list = []
        for probe in probe_list:
            # we get string for the join function which fail with int
            id_probe_list.append(str(self.getProbeId(probe)))
        address_probe_list = []
        # we get the address from atlas api
        target_address = self.getProbeAddress(id_target)

        # we create the ping object
        ping = Ping(
                af=4,
                target=target_address,
                description="measure to probe"
                          + " %d from %s" % (target_prob, str(probe_list).strip('[]')))
        nb_probe = len(probe_list)
        values = ",".join(id_probe_list)
        source = AtlasSource(type="probes", value=values, requested=nb_probe)
        epoch = datetime(1970, 1, 1)
        # we create the measure with the apikey
        # we do only 1 packet for it to be faster
        atlas_request = AtlasCreateRequest(
                # We delay the starting time to be able to retreive all data
                # with passiv methods
                start_time=datetime.utcfromtimestamp((datetime.utcnow()-epoch).total_seconds() + 5),
                key=self.ATLAS_API_KEY_CREATE,
                measurements=[ping],
                sources=[source],
                is_oneoff=True
        )
        (is_success, response) = atlas_request.create()
        response['measurements']

        # we then get the result
        id_result = response['measurements'][0]
        return id_result

    def measureGraph(self, nb_probes):
        # We initialize the measureFile
        self.initialize(nb_probes)

        # We create a list of nb_probes probes with Atlas_id
        sondes = [int(i) for i in range(1, nb_probes + 1)]

        # We create nb_probes-1 measure to have a complete graph
        threads = []

        # We create a queue to sock the results of each threads
        resultQueue = Queue.Queue()
        total = 0
        for i in range(nb_probes - 1):
            total += nb_probes - i - 1
            thread = Thread_makeMeasure(
                    "Thread-%s" % i,
                    self.makeMeasure(sondes[i], sondes[i + 1:]),
                    nb_probes - i - 1,
                    resultQueue
            )
            thread.start()
            threads.append(thread)
        # We create a thread to handle the Queue
        thread_write = Thread_writeMeasure(
                "Thread-write",
                resultQueue
        )
        thread_write.start()
        progress = total
        # We wait for the measure to finish
        while progress != 0:
            progress = 0
            for thread in threads:
                progress += thread.nb_msm
            total = float(total)
            progress = float(progress)
            avancement = round((total - progress) / total, 2)
            sys.stdout.flush()
            sys.stdout.write("Getting RIPE Atlas data: %d%%\r" % (avancement * 100))
        for thread in threads:
            thread.join()
        print "All Thread finish"
        # We wait for the queue to empty
        # Doesn't seem to work
        # ~ resultQueue.join()
        print "Queue is empty"
        # We notify the writing thread that the job is over
        thread_write.not_finished = False
        print "Notifying the last thread to finish"
        # We wait for the write thread to finish
        thread_write.join()
        # Replacing no value by 2000
        self.replaceValue()
        print "Adding the measurement in the archive"
        # if the archive doesn't exist we create it
        if not os.path.isdir("./data/archive"):
            os.mkdir("./data/archive")
        if not os.path.isdir("./data/archive/default"):
			os.mkdir("./data/archive/default")
        # We copy the measureFile to the archive
        # with the date of creation as timestamp
        date = int(os.path.getctime(self.measureFile))
        shutil.copy(self.measureFile, "./data/archive/default/%d" % date)
        # We then print some stats about the actual measurement
        self.statsOnActual()
        # We start a thread to make a log file for all the measurement
        thread = Thread_stats("stats")
        thread.start()
        
        print "Done"
        
        return

    # Function to get the probe adress based on it's ID
    def getProbeAddress(self, probe_id):
        with open("./data/links2.csv", "r") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",")
            spamreader.next()
            for row in spamreader:
                if int(row[1]) == probe_id:
                    return row[2]
                    
    def makeLinks(self,probes,id_measure):
		with open("./data/links%d.csv"%id_measure,"w") as f:
			spamwriter = csv.writer(f,delimiter=",")
			spamwriter.writerow(['id','id_probe','address_v4'])
			cpt = 1
			for probe in probes:
				filters = {"id" : "%d"%probe}
				probesfilter = ProbeRequest(**filters)
				for probefilter in probesfilter:
					address = probefilter["address_v4"]
				spamwriter.writerow([cpt,probe,address])
				cpt +=1

    # Function who take as input the probes to measure
    # and return the Atlas id of the probe
    def getProbeId(self, id_given):
        id_probe = 0
        with open(self.linksFile, "r") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",")
            spamreader.next()
            for row in spamreader:
                if int(row[0]) == id_given:
                    id_probe = int(row[1])
                    return id_probe
        print "The id: %d does not exist" % id_given
        return id_probe

    def getProbeIdFromAddress(self, probe_address):
        # Filter doesn't seem to work with address

        # ~ filters = {"address_v4" : "%s"%probe_address}
        # ~ probes = ProbeRequest(**filters)
        # ~ for probe in probes:
        # ~ print probe["id"]
        # ~ return int(probe["id"])

        # Just a fix, will change it if filter works
        with open(self.linksFile2, "r") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",")
            row = spamreader.next()
            for row in spamreader:
                if row[0] == "":
                    break
                if row[2] == probe_address:
                    return int(row[1])
            print "Probe not found"

    # Function to get the real id from atlas id
    def getRealId(self, atlas_probe_id):
        with open(self.linksFile, "r") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",")
            spamreader.next()
            for row in spamreader:
                if row[1] == "%d" % atlas_probe_id:
                    return int(row[0])
            print "Probe not found"

    # Write the rtt from source to dest in the measurefile
    def setRtt(self, source_prob, dest_prob, rtt):
        # if rtt= -1, path doesn't exist
        if int(rtt) == -1:
            rtt = 2000
        copy = "data/measureFile2.csv"
        with open(self.measureFile, "r+") as csvfile1, open(copy, "w") as csvfile2:
            spamreader = csv.reader(csvfile1, delimiter=",")
            spamwriter = csv.writer(csvfile2, delimiter=",")
            spamreader.next()
            # We recreate the first line in the copyfile
            liste = []
            liste.append('Probes')
            for i in xrange(1, 51):
                liste.append(i)
            spamwriter.writerow(liste)
            for row in spamreader:
                # We consider the rtt to be symetric, so we write the
                # same value for both source/dest and dest/source
                if row[0] != "" and int(row[0]) == source_prob:
                    row[dest_prob] = rtt
                if row[0] != "" and int(row[0]) == dest_prob:
                    row[source_prob] = rtt
                spamwriter.writerow(row)
            os.rename(copy, self.measureFile)

    def initialize(self, nb_probes):
        # We recreate the measureFile
        with open(self.measureFile, "w") as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=",")
            liste = []
            liste.append('Probes')
            for i in xrange(1, nb_probes+1):
                liste.append(i)
            spamwriter.writerow(liste)
            for i in xrange(1, nb_probes+1):
                # We put 0 on the diagonal
                liste = []
                liste.append(i)
                for j in xrange(1, nb_probes+1):
                    if j == i:
                        liste.append(0)
                    else:
                        liste.append('')
                spamwriter.writerow(liste)
                
    # get the stats on the last created measureFile
    def statsOnActual(self):
        with open(self.measureFile,"r") as f, open("./data/measureFile_log.txt","w") as g:
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
            g.write("Lost link: %d over %d links(%d%%)"%(lost,cpt,int(float(lost)/float(cpt)*100)))
            print "Lost link: %d over %d links(%d%%)"%(lost,cpt,int(float(lost)/float(cpt)*100))
            print "See the log file for details"
    
    def replaceValue(self):
        copy = "./data/measureFile2.csv"
        with open(self.measureFile,"r") as f, open(copy,"w") as g:
            spamreader = csv.reader(f,delimiter=",")
            spamwriter = csv.writer(g, delimiter=",")
            spamwriter.writerow(spamreader.next())
            for row in spamreader:
                for i in range(len(row)):
                    if row[i] == "":
                        row[i] = 2000
                spamwriter.writerow(row)
            os.rename(copy, self.measureFile)
                        
                
