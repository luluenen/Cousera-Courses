#!/usr/bin/python3
import os
from os import path as os_path
import sys
import csv
import copy
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json

path = []
path = os.path.abspath(os.path.join(os.path.dirname(__file__), './fileTools/'))
if not path in sys.path:
    sys.path.insert(1, path)
"""Import classes created"""
from csvFile import CsvFile 
from jsonFile import JsonFile

# Changes the current working directory to the parent of parent directory of the file (analysis_data)
if __name__ == "__main__":
    path = '/'.join(os_path.abspath(os_path.split(__file__)[0]).split('/')[:-1]) + '/data'
    os.chdir(path)
    print (path)

class RttCalculateToShow:
    """
    Claas Rtt calculates the shortest route belong to the file name given who has attributs
    @self.inputFname: name of input data file where original data saved
    @self.shortestTimeFname: name of data output file to save shortest path time  
    @self.lengthPathFname: name of data output file to save length of shortest path (nomber of hops)
    @self.targetPath: folder path to save data  
    """
    def __init__(self, dataID):
        self.dataID = dataID
        self.inputFname = ''.join(dataID) + '.csv' 
        self.folderName = self.dataID
        "Change courrent working directory to the folder of dataID"
        path = []
        path = ''.join(os.getcwd()) + '/'+ ''.join (self.folderName)
        self.targetPath = path
        if os.path.exists(self.targetPath):       
            #Check jsonData path dose not exists then creat a new folder 
            self.jsonFolder = self.targetPath + '/output'
            if not os.path.exists(self.jsonFolder):
                os.makedirs(self.jsonFolder)
            f1 = CsvFile(''.join(self.targetPath)+'/'+''.join(self.inputFname))
            self.allData = f1.read_dataCsv()
            self.nbprobes = int(len(self.allData[0]))
            self.nbtimes = int (len(self.allData)/len(self.allData[0]))
            self.shortestTimeFname = self.targetPath +"/calculateData/ShortestTime.csv"
            self.lengthPathFname = self.targetPath + "/calculateData/ShortestPathLength.csv"
            f2 = CsvFile(self.shortestTimeFname)
            self.shortestAllDataTime = f2.read_dataCsv()
            f3 = CsvFile(self.lengthPathFname)
            self.pathLength = f3.read_dataCsv()
        
            """Atributes json files to stock data to display """
            self.rtt3AllDataFile = JsonFile( self.targetPath +'/output/AllData.json')
            self.rtt3ShortestTimeFile = JsonFile( self.targetPath + "/output/ShortestTime.json")
            self.rtt3LengthPathFile = JsonFile( self.targetPath+"/output/ShortestPathLength.json")
            #self.rtt3DifferenceFile = JsonFile('jsonData/Difference.json')
            self.rtt3DiffPercentFile = JsonFile(self.targetPath+'/output/DiffPercent.json')
            self.rtt3MaxdiffPercentFile = JsonFile(self.targetPath+'/output/MaxdiffPercent.json')
            self.rtt3MindiffPercentFile = JsonFile(self.targetPath+'/output/MindiffPercent.json')
            self.rtt3MeandiffPercentFile = JsonFile(self.targetPath+'/output/MeandiffPercent.json')
            self.rtt3MeanDelayFile = JsonFile(self.targetPath+'/output/MeanDelay.json')
            self.rtt3MeanShortestDelayFile = JsonFile(self.targetPath+'/output/MeanShortestDelay.json')

        else:
            print ("dataID does not exist")



def data3D(data,nbprobes,nbtimes):
    '''
    Transform data to 3 dimensional matrix in which second and third corespond to first (src) and second (dst) node, the first dimension is the time
    @param data: a list or a array list of lists  
    @param nbprobes: number of nodes
    @param nbtimes: number of times
    @return: rtt2 is a 3 dimensional matrix in which second and third corespond to first (src) and second (dst) node the first dimention is the time
    '''
    if type(data) is not np.ndarray:
        newData = np.array(data) 
        rtt2 = newData.reshape((nbtimes,nbprobes,nbprobes))
    else:
        rtt2 = data.reshape((nbtimes,nbprobes,nbprobes))
    return rtt2

    
