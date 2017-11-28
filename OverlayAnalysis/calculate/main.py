import os

from rttShortest import *
from rttShortest import RttShortest
from rttCalculateToShow import *
from rttCalculateToShow import RttCalculateToShow
from rttDisplayPlugins import *
from rttDisplayPlugins import RttDisplay

import pdb


if __name__ == "__main__":

    path = '/'.join(os_path.abspath(os_path.split(__file__)[0]).split('/')[:-1]) + '/data'
    os.chdir(path)

    dataID = "20160808_161300"

    # calculate shortest time and information for shortest route path, calculation for shortest path used imported from rttShortest.py
    csvFilesList = [dataID +"/calculateData/ShortestPathLength.csv", dataID+"/calculateData/ShortestTime.csv", dataID+"/calculateData/informationDictResult.json"]
    filesExist = [f for f in csvFilesList if (os.path.isfile(f) and os.path.getsize(f)>0)]
    filesNoExist = list(set(filesExist)^set(csvFilesList))
    if filesNoExist:
        myRtt = RttShortest(dataID)
        myRtt.caculateAllData()
    else:
        print "csv files exist"
   
    
    # calculate to show, calculation function used imported from rttCalculateToShow.py
    jsonfilesList = [dataID+'/output/AllData.json', dataID+"/output/ShortestTime.json", dataID+"/output/ShortestPathLength.json", dataID+'/output/DiffPercent.json', dataID+'/output/MaxdiffPercent.json', dataID+'/output/MindiffPercent.json', dataID+'/output/MeandiffPercent.json', dataID+'/output/MeanDelay.json', dataID+'/output/MeanShortestDelay.json', dataID+'/output/information.json' ]
    filesExist = [f for f in jsonfilesList if (os.path.isfile(f) and os.path.getsize(f)>0)]
    filesNoExist = list(set(filesExist)^set(jsonfilesList))
    if filesNoExist:
        myRttCalculateToShow = RttCalculateToShow(dataID)
        """transform all data into three dimensions array list as rtt2[index of time][src][dst]"""
        rtt2AllData = data3D(myRttCalculateToShow.allData, myRttCalculateToShow.nbprobes, myRttCalculateToShow.nbtimes)
        rtt2ShortestAllDataTime = data3D(myRttCalculateToShow.shortestAllDataTime, myRttCalculateToShow.nbprobes, myRttCalculateToShow.nbtimes)
        rtt2PathLength = data3D(myRttCalculateToShow.pathLength, myRttCalculateToShow.nbprobes, myRttCalculateToShow.nbtimes)
        """transform all data into three dimensions array list as rtt3[src][dst][index of time]"""
        rtt3AllData = data3D2(rtt2AllData, myRttCalculateToShow.nbprobes, myRttCalculateToShow.nbtimes)
        rtt3ShortestAllDataTime = data3D2(rtt2ShortestAllDataTime, myRttCalculateToShow.nbprobes, myRttCalculateToShow.nbtimes)
        rtt3PathLength = data3D2(rtt2PathLength, myRttCalculateToShow.nbprobes, myRttCalculateToShow.nbtimes)
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
        
        if dataID+'/output/information.json' in filesNoExist:
            linkNoValide = []
            for src in range (myRttCalculateToShow.nbprobes):
                for dst in range (myRttCalculateToShow.nbprobes):
                    if np.ma.count(rtt3AllDataNew[src][dst])==0 and src != dst:
                        linkNoValide.append(str(src)+"-"+str(dst))

            """write data information (nbProbes, nbTimes) into a json file"""
            info = dict()
            info['nbProbes'] = myRttCalculateToShow.nbprobes
            info['nbTimes'] = myRttCalculateToShow.nbtimes
            info['Total non-valid measures (%) '] = str(float(np.ma.count_masked(rtt3AllDataNew))/(np.ma.count(rtt3AllDataNew)+np.ma.count_masked(rtt3AllDataNew))*100)
            info['Mean Improvement (%) '] = str(getMeanImprovement(rtt3DiffPercentNew))
            info['No valide measure links'] = linkNoValide
            print os.getcwd()
            with open(dataID +'/output/information.json', 'w') as fp:
                json.dump(info, fp)

        """Save data into corresponding json files """
        if dataID+'/output/AllData.json' in filesNoExist:
            myRttCalculateToShow.rtt3AllDataFile.write_data(rtt3AllDataNew)
        if dataID+'/output/ShortestTime.json' in filesNoExist:
            myRttCalculateToShow.rtt3ShortestTimeFile.write_data(rtt3ShortestAllDataTimeNew)
        if dataID+'/output/ShortestPathLength.json' in filesNoExist:
            myRttCalculateToShow.rtt3LengthPathFile.write_data(rtt3PathLengthNew)
        #if dataID+'/output/DiffPercent.json' in filesNoExist:
            #myRttCalculateToShow.rtt3DifferenceFile.write_data(rtt3DifferenceNew)
        if dataID+'/output/DiffPercent.json' in filesNoExist:
            myRttCalculateToShow.rtt3DiffPercentFile.write_data(rtt3DiffPercentNew) 
        if dataID+'/output/MaxdiffPercent.json' in filesNoExist:        
            myRttCalculateToShow.rtt3MaxdiffPercentFile.write_data(rtt3MaxdiffPercent)
        if dataID+'/output/MindiffPercent.json' in filesNoExist:
            myRttCalculateToShow.rtt3MindiffPercentFile.write_data(rtt3MindiffPercent)
        if dataID+'/output/MeandiffPercent.json' in filesNoExist: 
            myRttCalculateToShow.rtt3MeandiffPercentFile.write_data(rtt3MeanDiffPercent)
        if dataID+'/output/MeanDelay.json' in filesNoExist:
            myRttCalculateToShow.rtt3MeanShortestDelayFile.write_data(rtt3MeanDelay)
        if dataID+'/output/MeanShortestDelay.json' in filesNoExist:
            myRttCalculateToShow.rtt3MeanDelayFile.write_data(rtt3MeanShortestDelay)
    else:
        print "json files exist"


    #generate html graphs, display functions used imported from rttDisplayPlugins.py
    myRttDisplay = RttDisplay(dataID)
    print('Total non-valid measures (%) '+ myRttDisplay.info['Total non-valid measures (%) '])
    print('Mean Improvement (%) '+ myRttDisplay.info['Mean Improvement (%) '])
    
    """Load data from json files"""
    rtt3AllDataNew = myRttDisplay.rtt3AllDataFile.read_data()
    rtt3ShortestAllDataTimeNew = myRttDisplay.rtt3ShortestTimeFile.read_data()
    rtt3PathLengthNew = myRttDisplay.rtt3LengthPathFile.read_data()
    #rtt3DifferenceNew = myRttDisplay.rtt3DifferenceFile.read_data()
    rtt3DiffPercentNew = myRttDisplay.rtt3DiffPercentFile.read_data()
    """Load data from json files"""
    rtt3MaxDiffPercent = myRttDisplay.rtt3MaxdiffPercentFile.read_data()
    rtt3MinDiffPercent = myRttDisplay.rtt3MindiffPercentFile.read_data()                     
    rtt3MeanDiffPercent = myRttDisplay.rtt3MeandiffPercentFile.read_data()
    rtt3MeanDelay = myRttDisplay.rtt3MeanDelayFile.read_data()
    rtt3MeanShortestDelay = myRttDisplay.rtt3MeanShortestDelayFile.read_data()

    """Shortest path information plot"""
    with open (dataID +"/calculateData/informationDictResult.json", "r") as fs:
        print 'enter read'
        informationDict = json.load(fs)
    
    
    #showPathInformation(13, 18, informationDict, myRttDisplay.picturesPath, myRttDisplay.htmlPath)#no valide measure for this link
    #showPathInformation(19, 5, informationDict, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showPathInformation(7, 6, informationDict, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showPathInformation(3, 11, informationDict, myRttDisplay.picturesPath, myRttDisplay.htmlPath)#no valide measure for this link 

    """generate fix graphs for app"""
    #showMatrixMeanDelays(rtt3MeanDelay, rtt3MeanShortestDelay, myRttDisplay.nbProbes,myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showMatrixDiffRtt(rtt3DiffPercentNew, myRttDisplay.nbProbes, rtt3MaxDiffPercent, rtt3MinDiffPercent, rtt3MeanDiffPercent, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showMatrixDiffRttMinRttPathLength(rtt3ShortestAllDataTimeNew, rtt3AllDataNew, rtt3PathLengthNew, rtt3DiffPercentNew,myRttDisplay.nbProbes, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showMatrixCovRtt(rtt3ShortestAllDataTimeNew ,myRttDisplay.nbProbes , myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showHistoDifPercent(rtt3DiffPercentNew, "all data", myRttDisplay.nbProbes, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showHistoPathLengthAllCouples(rtt3PathLengthNew, "all data", myRttDisplay.nbProbes, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showCumulativenbTimesPercentDifRTT(rtt3DiffPercentNew, myRttDisplay.nbProbes, myRttDisplay.picturesPath, myRttDisplay.htmlPath)    
    #showCumulativeNbcouplesPercentDifRTT(rtt3MeanDiffPercent, rtt3MaxDiffPercent, rtt3MinDiffPercent, myRttDisplay.nbProbes, myRttDisplay.picturesPath, myRttDisplay.htmlPath)

    """test chnageable graphs for app with different src or dest"""
    showDefaultTime(rtt3AllDataNew, 8, 12, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    showHistoDefaultTime(rtt3AllDataNew, 8, 12, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    ##shortest route graphs for one link
    showDefaultTimeShortestTime(rtt3AllDataNew, rtt3ShortestAllDataTimeNew, 8, 12, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    showPathLength(rtt3PathLengthNew, 8, 12, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    showHistoPathLength(rtt3PathLengthNew, 8, 12, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    plotSrcFixedForVisu(rtt3MinDiffPercent, rtt3MeanDiffPercent, rtt3MaxDiffPercent, 8, myRttDisplay.nbProbes, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    showPathInformation(8, 12, informationDict, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    

    """test old function,  not for app"""
    #plotSrcFixed(rtt3DiffPercentNew, rtt3MeanDiffPercent, 8, myRttDisplay.nbProbes, myRttDisplay.picturesPath, myRttDisplay.htmlPath)



