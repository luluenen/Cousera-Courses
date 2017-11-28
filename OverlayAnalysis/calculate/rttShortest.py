
import os
from os import path as os_path
import shutil
import sys
import datetime
import copy
import json
import numpy as np

path = []
path = os.path.abspath(os.path.join(os.path.dirname(__file__), './node/'))
if not path in sys.path:
    sys.path.insert(1, path)
path = []
path = os.path.abspath(os.path.join(os.path.dirname(__file__), './algo/'))
if not path in sys.path:
    sys.path.insert(1, path)
path = []
path = os.path.abspath(os.path.join(os.path.dirname(__file__), './fileTools/'))
if not path in sys.path:
    sys.path.insert(1, path)

#import classes created  
import node
import floyd_WarshallAlgo
import dijkstraAlgo
from csvFile import CsvFile






# Changes the current working directory to data directory
if __name__ == "__main__":
    path = '/'.join(os_path.abspath(os_path.split(__file__)[0]).split('/')[:-1]) + '/data'
    os.chdir(path)
    print (path)


class RttShortest:
    """
    Claas Rtt calculates the shortest route belong to the file name given
    Then save shortestTime and shortestPathLength into csv files
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
        path = []
        path = ''.join(os.getcwd()) + '/'+ ''.join (self.folderName)
        self.targetPath = path
        # Check original data file is in data folder, if yes creat folder data/dataID/calculateData
        if os.path.exists(self.targetPath + '/' +''.join(self.inputFname)):
            #Chek if targetPath does not exist then creat a new folder
            if not os.path.exists(self.targetPath +'/calculateData'):
                os.makedirs(self.targetPath+'/calculateData')
                #shutil.move(''.join(os.getcwd())+'/'+ ''.join(self.inputFname), ''.join(self.targetPath)+'/'+''.join(self.inputFname))
            """Atributes to calculate shortest path"""
            inputFile = CsvFile(self.targetPath+'/'+''.join(self.inputFname))
            self.allData  = inputFile.read_dataCsv()
            self.nbprobes = int (len (self.allData[0]))
            self.nbtimes = int (len(self.allData)/len(self.allData[0]))
            self.dataToCalculate = dict()
            self.algo = None
            self.setAlgo(1)
            self.shortestAllDataTime = []
            self.pathLength = []
            
            """Atributes Csv files to stock data"""
            self.shortestTimeFile = CsvFile(self.targetPath+"/calculateData/ShortestTime.csv")
            self.lengthPathFile = CsvFile(self.targetPath+"/calculateData/ShortestPathLength.csv")
        else:
            print 'dataId does not exist'



        
        
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
                shortestTime [int(src)][int(dst)] = self.dataToCalculate[src].routingPath[dst].value
        return shortestTime



    # New function changed nbprobes by pathLength
    def shortestTimePathLength (self):
        """calculate hops in the shortest path"""
        indexes = list(self.dataToCalculate.keys())
        pathLength =[[0 for dst in range(self.nbprobes)] for src in range(self.nbprobes)]
        for src in indexes:
            for dst in indexes:
                pathLength [int(src)][int(dst)] = len(self.dataToCalculate[src].routingPath[dst].path)-1
        return pathLength

    def shortestPathDicts(self, data, dataOriginal, pathDict, timeListDict, diffPercentListDict):
        '''
        genrate a dictionary pathDict for shortest route path whose value is nbTimes appear
        genrate a dictionary timeListDict for shortest route path whose value is a list of time
        genrate a dictionary diffPercentListDict for shortest route path whose value is a list of diffPercent
        pathDict Structure Exemple:
        { "1-2":[{"1-3-2": 56},
                 {"1-7-8-2": 146}
                  ...
                ]

          "1-3":[{"1-2-3": 56},
                 {"1-7-8-3": 146}
                  ...
                ]
          ...
        }
        timeListDict Structure Exemple:
        { "1-2":[{"1-3-2": [125.98467(ms), 145.39448(ms), 135.39448(ms), .... ]},
                 {"1-7-8-2":[125.98467(ms), 145.39448(ms), 135.39448(ms), .... ] }
                  ...
                ]

          "1-3":[{"1-2-3": [125.98467(ms), 145.39448(ms), 135.39448(ms), .... ]},
                 {"1-7-8-3": [125.98467(ms), 145.39448(ms), 135.39448(ms), .... ]}
                  ...
                ]
          ...
        }
        timeListDict Structure Exemple:
        { "1-2":[{"1-3-2": [2(%), 35(%), 2(%), .... ]},
                 {"1-7-8-2":[2(%), 35(%), 2(%), .... ] }
                  ...
                ]

          "1-3":[{"1-2-3": [2(%), 35(%), 2(%), .... ]},
                 {"1-7-8-3": [2(%), 35(%), 2(%), .... ]}
                  ...
                ]
          ...
        }
        
        '''
        indexes = list(data.keys())
        for i in indexes:
            for j in indexes:
                if dataOriginal[int(i)][int(j)] != None and dataOriginal[int(i)][int(j)]>0 and dataOriginal[int(i)][int(j)]<2000:
                    if len(data[i].routingPath[j].path)>1:
                        path = str(data[i].routingPath[j].path)
                        value = data[i].routingPath[j].value
                       
                        diffPercent = ((dataOriginal[int(i)][int(j)]-value)*100.)/dataOriginal[int(i)][int(j)]
                        '''
                        print 'enter'
                        print dataOriginal[int(i)][int(j)]
                        print value
                        print dataOriginal[int(i)][int(j)]-value
                        print (dataOriginal[int(i)][int(j)]-value)/dataOriginal[int(i)][int(j)]
                        print diffPercent
                        '''
                        if i + "-" + j in pathDict:
                            pathList =  pathDict[i + "-" + j]
                            #indexTuple return a tuple (index in the list, {key is the path:value is nbTimes})
                            indexTuple = next(((i, d) for i, d in enumerate(pathList) if path in d), None)
                            if indexTuple:
                                pathDict[i + "-" + j][indexTuple[0]][path] += 1
                                timeListDict[i + "-" + j][indexTuple[0]][path].append(value)
                                diffPercentListDict[i + "-" + j][indexTuple[0]][path].append(diffPercent)
                            else:
                                pathDict[i + "-" + j].append({path:1})
                                timeListDict[i + "-" + j].append({path:[value,]})
                                diffPercentListDict[i + "-" + j].append({path:[diffPercent,]})                              
                        else:
                            pathDict[i + "-" + j] = [{path:1}]
                            timeListDict[i + "-" + j] = [{path:[value,]}]
                            diffPercentListDict[i + "-" + j] = [{path:[diffPercent,]}]
        return pathDict, timeListDict, diffPercentListDict

    
    def shortestPathOneDict(self, pathDict, timeListDict, diffPercentListDict):
        '''
        genrate dictionary for shortest route path whose value is a dictionary of the path information
        pathDict Structure Exemple:
        { "1-2":[{"1-3-2": {"nbtimes":56, "meanTime": 125.973888(ms), "meanDiffPercent": 25.88(%) }},
                 {"1-7-8-2": {"nbtimes":56, "meanTime": 125.973888(ms), "meanDiffPercent": 25.88(%) }}
                  ...
                ]

          "1-3":[{"1-2-3": {"nbtimes":56, "meanTime": 125.973888(ms), "meanDiffPercent": 25.88(%) }},
                 {"1-7-8-3": {"nbtimes":56, "meanTime": 125.973888(ms), "meanDiffPercent": 25.88(%) }}
                  ...
                ]
          ...
        }
        '''
        informationDict = copy.deepcopy(pathDict)
        for src in range (self.nbprobes):
            for dst in range (self.nbprobes):
                link = str(src) + "-" + str(dst)
                if link in informationDict:
                    for i in range (len(informationDict[link])):
                        for path in informationDict[link][i].keys():
                            informationDict[link][i][path] = {}
                            meanDiffPercent = np.mean(diffPercentListDict[link][i][path])
                            meanTime = np.mean(timeListDict[link][i][path])
                            nbTimes = pathDict[link][i][path]
                            informationDict[link][i][path]["nbtimes"] = nbTimes
                            informationDict[link][i][path]["meanTime"] = meanTime
                            informationDict[link][i][path]["meanDiffPercent"] = meanDiffPercent
        return informationDict


    def output_log_file(self, data, shortestRouteFile):
        '''
        write shortest routes in a the file log
        as form:
        15:49:38 22/09/2016
        11-13 : ['11', '9', '13']time:54.1942908
        11-12 : ['11', '9', '13', '12']time:369.0143748
        ...
        15:49:38 22/09/2016
        11-13 : ['11', '9', '13']time:54.1942908
        11-12 : ['11', '9', '13', '12']time:369.0143748
        ...
        ...
        ...
        '''
        f = open(shortestRouteFile, "a")
        log = (datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y") + "\n") # boundary between two measures
        indexes = list(data.keys())
        for i in indexes:
            for j in indexes:
                if len(data[i].routingPath[j].path) > 2:
                    log += (
                        i + "-" + j + " : " + str(data[i].routingPath[j].path) +'time:'+str(data[i].routingPath[j].value)+ "\n")
        log +="\n"
        f.write(log)
        f.close()


    def caculateAllData(self):
        """ Calculate the shortest route for all data """
        if os.path.exists("ShortestRoute"):
            os.remove("ShortestRoute")
        pathDict = {}
        timeListDict = {}
        diffPercentListDict = {}
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
            #Calculate pathDict, timeListDict, diffPercentListDict
            pathDict, timeListDict, diffPercentListDict = self.shortestPathDicts(self.dataToCalculate, 
                                                                                 dataBefore, 
                                                                                 pathDict, 
                                                                                 timeListDict, 
                                                                                 diffPercentListDict)
            #Write shortest routes in a file 
            #self.output_log_file(self.dataToCalculate, self.targetPath+"/calculateData/ShortestRoute")
            
        #claculate timeMeanDict 
        informationDict = self.shortestPathOneDict(pathDict, timeListDict, diffPercentListDict)
        """ write data into files """ 
        self.shortestTimeFile.write_data(self.shortestAllDataTime)
        self.lengthPathFile.write_data(self.pathLength)
        """ write pathDict into json file""" 
        with open (self.targetPath+"/calculateData/informationDictResult.json", "w") as fs:
            json.dump(informationDict, fs)
       


################################################################
########---------------    main   ---------------------#########
################################################################

if __name__ == "__main__":
    #log_files = [f for f in os.listdir(path) if f.endswith('.log')]
    """ data original """
    #dataAll = read_data(log_files[0])
    myRtt = RttShortest('20160808_161300')
    #write_data(dataAll, "rtt_data.csv")
    """create fiveDaysData"""
    #fiveDaysData = copy.deepcopy (dataAll [118*19 : -118*19])
    #write_data(fiveDaysData, "fiveDaysData.csv")
    """calculate shortest path time for all data"""
    myRtt.caculateAllData()
    #caculateOneDayData("fiveDaysData.csv", "shortestOneDayTime.csv",
    #                   "oneDayData.csv", "oneDayPathLength.csv", 0)





       



                