def data3D2(rtt3,nbprobes,nbtimes):
    '''
    Transform data to 3 dimensional matrix in which first and second corespond to first (src) and second (dst) node, the third dimension is the time
    @param data: a list or a array list of lists  
    @param nbprobes: number of nodes
    @param nbtimes: number of times
    @return: rtt3 is a 3 dimensional matrix in which first and second corespond to first (src) and second (dst) node the third dimention is the time
    '''
    rtt3New = np.zeros((nbprobes, nbprobes, nbtimes))
    for t in range(nbtimes):
        rtt3New[:,:,t] = rtt3[t,:,:]
    return rtt3New


def getImprovement(rtt3Difference,rtt3AllData):
    '''Returns a new array expressing the percentage of improvements, element wise
    @param rtt3Difference: differences with the reference value
    @type rtt3Difference: list
    @param rtt3AllData: reference values 
    @type rtt3AllData: list    
    @return the percentage of rtt3Difference with respect to rtt3AllData, element wise 
    @rtype: numpy array 
    '''
    percentage=np.divide(np.array(rtt3Difference)*100,np.array(rtt3AllData))
    return percentage



def getMeanImprovement(diffRTTPercent3):
    '''Returns the mean value of diffRTTPercent3 without considering masked values and without considering thode values where the improvement is zero.
    @param diffRTTPercent3: the data to be averaged
    @type diffRTTPercent3: numpy masked array
    @return the mean value of the input parameter without considerng masked values and excluding values equal to 0 
    @rtype: folat 
    '''
    #condition* have elements in True if data is valid
    condition1=np.ma.getdata(diffRTTPercent3)!=0.0
    old_mask=np.ma.getmask(diffRTTPercent3)
    condition=~old_mask & condition1
    new_ma=np.ma.array(np.ma.getdata(diffRTTPercent3), mask=~condition)
    return np.ma.mean(new_ma)


def getMaskedArray(referenceData, data1, errorValues):
    '''Returns a new masked array where the data is data1 and the mask is set such that valid values are those where referenceData is not NaN and such that errorValues[1]>referenceData> errorValues[0] 
    @param referenceData: the data against which the mask will be calculated
    @type referenceData: list
    @param data1: the data to be rerturned 
    @type data1: list
    @param errorValues: tuple indicating the exclusive interval within which data is considered valid
    @type errorValues: tuple of float or int    
    @return data data1 masked acording to referenceData and errorValues 
    @rtype: numpy masked array 
    '''
    #condition* have elements in True if data is valid
    condition1=(np.array(referenceData)>np.ones(np.shape(referenceData))*errorValues[0])
    condition2=(np.array(referenceData)<np.ones(np.shape(referenceData))*errorValues[1])
    condition3=~np.isnan(referenceData)
    condition4=~np.isnan(data1)     
    mask=(condition1 & condition2 & condition3 & condition4) 
    a = np.ma.array(np.array(data1), mask=~mask)
    return a



