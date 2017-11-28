import json
import urllib3
from pprint import pprint 
import numpy

'''
Gets all ripe Atlas probes, selects and saves into a json file those who are connected, and are either an anchor, or tagged as datacenter. In addition, prints to the standard output a a sublist of the firstly selected probes, of randomnly selected number_of_probes probes belonging to different ASs.
'''
ANCHOR_v2=6018
PROBE_v3=10000
number_of_probes=30
probes_always=numpy.array(['US','DE','GB','BR','HK','ZA','AR'])#consider at least probes from these countries, if available
all_probes_url = 'https://atlas.ripe.net/api/v1/probe-archive/?format=json'

http = urllib3.PoolManager()
r = http.request('GET', all_probes_url )
prb_info= json.loads( r.data.decode('utf-8') )
prbs=dict()
i=0

for prb in prb_info['objects']:
    try :
        tags=prb['tags']
        prb_id=prb['id']
        if prb['status_name']=='Connected' and (('datacentre' in tags and int(prb_id)>=PROBE_v3) or (prb['is_anchor']==True and int(prb_id)>=ANCHOR_v2)):
            prb_asn=prb['asn_v4']
            prb_country=prb['country_code']
            prb_ip_addr=prb['address_v4']
            if prb_ip_addr == None : #If no IPV4 addresse specified, try IPV6
                prb_ip_addr=prb['address_v6']
                prb_asn=prb['asn_v6']
            if prb_ip_addr !=None : #If no IP Addresse specified at all, skip probe
                prb_i={"prb_asn":prb_asn,"prb_ip_addr":prb_ip_addr,"prb_id":prb_id}
                try :
                    prbs[prb_country].append(prb_i)                  
                except KeyError :
                    prbs[prb_country]=[prb_i]              
                i+=1
    except Exception as err:
         continue #If any error, skip probe

#Write all connected probes that are anchor or are tagged as datacenter in a json, indexed by the country to which they belong
with open('probes_by_asn.json', 'w') as fp:
    json.dump(prbs, fp)

#Print the number_of_probes or number of probes in different country connected probes, belonging to a different country and to a different AS
i=0
asns=[]
probes_random=numpy.random.choice(list(prbs.keys()),min(number_of_probes,len(prbs.keys())),replace=False)
probes=numpy.concatenate((probes_always,probes_random))
print('Prb_id,Atlas_id,_IP_')
for country in probes :
    prb_i=numpy.random.choice(prbs[country])
    if  prb_i['prb_asn'] not in asns :
        asns.append(prb_i['prb_asn'])
        print('%s,%s,%s,%s'%(str(i),str(prb_i['prb_id']),prb_i['prb_ip_addr'],country))
        i+=1
        if i>= number_of_probes:
            break


