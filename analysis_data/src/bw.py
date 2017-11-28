import os
import sys
import csv

path = []
path = os.path.abspath(os.path.join(os.path.dirname(__file__), './'))
if not path in sys.path:
    sys.path.insert(1, path)
"""import all functions in rtt file"""
from rtt import *

path = []
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../bw_data'))
os.chdir(path)

log_files = [f for f in os.listdir(path) if f.endswith('.log')]


if __name__ == "__main__":
    """ data original """
    dataAll = read_data(log_files[0])
    #write_data(dataAll, "bw_data.csv")
    #data = read_dataCsv("bw_data.csv")
    nbnodes = len (dataAll[0])
    nbtimes = len(dataAll)/len(dataAll[0])
    bw2 = rtt_3D(dataAll, nbnodes, nbtimes)
    bw3 = rtt_3D2(dataAll, nbnodes, nbtimes)
    #showHisto(bw3,nbnodes)
    #showTrace(bw3,nbnodes)

    """calculate max bw"""
    maxBw=[[0 for dst in range(nbnodes)] for src in range(nbnodes)]
    for src in range (nbnodes):
        for dst in range (nbnodes):
            maxBw[src][dst] = max(bw3[src][dst])

    """calculate min bw"""
    minBw=[[0 for dst in range(nbnodes)] for src in range(nbnodes)]
    for src in range (nbnodes):
        for dst in range (nbnodes):
            minBw[src][dst] = min(bw3[src][dst])

    meanBw = meanRtt(bw3, nbnodes)
    
    """make difference matrix in one dimension"""
    bw  = []
    for src in range (nbnodes):
        for dst in range (nbnodes):
            """values are not useful for src = dst"""
            if src != dst :
                nbtimes = len (bw3[src][dst])
                for t in range (nbtimes):
                    bw.append(bw3[src][dst][t])
    """make percetmoyenne in one dimension"""
    meanBwValue = []
    for src in range (nbnodes):
        for dst in range (nbnodes):
            """values are not useful for src = dst"""
            if src != dst :
               meanBwValue.append(meanBw[src][dst])

    """draw histo for one dimension data bw"""
    '''weights = np.ones_like(bw)/float(len(bw))
    bins = np.linspace(int(min(bw)), int(max(bw)), 50)
    n, bins, patches = plt.hist(bw, bins, weights=weights, facecolor='b')
    plt.ylabel("probability")
    plt.xlabel("bw")
    plt.grid(True)
    plt.axis([int (min(bw)), int(max(bw)), 0, 1])
    plt.title("distribution for bw")
    plt.show()'''


    """write analysis data in csv file (mean of the difference and mean of percentage(dif/timeDirect))"""
    '''with open('analysisBwData.csv', 'w') as csvfile:
        fieldnames = ['link', 'mean of bw' ,'maxValue of bw','minValue of bw']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for src in xrange (nbnodes):
            for dst in xrange (nbnodes):
                link = str(src+1)+'--'+str(dst+1)
                meanV = meanBw[src][dst]
                minV = minBw[src][dst]
                maxV = maxBw[src][dst]
                writer.writerow({'link': link,'mean of bw': meanV, 'maxValue of bw':maxV, 'minValue of bw':minV})
    
    '''
