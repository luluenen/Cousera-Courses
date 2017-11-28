#coding:utf-8
import threading
import time
import os
import csv
from collections import OrderedDict
from Measure import Measure
from ripe.atlas.cousteau import AtlasStream

class Thread_makeMeasure(threading.Thread):
	
	def __init__(self, nom, msm_id, nb_msm, queue):
		threading.Thread.__init__(self)
		self.name = nom
		self.msm_id = msm_id
		self.nb_msm = nb_msm
		self.queue = queue
	
	def run(self):
		t1 = time.time()
		not_stop = True	
		# we stop the thread if time > 1mn
		while not_stop:
			print "Starting measurement %s"%self.msm_id
			atlas_stream = AtlasStream()
			atlas_stream.connect()
			# Measurement results
			stream_type = "result"
			# Bind function we want to run with every result message received
			atlas_stream.bind_channel(stream_type, self.on_result_response)
			# Subscribe to a new stream
			stream_parameters = {"msm": self.msm_id}
			atlas_stream.start_stream(stream_type=stream_type, **stream_parameters)			
			while self.nb_msm>0 and (time.time()- t1) < 1*60:
				atlas_stream.timeout(5)
			#~ print "Ending %s"%self.name
			self.nb_msm = 0
			not_stop = False
	
	# The callback function
	def on_result_response(self, *args):
		# We decrease the nb_msm on every message received
		self.nb_msm -= 1
		
		# We need to use some function from AtlasMeasure
		from AtlasMeasure import AtlasMeasure
		measure = AtlasMeasure()
		# args is list of json for each probe in the measurement
		# with the streaming api, we get them one by one so len(args)=1
		result = args[0]
		
		# We get the atlas probe_id
		target = measure.getProbeIdFromAddress(result['dst_addr'])
		source = result['prb_id']
		
		#~ print "Measure from %d to %d"%(source,target)
		
		# Then we get our probe id
		target = measure.getRealId(target)
		source = measure.getRealId(source)
		
		# there are 3 packets so we take the median
		rtt = result['avg']
		#We write a list with target,source and rtt to the queue
		self.queue.put([target,source,rtt])

class Thread_writeMeasure(threading.Thread):
	
	def __init__(self, nom, queue):
		threading.Thread.__init__(self)
		self.name = nom
		self.queue = queue
		self.not_finished = True
	
	def run(self):
		# We need to use some function from AtlasMeasure
		from AtlasMeasure import AtlasMeasure
		measure = AtlasMeasure()
		
		while self.not_finished or not self.queue.empty():
			if not self.queue.empty():
				args = self.queue.get()
				target = args[0]
				source = args[1]
				rtt = args[2]
				#~ print "Processing: %s to %s"%(target,source)
				measure.setRtt(source, target, rtt)

class Thread_stats(threading.Thread):
	
	def __init__(self, nom):
		threading.Thread.__init__(self)
		self.name = nom

	def run(self):
		# We read every file in the archive
		# for each probe we give:
		# - last uptime
		# - % of times down/number of measure
		# Mean for every link
		# % up of every link
		links = dict() # dict of dict for every link
		probes = dict() # dict of probes 
		location = os.listdir("./data/archive/default")
		location = sorted(location)
		for element in location:
			if not element.endswith(".py"): # We might have script in data to clean the csv
				with open("./data/archive/default/"+element,"r")as f:
					spamreader = csv.reader(f,delimiter=",")
					spamreader.next()
					for row in spamreader:
						##### Probe Stats #####
						if not row[0] in probes:
							probes[row[0]] = [0,0,0]
						probes[row[0]][0] += 1 # count number of msm
						# Check if the probe is up
						down = True
						for i in range(int(row[0])+1, len(row)):
							if float(row[i]) != float('2000'):
								down = False
								break
						if not down:
							probes[row[0]][1] = int(element) # the last uptime
							probes[row[0]][2] += 1 # count uptime
						##### Link Stats #####
						source = row[0]
						source_number = int(row[0])
						if not source in links:
							links[source] = dict()
						for i in range(source_number+1, len(row)):
							dest = '%d'%i
							if not dest in links[source]:
								links[source][dest] = [0,0,0]
							# sum of every measure for a link
							links[source][dest][0] += float(row[i]) # sum
							links[source][dest][1] += 1 # count
							#~ print float(row[i]) == float('2000')
							if float(row[i]) == float('2000'):
								links[source][dest][2] += 1 # time down
		# Ordering the dict
		probes = OrderedDict(sorted(probes.items(), key=lambda t: int(t[0])))
		links = OrderedDict(sorted(links.items(), key=lambda t: int(t[0])))
		for element in links:
			links[element] = OrderedDict(sorted(links[element].items(), key=lambda t: int(t[0])))

		######## Creating the logfile
		with open("./data/Statistics.txt","w") as f:
			data = ""
			data += "Number of measurement: %d"%len(location)
			data += "\n\n"
			data += "################ Probes Stats ################\n\n"
			for probe in probes:
				uptime = time.ctime(probes[probe][1])
				count = probes[probe][0]
				up = probes[probe][2]
				dispo = float(up)/float(count)*100
				data += "Probe %s: \n"%probe
				data += "\tNumber of measurement: %d\n" %probes[probe][0]
				data += "\tLast uptime: %s\n" %uptime
				data += "\tDisponibiliy: %.2f%%\n\n" %dispo
			
			data += "\n\n"
			data += "################ Links Stats ################\n\n"
			for source in links:
				for dest in links[source]:
					link = "%s - %s" %(source,dest)
					cpt = links[source][dest][1]
					up = cpt - links[source][dest][2] 
					mean = float(links[source][dest][0]) / float(cpt)
					dispo = float(up)/float(cpt)*100
					data += "Link %s: \n"%link
					data += "\tMoyenne: %.2f\n"%mean
					data += "\tDisponibilité: %.2f%%\n\n"%dispo
			f.write(data)
