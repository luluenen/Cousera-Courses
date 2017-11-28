#!/usr/bin/python3
import os
from os import path as os_path
import shutil
import sys
import datetime
import numpy as np
import matplotlib.pyplot as plt
import copy
import json
#from node import node
#from algo import floyd_WarshallAlgo
#from algo import dijkstraAlgo

path = []
path = os.path.abspath(os.path.join(os.path.dirname(__file__), './node/'))
if not path in sys.path:
    sys.path.insert(1, path)
path = []
path = os.path.abspath(os.path.join(os.path.dirname(__file__), './algo/'))
if not path in sys.path:
    sys.path.insert(1, path)
#import classes created  
import node
import floyd_WarshallAlgo
import dijkstraAlgo
from csvFile import CsvFile
from jsonFile import JsonFile





# Changes the current working directory to data directory
if __name__ == "__main__":
    path = '/'.join(os_path.abspath(os_path.split(__file__)[0]).split('/')[:-1]) + '/data'
    os.chdir(path)
    print (path)


class Rtt:
    """
    Claas Rtt calculates the shortest route belong to the file name given who has attributs
    @self.dataID: id of input data 
    @self.inputFname: name of input data file where original data saved   
    @self.shortestTimeFname: name of data output file to save shortest path time  
    @self.lengthPathFname: name of data output file to save length of shortest path (nomber of hops)
    @self.targetPath: folder path to save data  
    """
    # TODO where we stock the data
    def __init__(self, dataID):
        self.dataID = dataID
        self.inputFname = ''.join(self.dataID) + '.csv'
        " Creat folder path to save original data and new data  "
        self.folderName = self.dataID
        platform = sys.platform
        path = []
        path = ''.join(os.getcwd()) + '/'+ ''.join (self.folderName) #FIX ME: / not suitable for all OS --- OK ? 
        print (path)
        self.targetPath = path
        #if not self.targetPath in sys.path:
            #sys.path.insert(0, self.targetPath)
        print (os.getcwd())
        print (self.targetPath)
        print (''.join(os.getcwd())+'/'+ self.inputFname)
        # Check original data file is in analysis_data, if yes creat new folder and move it in the folder 
        if os.path.exists(''.join(os.getcwd())+'/'+ self.inputFname):
            print ('enter')
            #Chek if path does not exist then creat a new folder
            if not os.path.exists(self.targetPath):
                os.makedirs(self.targetPath)
                shutil.move(''.join(os.getcwd())+'/'+ self.inputFname, ''.join(self.targetPath)+'/'+self.inputFname)
        os.chdir(self.targetPath)
        print (os.getcwd())

        """Atributes to calculate shortest path"""
        inputFile = CsvFile(self.inputFname)
        self.allData  = inputFile.read_dataCsv()
        self.nbprobes = int (len (self.allData[0]))
        print(self.nbprobes)
        self.nbtimes = int (len(self.allData)/len(self.allData[0]))
        print(self.nbtimes)
        self.dataToCalculate = dict()
        self.algo = None
        self.setAlgo(1)
        self.shortestAllDataTime = []
        self.pathLength = []
        
        """Atributes Csv files to stock data"""
        self.shortestTimeFile = CsvFile(''.join(dataID) + "ShortestTime.csv")
        self.lengthPathFile = CsvFile(''.join(dataID) + "LengthShortestPath.csv")



        
        
    def setAlgo(self, type=1):
        '''
        set algo that you want
        @param type: choose floyd_WarshallAlgo if type = 1, choose dijkstraAlgo if type = 0
        type is 1 in default.
        '''
        if type == 1 :
            self.algo = floyd_WarshallAlgo.Floyd_WarshallAlgo()
        if type ==  0:
            self.algo = dijkstraAlgo.DijkstraAlgo()
   

    def getDataToCalculate(self, data):
        '''
        get data in the file and put in a dictionnary where key is the number of
        probes and values are all RTT times from this probes to others
        '''
        dataDict = dict()
        for src in range(self.nbprobes):
            dataDict[str(src)] = []
            for dst in range(self.nbprobes):
                if data[src][dst] >= 0 and data[src][dst] != None :
                    dataDict[str(src)].append(data[src][dst])
                else:
                    # if the case is None or is -1, we give it a number large enough
                    dataDict[str(src)].append(2000)
        self.dataToCalculate = copy.deepcopy(dataDict)
                

    def node_dict_generator(self):
        nodes = dict()
        for key, values in list(self.dataToCalculate.items()):
            anode = node.Node()
            anode.connections = dict()
            for i in range(len(values)):
                if values[i] != 0:
                    anode.connections['%d' % (i)] = values[i]
            nodes[key] = anode
        self.dataToCalculate = copy.deepcopy(nodes)


    # New function 
    def shortestTime (self, dataOriginal):
        """calculate time of the shortest path"""
        indexes = list(self.dataToCalculate.keys())
        shortestTime =[[0 for dst in range(self.nbprobes)] for src in range(self.nbprobes)]
        for src in indexes:
            for dst in indexes:
                if len(self.dataToCalculate[src].routingPath[dst].path) > 2:
                    length = len(self.dataToCalculate[src].routingPath[dst].path)
                    time = 0.
                    for i in range (length - 1):
                        x = self.dataToCalculate[src].routingPath[dst].path [i]
                        y = self.dataToCalculate[src].routingPath[dst].path [i+1]
                        time =  time + dataOriginal [int(x)][int(y)]
                    shortestTime [int(src)][int(dst)] = time
                #elif dataOriginal [int(src)][int(dst)] < 0:
                    #shortestTime [int(src)][int(dst)] = 2000
                else:
                    shortestTime [int(src)][int(dst)] = dataOriginal [int(src)][int(dst)]
        return shortestTime



    # New function changed nbprobes by pathLength
    def shortestTimePathLength (self):
        """calculate nbprobes in the shortest path"""
        indexes = list(self.dataToCalculate.keys())
        pathLength =[[0 for dst in range(self.nbprobes)] for src in range(self.nbprobes)]
        for src in indexes:
            for dst in indexes:
                pathLength [int(src)][int(dst)] = len(self.dataToCalculate[src].routingPath[dst].path)-1
        return pathLength


    def output_log_file(self, data, shortestRouteFile):
            '''
            write shortest routes in a the file log
            '''
            f = open(shortestRouteFile, "a")
            log = (datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y") + "\n")
            indexes = list(data.keys())
            for i in indexes:
                for j in indexes:
                    if len(data[i].routingPath[j].path) > 2:
                        #print i, j , data[i].routingPath[j].path
                        log += (
                            i + "-" + j + " : " + str(data[i].routingPath[j].path) + "\n")
            log +="\n"
            f.write(log)
            f.close()

    def caculateAllData(self):
        """ Calculate the shortest route for all data """
        if os.path.exists("ShortestRoute"):
            os.remove("ShortestRoute")
        for i in range (self.nbtimes):
            dataBefore = []
            dataBefore = self.allData[i*self.nbprobes: (i+1)*self.nbprobes]
            pathLengthOneTime = []
            shortestTime = []
            # Get data to calculate the shortest routes
            self.getDataToCalculate(dataBefore)
            self.node_dict_generator()
            self.algo.findRoutingPath(self.dataToCalculate)
            shortestTime = self.shortestTime(dataBefore)
            self.shortestAllDataTime = self.shortestAllDataTime + shortestTime
            shortestTimePathLength = self.shortestTimePathLength()
            self.pathLength = self.pathLength + shortestTimePathLength
            #write shortest routes in a file 
            self.output_log_file(self.dataToCalculate, "ShortestRoute")
            
        """ write data into files """ 
        self.shortestTimeFile.write_data(self.shortestAllDataTime)
        self.lengthPathFile.write_data(self.pathLength)           


################################################################
########---------------    main   ---------------------#########
################################################################

if __name__ == "__main__":
    #log_files = [f for f in os.listdir(path) if f.endswith('.log')]
    """ data original """
    #dataAll = read_data(log_files[0])
    myRtt = Rtt('RTT_RipeAtlas2')
    #write_data(dataAll, "rtt_data.csv")
    """create fiveDaysData"""
    #fiveDaysData = copy.deepcopy (dataAll [118*19 : -118*19])
    #write_data(fiveDaysData, "fiveDaysData.csv")
    """calculate shortest path time for all data"""
    myRtt.caculateAllData()
    #caculateOneDayData("fiveDaysData.csv", "shortestOneDayTime.csv",
    #                   "oneDayData.csv", "oneDayPathLength.csv", 0)





       



                