####################################################################################################
#########################################  main  ###################################################
####################################################################################################
if __name__ == "__main__":

    #####-------------------------------------for all data ---------------------------------------###############
    dataID = "20160808_161300"
    myRttDisplay = RttCalculateToShow(dataID)
    
    """transform all data into three dimensions array list as rtt2[index of time][src][dst]"""
    rtt2AllData = data3D(myRttDisplay.allData, myRttDisplay.nbprobes, myRttDisplay.nbtimes)
    rtt2ShortestAllDataTime = data3D(myRttDisplay.shortestAllDataTime, myRttDisplay.nbprobes, myRttDisplay.nbtimes)
    rtt2PathLength = data3D(myRttDisplay.pathLength, myRttDisplay.nbprobes, myRttDisplay.nbtimes)
        
    """transform all data into three dimensions array list as rtt3[src][dst][index of time]"""
    rtt3AllData = data3D2(rtt2AllData, myRttDisplay.nbprobes, myRttDisplay.nbtimes)
    rtt3ShortestAllDataTime = data3D2(rtt2ShortestAllDataTime, myRttDisplay.nbprobes, myRttDisplay.nbtimes)
    rtt3PathLength = data3D2(rtt2PathLength, myRttDisplay.nbprobes, myRttDisplay.nbtimes)
    rtt3Difference=rtt3AllData-rtt3ShortestAllDataTime
    rtt3DiffPercent=getImprovement(rtt3Difference, rtt3AllData)

    """get the masked arrays according to valid values, replace masked values by -99999"""     
    rtt3AllDataNew=getMaskedArray(rtt3AllData, rtt3AllData,(0,2000))
    #rtt3DifferenceNew=getMaskedArray(rtt3AllData, rtt3Difference,(0,2000))
    rtt3ShortestAllDataTimeNew=getMaskedArray(rtt3AllData, rtt3ShortestAllDataTime,(0,2000))
    rtt3PathLengthNew=getMaskedArray(rtt3AllData, rtt3PathLength,(0,2000))
    rtt3DiffPercentNew=getMaskedArray(rtt3AllData, rtt3DiffPercent,(0,2000))

    """ Calculate maxValues and minValues of rtt3DiffPercent """
    rtt3MaxdiffPercent = np.ma.amax(rtt3DiffPercentNew, axis=2)
    rtt3MindiffPercent = np.ma.amin(rtt3DiffPercentNew, axis=2)
    """calculate meanValues of rtt3DiffPercent """                       
    rtt3MeanDiffPercent = np.ma.mean(rtt3DiffPercentNew, axis=2)

    """ Calculate maxValues and minValues of rtt3AllData """
    rtt3MaxDelay = np.ma.amax(rtt3AllDataNew, axis=2)
    rtt3MinDelay = np.ma.amin(rtt3AllDataNew, axis=2)
    """calculate meanValues of rtt3AllData """                       
    rtt3MeanDelay = np.ma.mean(rtt3AllDataNew, axis=2)

    """ Calculate maxValues and minValues of rtt3ShortestAllDataTimeNew """
    rtt3MaxShortestDelay = np.ma.amax(rtt3ShortestAllDataTimeNew, axis=2)
    rtt3MinShortestDelay = np.ma.amin(rtt3ShortestAllDataTimeNew, axis=2)
    """calculate meanValues of rtt3ShortestAllDataTimeNew """                       
    rtt3MeanShortestDelay = np.ma.mean(rtt3ShortestAllDataTimeNew, axis=2)

    
    
    print('Total non-valid measures (%) '+str(float(np.ma.count_masked(rtt3AllDataNew))/(np.ma.count(rtt3AllDataNew)+np.ma.count_masked(rtt3AllDataNew))*100))

    print('Mean Improvement (%) '+str(getMeanImprovement(rtt3DiffPercentNew)))

    """write data information (nbProbes, nbTimes) into a json file"""
    info = dict()
    info['nbProbes'] = myRttDisplay.nbprobes
    info['nbTimes'] = myRttDisplay.nbtimes
    info['Total non-valid measures (%) '] = str(float(np.ma.count_masked(rtt3AllDataNew))/(np.ma.count(rtt3AllDataNew)+np.ma.count_masked(rtt3AllDataNew))*100)
    info['Mean Improvement (%) '] = str(getMeanImprovement(rtt3DiffPercentNew))
    with open('output/information.json', 'w') as fp:
        json.dump(info, fp)

    """Save data into corresponding json files """
    myRttDisplay.rtt3AllDataFile.write_data(rtt3AllDataNew)
    myRttDisplay.rtt3ShortestTimeFile.write_data(rtt3ShortestAllDataTimeNew)
    myRttDisplay.rtt3LengthPathFile.write_data(rtt3PathLengthNew)
    #myRttDisplay.rtt3DifferenceFile.write_data(rtt3DifferenceNew)
    myRttDisplay.rtt3DiffPercentFile.write_data(rtt3DiffPercentNew) 
    myRttDisplay.rtt3MaxdiffPercentFile.write_data(rtt3MaxdiffPercent)
    myRttDisplay.rtt3MindiffPercentFile.write_data(rtt3MindiffPercent) 
    myRttDisplay.rtt3MeandiffPercentFile.write_data(rtt3MeanDiffPercent)
    myRttDisplay.rtt3MeanShortestDelayFile.write_data(rtt3MeanShortestDelay)
    myRttDisplay.rtt3MeanDelayFile.write_data(rtt3MeanDelay)


    



    


