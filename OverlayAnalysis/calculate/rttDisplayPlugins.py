import os
from os import path as os_path
import sys
import copy
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
import mpld3
from mpld3 import plugins, utils
#import pandas module----sudo pip install pandas
import pandas as pd
from datetime import datetime
import collections


path = []
path = os.path.abspath(os.path.join(os.path.dirname(__file__), './fileTools/'))
if not path in sys.path:
    sys.path.insert(1, path)
"""Import classes created"""
from jsonFile import JsonFile

# Define some CSS to control our custom labels
css = """
table
{
    border-collapse: collapse;
    position: relative;
}
th
{
    color: #ffffff;
    background-color: #cccccc;
}
td
{
    background-color: #ECECEC;
}
table, th, td
{
    font-family:Arial, Helvetica, sans-serif;
    border: 1px solid #ccc;
    text-align: right;
}
"""


# Changes the current working directory to the parent of parent directory of the file (analysis_data)
if __name__ == "__main__":
    path = '/'.join(os_path.abspath(os_path.split(__file__)[0]).split('/')[:-1]) +'/data'
    os.chdir(path)
    print (path)



class RttDisplay:
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
        self.folderName =self.inputFname.split('.')[:-1]
        #Change courrent working directory to the folder of data
        path = []
        path = ''.join(os.getcwd()) + '/'+ ''.join (self.folderName) #FIX ME: / not suitable for all OS --- OK ? 
        self.targetPath = path
        print path
        #Chek path does exist then creat a new folder
        if os.path.exists(self.targetPath):
            #Check data/dataID/pictures and data/dataID/graphs path dose not exists then creat a new folder 
            self.picturesPath = self.targetPath + '/pictures'
            self.htmlPath = self.targetPath + '/graphs'
            if not os.path.exists(self.picturesPath):
                os.makedirs(self.picturesPath)
            if not os.path.exists(self.htmlPath):
                os.makedirs(self.htmlPath)
            # Read information file
            with open(self.targetPath+'/output/information.json', 'r') as fp:
                self.info = json.load(fp)
            self.nbProbes = self.info['nbProbes']
            self.nbTimes = self.info['nbTimes']
            print self.targetPath +'/output/AllData.json'
            """Attributes json files to read data """
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
            print 'dataID does not exist'


        
# DONE
def showHistoDifPercent(rtt3DifPercent, title, nbProbes, picturesPath, htmlPath):
    '''
    show histogram of vector for dif/direct time expresed by percentage where it contents all measurement values for all couples 
    @param rtt3DifPercent: contents all measurement values for all couples diference between shortest time and direct tiome divided by direct time expressed en percentage
    for every couple probes during a period mesurement
    @type rtt3DifPercent: numpy masked array
    @title: title of the histogram
    @type title: string
    @param nbProbes: number of probes in total
    @type nbProbes: int
    '''
    #Javascript class for histograms
    class BarLabelToolTip(plugins.PluginBase):    
        JAVASCRIPT = """
        mpld3.register_plugin("barlabeltoolTip", BarLabelToolTip);
        BarLabelToolTip.prototype = Object.create(mpld3.Plugin.prototype);
        BarLabelToolTip.prototype.constructor = BarLabelToolTip;
        BarLabelToolTip.prototype.requiredProps = ["ids","labels"];
        BarLabelToolTip.prototype.defaultProps = {
            hoffset: 0,
            voffset: 10,
            location: 'mouse'
        };
        function BarLabelToolTip(fig, props){
            mpld3.Plugin.call(this, fig, props);
        };

        BarLabelToolTip.prototype.draw = function(){
            var svg = d3.select("#" + this.fig.figid);
            var objs = svg.selectAll(".mpld3-path");
            var loc = this.props.location;
            var labels = this.props.labels

            test = this.fig.canvas.append("text")
                .text("hello world")
                .style("font-size", 72)
                .style("opacity", 0.5)
                .style("text-anchor", "middle")
                .attr("x", this.fig.width / 2)
                .attr("y", this.fig.height / 2)
                .style("visibility", "hidden");

            function mousemove(d) {
                if (loc === "mouse") {
                    var pos = d3.mouse(this.fig.canvas.node())
                    this.x = pos[0] + this.props.hoffset;
                    this.y = pos[1] - this.props.voffset;
                }

                test
                    .attr("x", this.x)
                    .attr("y", this.y);
            };

            function mouseout(d) {
                test.style("visibility", "hidden")
            };

            this.props.ids.forEach(function(id, i) {


                var obj = mpld3.get_element(id);

                function mouseover(d) {
                    test.style("visibility", "visible")
                        .style("font-size", 24)
                        .style("opacity", 0.7)
                        .text(labels[i])
                };

                obj.elements().on("mouseover", mouseover.bind(this))

            });

           objs.on("mousemove", mousemove.bind(this)) 
               .on("mouseout", mouseout.bind(this));     

        }       
        """
        def __init__(self, ids, labels=None, location="mouse"):

            self.dict_ = {"type": "barlabeltoolTip",
                          "ids": ids,
                          "labels": labels,
                          "location": location}
        
    f=plt.figure()
    ax = f.add_subplot(111)
    total_valid_values= np.ma.count(rtt3DifPercent)
    weights = (~np.ravel(np.ma.getmask(rtt3DifPercent))).astype(int)/float(total_valid_values)
    data = np.ma.ravel(rtt3DifPercent)
    bins = np.linspace(0, 100, 21)
    probilities, bins, patches = ax.hist(data, weights=weights,bins=bins,facecolor='b', label = 'Histogram')
    ax.set_ylabel("Measurement Epochs for all Origin-Destination Couples (%)")
    ax.set_xlabel("Improvement (%)")
    ax.set_xlim([0, np.ma.max(data)+5])
    ax.grid(True)  
    #ax.set_title("Distribution of delay improvement expresed in percentage (%) for " + title )

    
    # add plot cumulative probility
    bincenters = 0.5*(bins[1:]+bins[:-1])
    y = np.around(probilities.cumsum(),3)
    points1 = ax.plot(bincenters, y, '--', marker='o', label = 'Cumulative'  )
    plt.legend(loc='center right')
    #plt.draw()
    #f.show()
    # to save image
    #f.savefig(picturesPath + '/histoDifPercent.eps')

    # add plugis for probilities
    labelsBinCenters = [round(bar.get_height(),2) for bar in patches]
    ids = [utils.get_id(bar) for bar in patches]
    plugins.connect(f, BarLabelToolTip(ids, labelsBinCenters))
    
    # add plugins for cumulative plot 
    labels = []
    df = pd.DataFrame(index=range(len(bincenters)))
    df['x'] = bincenters
    df['y'] = y
    for i in range(len(bincenters)):
        label = df.ix[[i], :].T
        label.columns = ['Points {0} '.format(i+1)]
        # .to_html() is unicode; so make leading 'u' go away with str()
        labels.append(str(label.to_html()))

    tooltip = plugins.PointHTMLTooltip(points1[0], labels,
                                       voffset=10, hoffset=10, css=css)
    mpld3.plugins.connect(f, tooltip)

    mpld3.save_html(f, htmlPath+'/histoDifPercentCumulativeImprovement.html')
    
    #mpld3.show()



# DONE
def showHistoPathLengthAllCouples(shortestPathLength, title, nbProbes, picturesPath, htmlPath ):
    """
    show histogram of vector for shortest path Length
    @param shortestPathLength: contents all data of shortest path length calculated for every couple probes during a period mesurement
    @type shortestPathLength: numpy masked array
    @title: title of the histogram
    @type title: string
    @param nbProbes: number of probes in total
    @type nbProbes: int

    """
    class BarLabelToolTip(plugins.PluginBase):    
        JAVASCRIPT = """
        mpld3.register_plugin("barlabeltoolTip", BarLabelToolTip);
        BarLabelToolTip.prototype = Object.create(mpld3.Plugin.prototype);
        BarLabelToolTip.prototype.constructor = BarLabelToolTip;
        BarLabelToolTip.prototype.requiredProps = ["ids","labels"];
        BarLabelToolTip.prototype.defaultProps = {
            hoffset: 0,
            voffset: 10,
            location: 'mouse'
        };
        function BarLabelToolTip(fig, props){
            mpld3.Plugin.call(this, fig, props);
        };

        BarLabelToolTip.prototype.draw = function(){
            var svg = d3.select("#" + this.fig.figid);
            var objs = svg.selectAll(".mpld3-path");
            var loc = this.props.location;
            var labels = this.props.labels

            test = this.fig.canvas.append("text")
                .text("hello world")
                .style("font-size", 72)
                .style("opacity", 0.5)
                .style("text-anchor", "middle")
                .attr("x", this.fig.width / 2)
                .attr("y", this.fig.height / 2)
                .style("visibility", "hidden");

            function mousemove(d) {
                if (loc === "mouse") {
                    var pos = d3.mouse(this.fig.canvas.node())
                    this.x = pos[0] + this.props.hoffset;
                    this.y = pos[1] - this.props.voffset;
                }

                test
                    .attr("x", this.x)
                    .attr("y", this.y);
            };

            function mouseout(d) {
                test.style("visibility", "hidden")
            };

            this.props.ids.forEach(function(id, i) {


                var obj = mpld3.get_element(id);

                function mouseover(d) {
                    test.style("visibility", "visible")
                        .style("font-size", 24)
                        .style("opacity", 0.7)
                        .text(labels[i])
                };

                obj.elements().on("mouseover", mouseover.bind(this))

            });

           objs.on("mousemove", mousemove.bind(this)) 
               .on("mouseout", mouseout.bind(this));     

        }       
        """
        def __init__(self, ids, labels=None, location="mouse"):

            self.dict_ = {"type": "barlabeltoolTip",
                          "ids": ids,
                          "labels": labels,
                          "location": location}
            
    """make percentage values into one dimension vector, delete cases where src = dst"""
    f=plt.figure()
    ax = f.add_subplot(111)
    total_valid_values= np.ma.count(shortestPathLength)
    weights = (~np.ravel(
        np.ma.getmask(shortestPathLength))).astype(int)/float(total_valid_values)
    data = np.ma.ravel(shortestPathLength)
    bins = np.linspace(0, 10,11)
    probilities, bins, patches = ax.hist(data,
                                         weights=weights,
                                         bins=bins,
                                         facecolor='b',align='left',
                                         label = 'Histogram')

    ax.set_ylabel("Measurement Epochs for all Origin-Destination Couples (%)")
    ax.set_xticks(bins[:-1])
    ax.set_xlabel("Path length")
    ax.set_xlim([0, bins[-1]+1])
    ax.grid(True)

    # add plot bincenters
    bincenters = bins[1:-1]
    y = np.around(probilities[1:].cumsum(),3)
    points1 = ax.plot(bincenters, y, '--', marker='o', label = 'Cumulative')
    plt.legend(loc='center right')
    
    #plt.draw() 
    # to save image
    #f.savefig(picturesPath + '/histoPathLength.eps')
    #f.show()

    # add plugins for probilities
    labelsBinCenters = [round(bar.get_height(),2) for bar in patches]
    ids = [utils.get_id(bar) for bar in patches]
    plugins.connect(f, BarLabelToolTip(ids, labelsBinCenters))
    
    # add plugins for cumulative plot 
    labels = []
    df = pd.DataFrame(index=range(len(bincenters)))
    df['x'] = bincenters
    df['y'] = y
    for i in range(len(bincenters)):
        label = df.ix[[i], :].T
        label.columns = ['Points {0} '.format(i+1)]
        # .to_html() is unicode; so make leading 'u' go away with str()
        labels.append(str(label.to_html()))    
    
    tooltip = plugins.PointHTMLTooltip(points1[0], labels,
                                       voffset=10, hoffset=10, css=css)
    mpld3.plugins.connect(f, tooltip)

    mpld3.save_html(f, htmlPath+'/histoPathLength.html')
    #mpld3.show()



    

# Replace by showHistoDifPerccent
def showCumulativenbTimesPercentDifRTT(rtt3DifPercent, nbProbes, picturesPath, htmlPath):
    '''
    This function shows the chart of the cumulative relation nbTimes(%)-difPercentage(%)
    That means the cumulative relation between the number of times (measurements) where the
    delay difference between the shortest path and the direct one is less than a given value.
    All quantities are expressed in percentage.  

    @param difPercent: contents all percentages of difference(all difference values of all links concatenated),
    the difference is between the direct link and the shortest path, expresed as a percentage of
    the delay of the direct link which is a 3 dimensional matrix in which first and second corespond to first (src) and second (dst) node
    the third dimension is shortestPathLength of  

    @type difPercent: 3 dimensional matrix
    '''
    """Make percentage values into one dimension vector"""
    f=plt.figure()
    ax = f.add_subplot(111)
    difPercent = np.ma.ravel(rtt3DifPercent)
    nbValues = np.ma.count(difPercent)
    percentCompressed = difPercent.compressed()
    sortDifPercent = np.ma.sort(percentCompressed)
    probility = np.array(range(nbValues))*100/float(nbValues)
    lines = points = ax.plot(
        sortDifPercent, probility, linewidth = 5.0, marker = ".",
        markeredgewidth=0.05, label='Cumulative relation of nbTimes(%) and PercentDiference(%)')
    ax.set_ylabel("probility of nbTimes (%)")
    ax.set_xlabel("difference/direct path time (%)")
    ax.set_xlim([0, 100])
    ax.set_ylim([0, 100])
    ax.set_title("Cumulative relation of nbTimes(%) and PercentDiference(%)" )

    #plt.draw()
    # to save image
    #f.savefig(picturesPath +'/CumulativeNbTimesPercentDifRTT.eps')
    #f.show()

    # add plugins
    labels = np.around(np.column_stack((sortDifPercent, probility)), 3)
    tooltip = mpld3.plugins.PointLabelTooltip(lines[0],labels=labels.tolist())
    mpld3.plugins.connect(f, tooltip)
    mpld3.save_html(f, htmlPath+'/CumulativeNbTimesPercentDifRTT.html')
    #mpld3.show()

    
    
#DONE  
def showCumulativeNbcouplesPercentDifRTT(rtt3MeanDifPercent, rtt3MaxDifPercent, rtt3MinDifPercent, nbProbes, picturesPath, htmlPath):
    '''
    This function shows three charts. The cumulative relations of 
    nbCouples(%)-meanDifPercent(%) nbCouples(%)-maxDifPercent(%), nbCouples(%)-minDifPercent(%) in one figure.
    
    @param meanDifPercent:     contents mean values of percentage of difference of all couples of probes,
    the difference is between the direct link and the shortest path, expresed as a percentag of the delay
    of the direct link. 2 dimentional matrix in which first and second corespond to first (src) and second (dst) node

    @type meanDifPercent:     2 dimentional matrix

    @param maxDifPercent:     2 dimentional matrix(first and second corespond to first (src) and second (dst) node)
    of maximum values of percentage of difference of all couples of probes

    @type maxDifPercent:      2 dimentional matrix

    @param minDifPercent:     2 dimentional matrix(first and second corespond to first (src) and second (dst) node)
    of minimum values of percentage of difference of all couples of probes

    @type minDifPercent:      2 dimentional matrix
    '''
    print 'enter cumulative nbcouples'

    # make mean values into one dimention vector
    """Make mean values in one dimension"""
    meanDifPercent = np.ma.ravel(rtt3MeanDifPercent)
    """Make max values and min values in one dimension"""
    maxDifPercent = np.ma.ravel(rtt3MaxDifPercent)
    minDifPercent = np.ma.ravel(rtt3MinDifPercent)
    lengthMean = meanDifPercent.count()
    lengthMax = maxDifPercent.count()
    lengthMin = minDifPercent.count()
    if lengthMean == lengthMax and lengthMean == lengthMin and lengthMax == lengthMin:
        f=plt.figure()
        ax = f.add_subplot(111)
        nbValues = lengthMean
        percent = np.array(range(nbValues))*100/float(nbValues)
        meanCompressed = meanDifPercent.compressed()
        sortMean = np.ma.sort(meanCompressed)
        maxCompressed = maxDifPercent.compressed()
        sortMax = np.ma.sort(maxCompressed)
        minCompressed = minDifPercent.compressed()
        sortMin = np.ma.sort(minCompressed)
        points1 = ax.plot(sortMean, percent, 'r',  marker='o', markersize = 3.0, label='Mean Improvement')
        points2 = ax.plot(sortMax, percent, 'b--', marker='o', markersize = 3.0, label='Max Improvement')
        points3 = ax.plot(sortMin, percent, 'g', linewidth = 5.0, marker='o', markersize = 5.0, label='Min Improvement')
        plt.legend(loc='lower right')
        ax.set_ylabel('Percentage of Origin-Destination Couples (%)')
        ax.set_xlabel("Improvement (%)")
        ax.set_xlim([0, 100])
        ax.set_ylim([0, 105])
        ax.grid(True)
        #plt.draw()
        # to save image
        #f.savefig(picturesPath +'/showCumulativeNbcouplesPercentDifRTT.eps')
        #f.show()

        """add plugins for mean plot""" 
        labels1 = []
        df = pd.DataFrame(index=range(nbValues))
        df['x'] = sortMean
        df['y'] = percent
        for i in range(nbValues):
            label = df.ix[[i], :].T
            label.columns = ['Points {0} '.format(i+1)]
            # .to_html() is unicode; so make leading 'u' go away with str()
            labels1.append(str(label.to_html()))
        tooltip1 = plugins.PointHTMLTooltip(points1[0], labels1,
                                           voffset=10, hoffset=10, css=css)
        mpld3.plugins.connect(f, tooltip1)
        
        """add plugins for max plot """
        labels2 = []
        df = pd.DataFrame(index=range(nbValues))
        df['x'] = sortMax
        df['y'] = percent
        for i in range(nbValues):
            label = df.ix[[i], :].T
            label.columns = ['Points {0} '.format(i+1)]
            # .to_html() is unicode; so make leading 'u' go away with str()
            labels2.append(str(label.to_html()))
        tooltip2 = plugins.PointHTMLTooltip(points2[0], labels2,
                                           voffset=10, hoffset=10, css=css)
        mpld3.plugins.connect(f, tooltip2)
        
        """add plugins for min plot """
        labels3 = []
        df = pd.DataFrame(index=range(nbValues))
        df['x'] = sortMin
        df['y'] = percent
        for i in range(nbValues):
            label = df.ix[[i], :].T
            label.columns = ['Points {0} '.format(i+1)]
            # .to_html() is unicode; so make leading 'u' go away with str()
            labels3.append(str(label.to_html()))
        tooltip3 = plugins.PointHTMLTooltip(points3[0], labels3,
                                           voffset=10, hoffset=10, css=css)
        mpld3.plugins.connect(f, tooltip3)

        '''
        #add plugins
        labels1 = np.around(np.column_stack((sortMean, percent)), 3)
        tooltip1 = mpld3.plugins.PointLabelTooltip(lines1[0],labels=labels1.tolist())
        mpld3.plugins.connect(f, tooltip1)
        labels2 = np.around(np.column_stack((sortMax, percent)), 3)
        tooltip2 = mpld3.plugins.PointLabelTooltip(lines2[0],labels=labels2.tolist())
        mpld3.plugins.connect(f, tooltip2)
        labels3 = np.around (np.column_stack((sortMin, percent)), 3)
        tooltip3 = mpld3.plugins.PointLabelTooltip(lines3[0],labels=labels3.tolist())
        mpld3.plugins.connect(f, tooltip3)
        '''
        mpld3.save_html(f, htmlPath+'/showCumulativeNbcouplesPercentDifRTT.html')
        #mpld3.show()


    else:
        print 'ValuesError'


# This plotSrcFixed function show all points, not for web application
def plotSrcFixed(rtt3DifPercent, rtt3Mean, src, nbProbes, picturesPath, htmlPath):
    """
    Show rtt3DifPercent(by '.') and rtt3Moyenne(by 'x') for one source fixed to all destination in one figure, x-axis for the destination ID, y-axis for rtt3DifPercent values
    @param rtt3DifPercent: contents all percentages of difference(all difference values of all links concatenated),
    the difference is between the direct link and the shortest path, expresed as a percentage of
    the delay of the direct link which is a 3 dimensional matrix in which first and second corespond to first (src) and second (dst) node
    the third dimension is shortestPathLength of  
    @type rtt3DifPercent: 3 dimensional matrix 
    @param rtt3Moyenne:     contents mean values of percentage of difference of all couples of probes,
    the difference is between the direct link and the shortest path, expresed as a percentag of the delay
    of the direct link. 2 dimentional matrix in which first and second corespond to first (src) and second (dst) node
    @type rtt3Moyenne:     2 dimentional matrix
    @param nbProbes: number of nodes
    @type nbProbes: int
    """
    f=plt.figure()
    ax = f.add_subplot(111)
    dataSrc = rtt3DifPercent[src][:, 0:719]
    ones = np.ones(dataSrc.shape)
    v = np.arange(nbProbes).reshape((nbProbes, 1))
    data = np.ma.ravel(dataSrc)
    x1 = np.ravel(v*ones)
    meanSrc = rtt3Mean[src]
    x2 = np.arange(nbProbes)
    points = ax.plot(x1,data,'o', marker = "o")
    scatter = ax.scatter(x2,meanSrc, s=150, marker = "X")
    ax.set_ylabel('percentage of time optimisation')
    ax.set_xlabel("id of destination")
    ax.set_xlim([-1, nbProbes])
    ax.set_ylim([-1, 100])
    ax.set_xticks(range(nbProbes))
    ax.set_title("src :" + str(src)+ " to all destinations " )
    plt.draw()
    
    # to save image
    name ="src_" +str(src)+"_difPercentage"
    f.savefig(picturesPath +'/'+ name +'.eps')
    f.show()

    #add plugins
    tooltip1 = mpld3.plugins.PointLabelTooltip(points[0],labels=np.around(data,3).tolist())
    mpld3.plugins.connect(f, tooltip1)
    labels = ["Mean is {0}".format(i) for i in meanSrc]
    tooltip2 = mpld3.plugins.PointLabelTooltip(scatter,labels=np.around(meanSrc,3).tolist())
    mpld3.plugins.connect(f, tooltip2)
    s = mpld3.fig_to_html(f)
    mpld3.save_html(f, htmlPath+'/'+ name +'.html')

    mpld3.show()

    #return s

# This plotSrcFixedForVisu is for web application to generate graphs 
def plotSrcFixedForVisu(rtt3Min, rtt3Mean, rtt3Max,  src, nbProbes, picturesPath, htmlPath):
    """
    Show rtt3DifPercent(by '.') and rtt3Moyenne(by 'x') for one source fixed to all destination in one figure, x-axis for the destination ID, y-axis for rtt3DifPercent values
    @param rtt3DifPercent: contents all percentages of difference(all difference values of all links concatenated),
    the difference is between the direct link and the shortest path, expresed as a percentage of
    the delay of the direct link which is a 3 dimensional matrix in which first and second corespond to first (src) and second (dst) node
    the third dimension is shortestPathLength of  
    @type rtt3DifPercent: 3 dimensional matrix 
    @param rtt3Moyenne:     contents mean values of percentage of difference of all couples of probes,
    the difference is between the direct link and the shortest path, expresed as a percentag of the delay
    of the direct link. 2 dimentional matrix in which first and second corespond to first (src) and second (dst) node
    @type rtt3Moyenne:     2 dimentional matrix
    @param nbProbes: number of nodes
    @type nbProbes: int
    """
    f=plt.figure()
    ax = f.add_subplot(111)
    minSrc = rtt3Min[src]
    meanSrc = rtt3Mean[src]
    maxSrc = rtt3Max[src]
    x = np.arange(nbProbes)
    width = 0.35       # the width of the bars
    
    #bars1 = ax.bar(x-width*1.5, minSrc, width, fc='g', label='min')
    #bars2 = ax.bar(x-width*0.5, meanSrc, width, fc = 'r', label='mean')
    #bars3 = ax.bar(x+width*0.5, maxSrc, width, fc = 'b', label='max')
    markerline1, stemlines1, baseline1 = ax.stem(x,maxSrc, 'r-',label='max', markerfmt='rD', basefmt=" ",markersize=10)
    markerline2, stemlines2, baseline2 = ax.stem(x,meanSrc,'g-', label='mean', markerfmt='go', basefmt=" ",ms=8)
    markerline3, stemlines3, baseline3 = ax.stem(x,minSrc, 'b-',label='min', markerfmt='bs', basefmt=" ",ms=4)

    ax.set_ylabel('Improvement (%)')
    ax.set_xlabel("Destination Probe")
    ax.set_xlim([-1, nbProbes])
    ax.set_ylim([-1, 100])
    ax.set_xticks(range(nbProbes))
    #ax.set_title("Min (green), Max (blue), and Mean (red) \n % of improvement from probe :" + str(src)+ " to all probes" )
    ax.legend(loc='best',fancybox=True, borderaxespad=0. )   
    ax.yaxis.grid(True) 
    ax.xaxis.grid(False) 

    name ="src_" +str(src)+"_difPercentage"
    mpld3.save_html(f, htmlPath+'/generated/'+ name +'.html')
    #mpld3.show()




 
# with plugins for points values show in a table
def showDefaultTime(rtt3Data, src, dst, picturesPath,  htmlPath):
    """
    This function is to draw two charts in one figure for one couple of
    source probe and dstination probe which contents chart of direct link time (rtt3Data)
    of each time measurement,and chart of corresponding shortest time (rtt3ShortestTime) of every
    time measurement. Line blue is for the shortest path time , line red is for direct link time.
    
    @param rtt3Data: contains all default time (direct path) in 3 dimensional
    matrix in which first and second corespond to first (src) and second (dst)
    node the third dimension is time

    @type rtt3Data: 3 dimensional matrix

    @param rtt3ShortestTime: contains all time of shortest time in 3 dimensional
    matrix in which first and second corespond to first (src) and second (dst)
    node the third dimension is time

    @type rtt3ShortestTime: 3 dimensional matrix

    @param src:	 id of source probe
    @type src:	 int

    @param dst:	 id of destination probe
    @type dst:	 int

    """
    
    if 2000 in rtt3Data:
        print  ("defaultTime list have invalide values")
    else: 
        f=plt.figure()
        ax = f.add_subplot(111)
        if src != dst:
            total_valid_values = np.ma.count(rtt3Data[src][dst])
            print "total_valid_values: " + str(total_valid_values)
            if total_valid_values == 0:
                html_str = '''
                <!DOCTYPE html>
                <html>
                <body>

                <p>No valide measurement to show direct path delay</p>

                </body>
                </html>'''
                name =str(src)+ "_" +str(dst)
                f_name = htmlPath+'/generated/'+ name +'.html'
                Html_file= open(f_name,"w")
                Html_file.write(html_str)
                Html_file.close()
            else:
                x = np.arange(0, rtt3Data[src][dst].count())
                points = ax.plot(x, rtt3Data[src][dst].compressed(),'*',  marker='o', markersize = 3.0, label='shortest path time') 
                ax.set_ylabel('time(ms)')
                ax.set_xlabel("times/nbTimes")
                #ax.set_ylim([0,max(rtt3Data[src][dst].compressed())])
                #ax.set_xlim([0, len(x)+10])
                #ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)
                ax.set_title("src :" + str(src)+ " dst :" +str(dst)+" Direct path delay")

                #add plugins
                labels = []
                df = pd.DataFrame(index=range(len(x)))
                df['x'] = x
                df['y'] = rtt3Data[src][dst].compressed()
                for i in range(len(x)):
                    label = df.ix[[i], :].T
                    label.columns = ['Points {0} '.format(i+1)]
                    # .to_html() is unicode; so make leading 'u' go away with str()
                    labels.append(str(label.to_html()))
                tooltip = plugins.PointHTMLTooltip(points[0], labels,
                                                    voffset=10, hoffset=10, css=css)
                #mpld3.plugins.connect(f, tooltip)

                name =  str(src)+ "_" +str(dst)
                mpld3.save_html(f, htmlPath+'/generated/'+ name +'.html')
                #mpld3.show()
        else :
            print ("ValueError")

# DONE
def showHistoDefaultTime(rtt3Data, src, dst, picturesPath,  htmlPath):
    """
    show histogram of vector for shortest path Length
    @param shortestPathLength: contents all data of shortest path length calculated for every couple probes during a period mesurement
    @type shortestPathLength: numpy masked array
    @title: title of the histogram
    @type title: string
    @param nbProbes: number of probes in total
    @type nbProbes: int

    """
    class BarLabelToolTip(plugins.PluginBase):    
        JAVASCRIPT = """
        mpld3.register_plugin("barlabeltoolTip", BarLabelToolTip);
        BarLabelToolTip.prototype = Object.create(mpld3.Plugin.prototype);
        BarLabelToolTip.prototype.constructor = BarLabelToolTip;
        BarLabelToolTip.prototype.requiredProps = ["ids","labels"];
        BarLabelToolTip.prototype.defaultProps = {
            hoffset: 0,
            voffset: 10,
            location: 'mouse'
        };
        function BarLabelToolTip(fig, props){
            mpld3.Plugin.call(this, fig, props);
        };

        BarLabelToolTip.prototype.draw = function(){
            var svg = d3.select("#" + this.fig.figid);
            var objs = svg.selectAll(".mpld3-path");
            var loc = this.props.location;
            var labels = this.props.labels

            test = this.fig.canvas.append("text")
                .text("hello world")
                .style("font-size", 72)
                .style("opacity", 0.5)
                .style("text-anchor", "middle")
                .attr("x", this.fig.width / 2)
                .attr("y", this.fig.height / 2)
                .style("visibility", "hidden");

            function mousemove(d) {
                if (loc === "mouse") {
                    var pos = d3.mouse(this.fig.canvas.node())
                    this.x = pos[0] + this.props.hoffset;
                    this.y = pos[1] - this.props.voffset;
                }

                test
                    .attr("x", this.x)
                    .attr("y", this.y);
            };

            function mouseout(d) {
                test.style("visibility", "hidden")
            };

            this.props.ids.forEach(function(id, i) {


                var obj = mpld3.get_element(id);

                function mouseover(d) {
                    test.style("visibility", "visible")
                        .style("font-size", 24)
                        .style("opacity", 0.7)
                        .text(labels[i])
                };

                obj.elements().on("mouseover", mouseover.bind(this))

            });

           objs.on("mousemove", mousemove.bind(this)) 
               .on("mouseout", mouseout.bind(this));     

        }       
        """
        def __init__(self, ids, labels=None, location="mouse"):

            self.dict_ = {"type": "barlabeltoolTip",
                          "ids": ids,
                          "labels": labels,
                          "location": location}
    print 'enter histo show'
    f=plt.figure()
    ax = f.add_subplot(111)
    if src != dst:
        data = rtt3Data[src][dst]
        total_valid_values= np.ma.count(data)
        if total_valid_values == 0:
            html_str = '''
            <!DOCTYPE html>
            <html>
            <body>

            <p>No valide measurement to show distribution of direct delay</p>

            </body>
            </html>'''
            name =str(src)+ "_" +str(dst)+"_Histo"
            f_name = htmlPath+'/generated/'+ name +'.html'
            Html_file= open(f_name,"w")
            Html_file.write(html_str)
            Html_file.close()
        else:
            weights = (~np.ma.getmask(data)).astype(int)/float(total_valid_values)
            dataNew = data.compressed()
            bins = np.linspace(int(min(dataNew))-4, int(max(dataNew))+4, 40)
            probilities, bins, patches = ax.hist(data, weights=weights,bins=bins,facecolor='b', label = 'Histogram')
            ax.set_xlabel("Direct delay time")
            ax.set_ylabel("Probability")
            ax.set_ylim([0,1])
            ax.set_xlim([bins[0]-10, bins[-1]+10])
            ax.set_title("src :" + str(src)+ " dst :" +str(dst) + " Distribution of direct delay" )


            # add plot bincenters, cumulative function
            bincenters = 0.5*(bins[1:]+bins[:-1])
            y = np.around(probilities.cumsum(),3)
            points1 = ax.plot(bincenters, y, '--', marker='o', label = 'Cumulative')
            plt.legend(loc='center right')
            
            
            # add plugins for probilities
            labelsBinCenters = [round(bar.get_height(),2) for bar in patches]
            ids = [utils.get_id(bar) for bar in patches]
            plugins.connect(f, BarLabelToolTip(ids, labelsBinCenters))
            
            # add plugins for cumulative plot 
            labels = []
            df = pd.DataFrame(index=range(len(bincenters)))
            df['x'] = bincenters
            df['y'] = y
            for i in range(len(bincenters)):
                label = df.ix[[i], :].T
                label.columns = ['Points {0} '.format(i+1)]
                # .to_html() is unicode; so make leading 'u' go away with str()
                labels.append(str(label.to_html()))    
            
            tooltip = plugins.PointHTMLTooltip(points1[0], labels,
                                            voffset=10, hoffset=10, css=css)
            mpld3.plugins.connect(f, tooltip)
            name =  str(src)+ "_" +str(dst)+"_Histo"
            mpld3.save_html(f, htmlPath+'/generated/'+ name +'.html')
            #mpld3.show()
            


        
# DONE
def showDefaultTimeShortestTime(rtt3Data, rtt3ShortestTime, src, dst, picturesPath,  htmlPath):
    '''
    This function is to draw two charts in one figure for one couple of
    source probe and dstination probe which contents chart of direct link time (rtt3Data)
    of each time measurement,and chart of corresponding shortest time (rtt3ShortestTime) of every
    time measurement. Line blue is for the shortest path time , line red is for direct link time.
    
    @param rtt3Data: contains all default time (direct path) in 3 dimensional
    matrix in which first and second corespond to first (src) and second (dst)
    node the third dimension is time

    @type rtt3Data: 3 dimensional matrix

    @param rtt3ShortestTime: contains all time of shortest time in 3 dimensional
    matrix in which first and second corespond to first (src) and second (dst)
    node the third dimension is time

    @type rtt3ShortestTime: 3 dimensional matrix

    @param src:	 id of source probe

    @type src:	 int

    @param dst:	 id of destination probe

    @type dst:	 int

    '''
    # Javascript for function showDefaultTimeShortestTime
    class InteractiveLegendPlugin(plugins.PluginBase):
        """A plugin for an interactive legends.
        Inspired by http://bl.ocks.org/simzou/6439398
        Parameters
        ----------
        plot_elements : iterable of matplotlib elements
            the elements to associate with a given legend items
        labels : iterable of strings
            The labels for each legend element
        ax :  matplotlib axes instance, optional
            the ax to which the legend belongs. Default is the first
            axes. The legend will be plotted to the right of the specified
            axes
        alpha_unsel : float, optional
            the alpha value to multiply the plot_element(s) associated alpha
            with the legend item when the legend item is unselected.
            Default is 0.2
        alpha_over : float, optional
            the alpha value to multiply the plot_element(s) associated alpha
            with the legend item when the legend item is overlaid.
            Default is 1 (no effect), 1.5 works nicely !
        start_visible : boolean, optional (could be a list of booleans)
            defines if objects should start selected on not.
        Examples
        --------
        >>> import matplotlib.pyplot as plt
        >>> from mpld3 import fig_to_html, plugins
        >>> N_paths = 5
        >>> N_steps = 100
        >>> x = np.linspace(0, 10, 100)
        >>> y = 0.1 * (np.random.random((N_paths, N_steps)) - 0.5)
        >>> y = y.cumsum(1)
        >>> fig, ax = plt.subplots()
        >>> labels = ["a", "b", "c", "d", "e"]
        >>> line_collections = ax.plot(x, y.T, lw=4, alpha=0.6)
        >>> interactive_legend = plugins.InteractiveLegendPlugin(line_collections,
        ...                                                      labels,
        ...                                                      alpha_unsel=0.2,
        ...                                                      alpha_over=1.5,
        ...                                                      start_visible=True)
        >>> plugins.connect(fig, interactive_legend)
        >>> fig_to_html(fig)
        """

        JAVASCRIPT = """
        mpld3.register_plugin("interactive_legend", InteractiveLegend);
        InteractiveLegend.prototype = Object.create(mpld3.Plugin.prototype);
        InteractiveLegend.prototype.constructor = InteractiveLegend;
        InteractiveLegend.prototype.requiredProps = ["element_ids", "labels"];
        InteractiveLegend.prototype.defaultProps = {"ax":null,
                                                    "alpha_unsel":0.2,
                                                    "alpha_over":1.0,
                                                    "start_visible":true}
        function InteractiveLegend(fig, props){
            mpld3.Plugin.call(this, fig, props);
        };
        InteractiveLegend.prototype.draw = function(){
            var alpha_unsel = this.props.alpha_unsel;
            var alpha_over = this.props.alpha_over;
            var legendItems = new Array();
            for(var i=0; i<this.props.labels.length; i++){
                var obj = {};
                obj.label = this.props.labels[i];
                var element_id = this.props.element_ids[i];
                mpld3_elements = [];
                for(var j=0; j<element_id.length; j++){
                    var mpld3_element = mpld3.get_element(element_id[j], this.fig);
                    // mpld3_element might be null in case of Line2D instances
                    // for we pass the id for both the line and the markers. Either
                    // one might not exist on the D3 side
                    if(mpld3_element){
                        mpld3_elements.push(mpld3_element);
                    }
                }
                obj.mpld3_elements = mpld3_elements;
                obj.visible = this.props.start_visible[i]; // should become be setable from python side
                legendItems.push(obj);
                set_alphas(obj, false);
            }
            // determine the axes with which this legend is associated
            var ax = this.props.ax
            if(!ax){
                ax = this.fig.axes[0];
            } else{
                ax = mpld3.get_element(ax, this.fig);
            }
            // add a legend group to the canvas of the figure
            var legend = this.fig.canvas.append("svg:g")
                                   .attr("class", "legend");
            // add the rectangles
            legend.selectAll("rect")
                    .data(legendItems)
                    .enter().append("rect")
                    .attr("height", 10)
                    .attr("width", 25)
                    .attr("x", ax.width + ax.position[0] + 25)
                    .attr("y",function(d,i) {
                               return ax.position[1] + i * 25 + 10;})
                    .attr("stroke", get_color)
                    .attr("class", "legend-box")
                    .style("fill", function(d, i) {
                               return d.visible ? get_color(d) : "white";})
                    .on("click", click).on('mouseover', over).on('mouseout', out);
            // add the labels
            legend.selectAll("text")
                  .data(legendItems)
                  .enter().append("text")
                  .attr("x", function (d) {
                               return ax.width + ax.position[0] + 25 + 40;})
                  .attr("y", function(d,i) {
                               return ax.position[1] + i * 25 + 10 + 10 - 1;})
                  .text(function(d) { return d.label });
            // specify the action on click
            function click(d,i){
                d.visible = !d.visible;
                d3.select(this)
                  .style("fill",function(d, i) {
                    return d.visible ? get_color(d) : "white";
                  })
                set_alphas(d, false);
                if (i == 0){
                    alert("shortest path time");}
                if (i == 1){
                    alert("direct path time");}
            };
            // specify the action on legend overlay 
            function over(d,i){
                 set_alphas(d, true);
            };
            // specify the action on legend overlay 
            function out(d,i){
                 set_alphas(d, false);
            };
            // helper function for setting alphas
            function set_alphas(d, is_over){
                for(var i=0; i<d.mpld3_elements.length; i++){
                    var type = d.mpld3_elements[i].constructor.name;
                    if(type =="mpld3_Line"){
                        var current_alpha = d.mpld3_elements[i].props.alpha;
                        var current_alpha_unsel = current_alpha * alpha_unsel;
                        var current_alpha_over = current_alpha * alpha_over;
                        d3.select(d.mpld3_elements[i].path[0][0])
                            .style("stroke-opacity", is_over ? current_alpha_over :
                                                    (d.visible ? current_alpha : current_alpha_unsel))
                            .style("stroke-width", is_over ? 
                                    alpha_over * d.mpld3_elements[i].props.edgewidth : d.mpld3_elements[i].props.edgewidth);
                    } else if((type=="mpld3_PathCollection")||
                             (type=="mpld3_Markers")){
                        var current_alpha = d.mpld3_elements[i].props.alphas[0];
                        var current_alpha_unsel = current_alpha * alpha_unsel;
                        var current_alpha_over = current_alpha * alpha_over;
                        d3.selectAll(d.mpld3_elements[i].pathsobj[0])
                            .style("stroke-opacity", is_over ? current_alpha_over :
                                                    (d.visible ? current_alpha : current_alpha_unsel))
                            .style("fill-opacity", is_over ? current_alpha_over :
                                                    (d.visible ? current_alpha : current_alpha_unsel));
                    } else{
                        console.log(type + " not yet supported");
                    }
                }
            };
            // helper function for determining the color of the rectangles
            function get_color(d){
                var type = d.mpld3_elements[0].constructor.name;
                var color = "black";
                if(type =="mpld3_Line"){
                    color = d.mpld3_elements[0].props.edgecolor;
                } else if((type=="mpld3_PathCollection")||
                          (type=="mpld3_Markers")){
                    color = d.mpld3_elements[0].props.facecolors[0];
                } else{
                    console.log(type + " not yet supported");
                }
                return color;
            };
        };
        """

        css_ = """
        .legend-box {
          cursor: pointer;
        }
        """

        def __init__(self, plot_elements, labels, ax=None,
                     alpha_unsel=0.2, alpha_over=1., start_visible=True):

            self.ax = ax

            if ax:
                ax = utils.get_id(ax)

            # start_visible could be a list
            if isinstance(start_visible, bool):
                start_visible = [start_visible] * len(labels)
            elif not len(start_visible) == len(labels):
                raise ValueError("{} out of {} visible params has been set"
                                 .format(len(start_visible), len(labels)))     

            mpld3_element_ids = self._determine_mpld3ids(plot_elements)
            self.mpld3_element_ids = mpld3_element_ids
            self.dict_ = {"type": "interactive_legend",
                          "element_ids": mpld3_element_ids,
                          "labels": labels,
                          "ax": ax,
                          "alpha_unsel": alpha_unsel,
                          "alpha_over": alpha_over,
                          "start_visible": start_visible}

        def _determine_mpld3ids(self, plot_elements):
            """
            Helper function to get the mpld3_id for each
            of the specified elements.
            """
            mpld3_element_ids = []

            # There are two things being done here. First,
            # we make sure that we have a list of lists, where
            # each inner list is associated with a single legend
            # item. Second, in case of Line2D object we pass
            # the id for both the marker and the line.
            # on the javascript side we filter out the nulls in
            # case either the line or the marker has no equivalent
            # D3 representation.
            for entry in plot_elements:
                ids = []
                if isinstance(entry, collections.Iterable):
                    for element in entry:
                        mpld3_id = utils.get_id(element)
                        ids.append(mpld3_id)
                        if isinstance(element, matplotlib.lines.Line2D):
                            mpld3_id = utils.get_id(element, 'pts')
                            ids.append(mpld3_id)
                else:
                    ids.append(utils.get_id(entry))
                    if isinstance(entry, matplotlib.lines.Line2D):
                        mpld3_id = utils.get_id(entry, 'pts')
                        ids.append(mpld3_id)
                mpld3_element_ids.append(ids)
            return mpld3_element_ids
    
    if 2000 in rtt3Data:
        print  ("defaultTime list have invalide values")
    else: 
        f=plt.figure()
        ax = f.add_subplot(111)
        if src != dst and np.ma.count(rtt3ShortestTime[src][dst])!=0:
            lines = np.vstack([rtt3ShortestTime[src][dst].compressed(), rtt3Data[src][dst].compressed()])
            x = np.arange(0, rtt3ShortestTime[src][dst].count())
            line_collections = ax.plot(x, lines.T, lw=4, alpha=1)
            ax.set_ylabel('time(ms)')
            ax.set_xlabel("times")
            #ax.set_ylim([0,max(rtt3Data[src][dst].compressed())])
            #ax.set_xlim([0, len(x)+10])
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)
            ax.set_title("src :" + str(src)+ " dst :" +str(dst)+" Direct path time and shortest path time")
            
            #plt.draw()
            # to save image
            name =  str(src)+ "_" +str(dst)+"_DT_ST"
            #f.savefig(picturesPath +'/'+ name +'.eps')
            #f.show()
            
            #add plugins
            labels = ["shortest path time ", "direct path time"]
            interactive_legend = InteractiveLegendPlugin(line_collections,
                                                                 labels,
                                                                 alpha_unsel=0.2,
                                                                 alpha_over=1.5,
                                                                 start_visible=True)
            plugins.connect(f, interactive_legend)
            mpld3.save_html(f, htmlPath+'/generated/'+ name +'.html')
            #mpld3.show()
            
        else :
            html_str = '''
            <!DOCTYPE html>
            <html>
            <body>

            <p>No valide measurement for this link</p>

            </body>
            </html>'''
            name =  str(src)+ "_" +str(dst)+"_DT_ST"
            f_name = htmlPath+'/generated/'+ name +'.html'
            Html_file= open(f_name,"w")
            Html_file.write(html_str)
            Html_file.close()


# DONE
def showHistoPathLength(rtt3ShortestPathLength, src, dst, picturesPath, htmlPath):

    '''
    This function is to draw the histogram of the distribution of the number of hops in the shortest path(number of probes in the shortest route minus 1)
    as a function of time(each elements corresponds to a measurement epoch), for onecouple of source probe and destination probe.  
    @param shortestPathLength:	contents all shortest path lengths in 3dimensional matrix in which first and second corespond to first (src) and second (dst)
    node the third dimension is shortestPathLength
    @type shortestPathLength:	3 dimensional matrix
    @param src:	id of source probe
    @type src: int
    @param dst:	id of destination probe
    @type dst: int

    '''
    class BarLabelToolTip(plugins.PluginBase):    
        JAVASCRIPT = """
        mpld3.register_plugin("barlabeltoolTip", BarLabelToolTip);
        BarLabelToolTip.prototype = Object.create(mpld3.Plugin.prototype);
        BarLabelToolTip.prototype.constructor = BarLabelToolTip;
        BarLabelToolTip.prototype.requiredProps = ["ids","labels"];
        BarLabelToolTip.prototype.defaultProps = {
            hoffset: 0,
            voffset: 10,
            location: 'mouse'
        };
        function BarLabelToolTip(fig, props){
            mpld3.Plugin.call(this, fig, props);
        };

        BarLabelToolTip.prototype.draw = function(){
            var svg = d3.select("#" + this.fig.figid);
            var objs = svg.selectAll(".mpld3-path");
            var loc = this.props.location;
            var labels = this.props.labels

            test = this.fig.canvas.append("text")
                .text("hello world")
                .style("font-size", 72)
                .style("opacity", 0.5)
                .style("text-anchor", "middle")
                .attr("x", this.fig.width / 2)
                .attr("y", this.fig.height / 2)
                .style("visibility", "hidden");

            function mousemove(d) {
                if (loc === "mouse") {
                    var pos = d3.mouse(this.fig.canvas.node())
                    this.x = pos[0] + this.props.hoffset;
                    this.y = pos[1] - this.props.voffset;
                }

                test
                    .attr("x", this.x)
                    .attr("y", this.y);
            };

            function mouseout(d) {
                test.style("visibility", "hidden")
            };

            this.props.ids.forEach(function(id, i) {


                var obj = mpld3.get_element(id);

                function mouseover(d) {
                    test.style("visibility", "visible")
                        .style("font-size", 24)
                        .style("opacity", 0.7)
                        .text(labels[i])
                };

                obj.elements().on("mouseover", mouseover.bind(this))

            });

           objs.on("mousemove", mousemove.bind(this)) 
               .on("mouseout", mouseout.bind(this));     

        }       
        """
        def __init__(self, ids, labels=None, location="mouse"):

            self.dict_ = {"type": "barlabeltoolTip",
                          "ids": ids,
                          "labels": labels,
                          "location": location}

    
    f=plt.figure()
    ax = f.add_subplot(111)
    if src != dst and np.ma.count(rtt3ShortestPathLength[src][dst])!=0:
        data = rtt3ShortestPathLength[src][dst]
        total_valid_values= np.ma.count(data)
        weights = (~np.ma.getmask(data)).astype(int)/float(total_valid_values)
        bins = np.linspace(0, 10,11)
        probilities, bins, patches = plt.hist(data,
                                              weights=weights,
                                              bins=bins, normed=True,
                                              facecolor='b',align='left',
                                              label = 'Histogram')
        ax.set_xlabel("Path Length")
        ax.set_ylabel("Probability")
        #ax.set_ylim([0,1])
        ax.set_xticks(bins[:-1])
        ax.set_xticks(bins[:-1])
        ax.set_xlim([0, bins[-1]+1])
        ax.set_title("src :" + str(src)+ " dst :" +str(dst) + " Distribution of path length" )


        # add plot bincenters
        bincenters = bins[1:-1]
        y = np.around(probilities[1:].cumsum(),3)
        points1 = ax.plot(bincenters, y, '--', marker='o', label = 'Cumulative')
        plt.legend(loc='center right')
        
        #plt.draw()
        # to save image
        name =  str(src)+ "_" +str(dst)+"_HistoPL"
        #f.savefig(picturesPath +'/'+ name +'.eps')
        #f.show()

        # add plugins for probilities
        labelsBinCenters = [round(bar.get_height(),2) for bar in patches]
        ids = [utils.get_id(bar) for bar in patches]
        plugins.connect(f, BarLabelToolTip(ids, labelsBinCenters))
        
        # add plugins for cumulative plot 
        labels = []
        df = pd.DataFrame(index=range(len(bincenters)))
        df['x'] = bincenters
        df['y'] = y
        for i in range(len(bincenters)):
            label = df.ix[[i], :].T
            label.columns = ['Points {0} '.format(i+1)]
            # .to_html() is unicode; so make leading 'u' go away with str()
            labels.append(str(label.to_html()))    
        
        tooltip = plugins.PointHTMLTooltip(points1[0], labels,
                                           voffset=10, hoffset=10, css=css)
        mpld3.plugins.connect(f, tooltip)
        mpld3.save_html(f, htmlPath+'/generated/'+ name +'.html')
        #mpld3.show()

        
    else :
        html_str = '''
        <!DOCTYPE html>
        <html>
        <body>

        <p>No valide measurement for this link</p>

        </body>
        </html>'''
        name =  str(src)+ "_" +str(dst)+"_HistoPL"
        f_name = htmlPath+'/generated/'+ name +'.html'
        Html_file= open(f_name,"w")
        Html_file.write(html_str)
        Html_file.close()


# plugins too large
def showPathLength(shortestPathLength, src, dst, picturesPath, htmlPath):
    '''
    This function is to draw the chart of the evolution of the number of hops
    in the shortest path(number of probes in the shortest route minus 1) as a
    function of time(each elements corresponds to a measurement epoch), for one
    couple of source probe and destination probe.  

    @param shortestPathLength:	contents all shortest path lengths in 3dimensional
    matrix in which first and second corespond to first (src) and second (dst) node
    the third dimension is shortestPathLength

    @type shortestPathLength:	numpy masked array

    @param src:	id of source probe

    @type src: int

    @param dst:	id of destination probe

    @type dst: int
    '''
    f=plt.figure()
    ax = f.add_subplot(111)
    if src != dst and np.ma.count(shortestPathLength[src][dst])!=0:
        points = ax.plot(shortestPathLength[src][dst], linestyle='None', marker = ".", markersize=1) 
        nbTimes = len (shortestPathLength[src][dst])
        ax.set_ylabel('Path Length')
        ax.set_xlabel("times")
        ax.set_title("src :" + str(src)+ " dst :" +str(dst)+" Shortest Path Length")
        ax.set_xlim([0,nbTimes+10])
        ax.set_ylim([0, 6])
        #plt.draw()
        # to save image
        name = str(src)+"_"+str(dst)+"SPL"
        #f.savefig(picturesPath +'/'+name+'.eps')
        #f.show()


        """add plugins for plot """
        labels3 = []
        x = range(0, len(shortestPathLength[src][dst]) )
        df = pd.DataFrame(index=range(nbTimes))
        df['x'] = x
        df['y'] = shortestPathLength[src][dst]
        for i in range(nbTimes):
            label = df.ix[[i], :].T
            label.columns = ['Points {0} '.format(i+1)]
            # .to_html() is unicode; so make leading 'u' go away with str()
            labels3.append(str(label.to_html()))
        tooltip3 = plugins.PointHTMLTooltip(points[0], labels3,
                                           voffset=10, hoffset=10, css=css)
        #mpld3.plugins.connect(f, tooltip3)

        '''
        #labels1 = np.around(shortestPathLength[src][dst], 3)
        tooltip1 = mpld3.plugins.PointLabelTooltip(points[0],labels=x)
        mpld3.plugins.connect(f, tooltip1)
        '''

        #s = mpld3.fig_to_html(f)
        mpld3.save_html(f, htmlPath+'/generated/'+ name +'.html')
        #mpld3.show()

        #return s
        
    else :
        html_str = '''
        <!DOCTYPE html>
        <html>
        <body>

        <p>No valide measurement for this link</p>

        </body>
        </html>'''
        name = str(src)+"_"+str(dst)+"SPL"
        f_name = htmlPath+'/generated/'+ name +'.html'
        Html_file= open(f_name,"w")
        Html_file.write(html_str)
        Html_file.close()
    

# TO DO PLUGINS     
def showTraceTwoLinks(rtt3, link1, link2, picturesPath, htmlPath):
    """
    show temporal trace for rtt3[src1][dst1] and rtt3[src2][dst2] where link1=(src1,dst1) and link1=(src2,dst2)
    """
    src1=link1[0]
    dst1=link1[1]
    src2=link2[0]    
    dst2=link2[1]
    f=plt.figure()
    ax = f.add_subplot(111)
    if dst1 != src1:
        line1, = ax.plot(rtt3[src1][dst1],'b', label=str(link1))
        line2, = ax.plot(rtt3[src2][dst2],'r', label =str(link2))
        ax.set_ylabel('milliseconds')
        ax.set_xlabel("times")
        ax.set_title("RTT")
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)
        plt.draw()
        f.show()
        # to save image
        name = str(link1)+"_"+str(link2)+"TemporalTrace"
        #f.savefig(picturesPath +'/'++'.eps')
        #s = mpld3.fig_to_html(f)
        mpld3.save_html(f, htmlPath+'/generated/'+ name +'.html')
        #mpld3.show()
        #return s

def showPathInformation(src, dst, informationDict,  picturesPath, htmlPath):
    '''
    informationDict Structure Exemple:
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
    Two bar charts in one figure to reprensent nbTimes appear of shortest paths possiblec for the link src-dst
    in both charts of them, height of bar is nbTimes, vertical axe shows the path
    one of them, its label on top of bar is the average time of this path with unit ms (limited two decimal points)
    the other one, its label on top of bar is the average of the percentage improvement with unit % (limited two decimal points)
    '''
    def autolabel(rects, ax):
        # attach some text labels
        for i in range(len(rects)):
            height = rects[i].get_height()
            ax.text(rects[i].get_x() + rects[i].get_width()/2., 1.01*height,
                    '%d' % height,
                    ha='center', va='bottom')

    if str(src) + "-" + str(dst) in informationDict:
        listPath = informationDict[str(src) + "-" + str(dst)]
        xticklabels= [j.encode('utf-8') for d in listPath for j in d.keys()]
        
        print xticklabels
        
        ylabels1 = [ str(float("{0:.2f}".format(i["meanTime"])))+'(ms)' for d in listPath for i in d.values()]
        ylabels2 = [ str(float("{0:.2f}".format(i["meanDiffPercent"])))+'(%)' for d in listPath for i in d.values()]
        y = [ i["nbtimes"] for d in listPath for i in d.values()]
        x = np.arange(len(y))
        print y
        width = 0.25
        
        f=plt.figure(1)
        ax1 = f.add_subplot(111)
        rects1 = ax1.bar(x-0.5*width, y , width, color='b')
        ax1.set_ylabel('nbTimes appear')
        ax1.set_xticks(x)
        ax1.set_xticklabels(xticklabels)
        autolabel(rects1, ax1)
        ax1.set_title('Shortest routes path nbTimes, meanTime representation')
        #plt.draw()
        #f.show()
        
        for i, box in enumerate(rects1.get_children()):
            tooltip = mpld3.plugins.LineLabelTooltip(box, label="meanTime:"+ylabels1[i]+"path:"+xticklabels[i])
            mpld3.plugins.connect(f, tooltip)

        name1 =  str(src)+ "_" +str(dst)+"meanTime_pathInformation"
        mpld3.save_html(f, htmlPath+'/generated/'+ name1 +'.html')
        #mpld3.show()
        
        
        f1=plt.figure(2)
        ax2 = f1.add_subplot(111)
        rects2 = ax2.bar(x-0.5*width, y , width, color='b')
        ax2.set_ylabel('nbTimes appear')
        ax2.set_xticks(x)
        ax2.set_xticklabels(xticklabels)
        autolabel(rects2,ax2)
        ax2.set_title('Shortest routes path nbTimes, meanDiffpercent representation')
        #plt.show()
        #f.show()
        for i, box in enumerate(rects2.get_children()):
            tooltip = mpld3.plugins.LineLabelTooltip(box, label="meanDiffpercent:"+ylabels2[i]+" path:"+xticklabels[i])
            mpld3.plugins.connect(f1, tooltip)
        name2 =  str(src)+ "_" +str(dst)+"meanDiffpercent_pathInformation"
        mpld3.save_html(f1, htmlPath+'/generated/'+ name2 +'.html')
        #mpld3.show()
         
    else:
        html_str = '''
        <!DOCTYPE html>
        <html>
        <body>

        <p>No valide measurement for this link</p>

        </body>
        </html>'''
        name1 =  str(src)+ "_" +str(dst)+"meanTime_pathInformation"
        name2 =  str(src)+ "_" +str(dst)+"meanDiffpercent_pathInformation"
        f_name = htmlPath+'/generated/' + name1 + '.html'
        Html_file= open(f_name,"w")
        Html_file.write(html_str)
        Html_file.close()
        
        f_name2 = htmlPath+'/generated/' + name2 + '.html'
        Html_file2= open(f_name2,"w")
        Html_file2.write(html_str)
        Html_file2.close()


# TO ADD PLUGINS 
def showMatrixDiffRtt(diffRTT3Percentage, nbProbes, rtt3MaxdiffPercent, rtt3MindiffPercent, rtt3MeandiffPercent, picturesPath, htmlPath):

    '''
    Shows a matrix representation of the difference (min diff, mean diff and max diff) between the RTT of the direct (IP) path and the min RTT path, for all origin destination couples
    @param diffRTT3Percentage: difference of RTT between the IP path and the  path with the minimum RTT, expressed between each origin destination couple, time series
    @type diffRTT3Percentage:   list, 3-dimensional matrix [src][dst][nbMeasure]   
    @param nbProbes: number of probes considered
    @type nbProbes: int
    '''
    f,(ax1,ax2,ax3)=plt.subplots(1,3)

    '''
    matrixMean=np.zeros((nbProbes,nbProbes))
    matrixMax=np.zeros((nbProbes,nbProbes))
    matrixMin=np.zeros((nbProbes,nbProbes))

    
    for src in range (nbProbes):
        for dst in range (nbProbes):
            if src==dst or len(np.ma.getdata(diffRTT3Percentage[src][dst]))==np.ma.count_masked(diffRTT3Percentage[src][dst])  :
                matrixMin[src][dst] = float('nan')
                matrixMean[src][dst] = float('nan')
                matrixMax[src][dst] = float('nan')
            else:
                matrixMin[src][dst] = np.ma.min(diffRTT3Percentage[src][dst])
                matrixMean[src][dst] = np.ma.mean(diffRTT3Percentage[src][dst])
                matrixMax[src][dst] = np.ma.max(diffRTT3Percentage[src][dst])
    '''
    
    '''replace all masked values by float('nan')'''
    matrixMean=np.ma.filled(rtt3MeandiffPercent, fill_value = float('nan'))
    matrixMax=np.ma.filled(rtt3MaxdiffPercent, fill_value = float('nan'))
    matrixMin=np.ma.filled(rtt3MindiffPercent, fill_value = float('nan'))
    
    vmax=100
    vmin=0
    ax1.imshow(matrixMin, cmap=plt.cm.jet, vmin=vmin, vmax=vmax, interpolation='nearest')
    ax2.imshow(matrixMean, cmap=plt.cm.jet, vmin=vmin, vmax=vmax, interpolation='nearest')	
    im=ax3.imshow(matrixMax, cmap=plt.cm.jet, vmin=vmin, vmax=vmax, interpolation='nearest')
    for ax in [ax1,ax2,ax3]:
        ax.set_xticks(range(nbProbes))
        ax.set_xticklabels(range(nbProbes))
        ax.set_xlabel('Dst probe Id')
        ax.set_yticks(range(nbProbes))
        ax.set_yticklabels(range(nbProbes))
        ax.set_ylabel('Src probe Id')
    ax1.set_title('Min')
    ax2.set_title('Mean')
    ax3.set_title('Max')
    f.subplots_adjust(right=0.8)
    f.suptitle('Difference between direct link delay and min delay path (% of direct link delay)')
       
    cbar_ax = f.add_axes([0.85, 0.25, 0.02, 0.5])
    f.colorbar(im,cax=cbar_ax)
    
    #plt.ion()
    plt.show()
    #plt.show()
    #f.savefig(picturesPath + '/matrixDifPercent.eps')
    plt.pause(5)
    # to save image
    #s = mpld3.fig_to_html(f)
    mpld3.save_html(f, htmlPath+'/MatrixThree.html')
    mpld3.show()

    #return s
    


def showMatrixCovRtt(rtt3IPPath ,nbProbes, picturesPath, htmlPath):
    '''
    Shows a matrix representation of the covariance of RTT time traces for each pair of links
    @param rtt3IPPath: RTT of the direct (IP) path between each origin destination couple, time series 
    @type rtt3IPPath: list, 3-dimensional matrix [src][dst][nbMeasure]
    @param nbProbes: number of probes considered
    @type nbProbes: int
    '''
    #Javascript class for histograms
    class BarLabelToolTip(plugins.PluginBase):    
        JAVASCRIPT = """
        mpld3.register_plugin("barlabeltoolTip", BarLabelToolTip);
        BarLabelToolTip.prototype = Object.create(mpld3.Plugin.prototype);
        BarLabelToolTip.prototype.constructor = BarLabelToolTip;
        BarLabelToolTip.prototype.requiredProps = ["ids","labels"];
        BarLabelToolTip.prototype.defaultProps = {
            hoffset: 0,
            voffset: 10,
            location: 'mouse'
        };
        function BarLabelToolTip(fig, props){
            mpld3.Plugin.call(this, fig, props);
        };

        BarLabelToolTip.prototype.draw = function(){
            var svg = d3.select("#" + this.fig.figid);
            var objs = svg.selectAll(".mpld3-path");
            var loc = this.props.location;
            var labels = this.props.labels

            test = this.fig.canvas.append("text")
                .text("hello world")
                .style("font-size", 72)
                .style("opacity", 0.5)
                .style("text-anchor", "middle")
                .attr("x", this.fig.width / 2)
                .attr("y", this.fig.height / 2)
                .style("visibility", "hidden");

            function mousemove(d) {
                if (loc === "mouse") {
                    var pos = d3.mouse(this.fig.canvas.node())
                    this.x = pos[0] + this.props.hoffset;
                    this.y = pos[1] - this.props.voffset;
                }

                test
                    .attr("x", this.x)
                    .attr("y", this.y);
            };

            function mouseout(d) {
                test.style("visibility", "hidden")
            };

            this.props.ids.forEach(function(id, i) {


                var obj = mpld3.get_element(id);

                function mouseover(d) {
                    test.style("visibility", "visible")
                        .style("font-size", 24)
                        .style("opacity", 0.7)
                        .text(labels[i])
                };

                obj.elements().on("mouseover", mouseover.bind(this))

            });

           objs.on("mousemove", mousemove.bind(this)) 
               .on("mouseout", mouseout.bind(this));     

        }       
        """
        def __init__(self, ids, labels=None, location="mouse"):

            self.dict_ = {"type": "barlabeltoolTip",
                          "ids": ids,
                          "labels": labels,
                          "location": location}

    def onclickTimeTraces(event):
        '''
        On mouse click callback, displays time series for RTT of direct (IP) path of the two links corresponding to the clicked x,y value 
        '''
        print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              (event.button, event.x, event.y, event.xdata, event.ydata))
        i=int(np.round(event.ydata))
        j=int(np.round(event.xdata))
        link1=links[i]
        link2=links[j]
        src1=link1[0]
        dst1=link1[1]
        src2=link2[0]
        dst2=link2[1]  
        '''get the RTT values that were considered for calculating the covariance'''      
        rttLink2=rtt3IPPath[src2][dst2]
        rttLink1=rtt3IPPath[src1][dst1]

        '''plot the RTT values'''
        f=plt.figure()
        ax = f.add_subplot(111)
        line1, = ax.plot(rttLink1,'b', label=str(link1))
        line2, = ax.plot(rttLink2,'r', label =str(link2))
        ax.set_ylabel('milliseconds')
        ax.set_xlabel("times")
        ax.set_title("RTT")
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)
        plt.draw()
        f.show()
        #s = mpld3.fig_to_html(f)
        mpld3.save_html(f, htmlPath+'/'+str(link1)+str(link2)+'TimeTraces'+'.html')
        #mpld3.show()
        
        
    f1=plt.figure()
    ax=f1.add_subplot(111)
    matrixCov=np.zeros((nbProbes*(nbProbes-1),nbProbes*(nbProbes-1)))*float('nan')
    links=[]
    yticks=[]
    xticks=[]
    yticks_labels=[]
    xticks_labels=[]
    
    for src in range (nbProbes):
        for dst in range (nbProbes):
            if src!=dst:
                links.append((src,dst))
    
    for j in range(np.shape(links)[0]) :
        l1=links[j]
        for i in range(j,np.shape(links)[0]) :
            l2=links[i]
            src1=l1[0]
            dst1=l1[1]
            src2=l2[0]
            dst2=l2[1]
            rttLink1=rtt3IPPath[src1][dst1]
            rttLink2=rtt3IPPath[src2][dst2]
            if len(np.ma.getdata(rttLink1))!=np.ma.count_masked(rttLink1) and len(np.ma.getdata(rttLink2))!=np.ma.count_masked(rttLink2) :
                aux= np.ma.corrcoef(rttLink1, rttLink2)
                matrixCov[j][i] =aux[0][1]
                matrixCov[i][j] =aux[1][0]    
                if 1-np.abs(aux[0][1]) <0.2 and i!=j and l2 != l1[::-1] : #only display ticks of highly correlted links and which are not the same RTT (correlation in (-0.8,0.8))
                   yticks_labels.append(str((src1,dst1)))
                   xticks_labels.append(str((src2,dst2)))
                   yticks.append([j])
                   xticks.append([i])              
            else :
                matrixCov[j][i]=float('nan')     
    im=ax.imshow(matrixCov, cmap=plt.cm.jet,interpolation='nearest')
    ax.set_title('Links\' Covariance')
    allCov=np.ravel(matrixCov)
    noNan=~np.isnan(allCov)
 
    f1.subplots_adjust(right=0.8)
    cbar_ax = f1.add_axes([0.85, 0.25, 0.02, 0.5])
    f1.colorbar(im,cax=cbar_ax)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticks_labels,fontsize='8')
    ax.set_xticklabels(xticks_labels,rotation='vertical',fontsize='8')
    #f1.savefig(picturesPath + '/matrixCov.eps')

    try :
        cid = f1.canvas.mpl_connect('button_press_event', onclickTimeTraces)
        plt.gcf().autofmt_xdate()
        plt.draw()
        #f1.savefig(picturesPath+'/matrixCov.eps')

        #mpld3.save_html(f1, htmlPath+'/matrixCov.html')
        #mpld3.show()
        
    except: 
        f1.canvas.mpl_disconnect(cid)
  
    
    
    f2=plt.figure()
    ax2=f2.add_subplot(111)
    ax2.grid(True)
    probilities, bins, patches = ax2.hist(np.extract(noNan,allCov),bins=100, label = 'Histogram')
    #ax2.set_title('Histogram of Links\' Covariance')



    # add plugins for probilities
    labelsBinCenters = [round(bar.get_height(),2) for bar in patches]
    ids = [utils.get_id(bar) for bar in patches]
    plugins.connect(f2, BarLabelToolTip(ids, labelsBinCenters))
        
    

    #f2.savefig(picturesPath + '/histoCov.eps')
    #plt.show()
    # to save image
    #s2 = mpld3.fig_to_html(f)
    mpld3.save_html(f2, htmlPath+'/histoCov.html')
    #mpld3.show()

    #return s, s1, s2

# TO DO PLUGINS    
def showMatrixDiffRttMinRttPathLength(rtt3MinRTTPath, rtt3IPPath, hops3MinRTTPath, diffRTT3Percentage,nbProbes,picturesPath, htmlPath):
    '''
    Shows a matrix representation of the mean difference between the RTT of the direct (IP) path and the min RTT path, for all origin destination couples
    Shows also the mean number of hops of the min RTT path. On mouse click shows time series of direct path RTT, min RTT path RTT, and min RTT path number of hops.
    @param rtt3MinRTTPath: RTT of the path with the minimum RTT, between each origin destination couple, time series
    @type rtt3MinRTTPath: list, 3-dimensional matrix [src][dst][nbMif len(np.ma.getdata(rttLink1))!=np.ma.count_masked(rttLink1) and len(np.ma.getdata(rttLink2))!=np.ma.count_masked(rttLink2) :easure]
    @param rtt3IPPath: RTT of the direct (IP) path between each origin destination couple, time series 
    @type rtt3IPPath: list, 3-dimensional matrix [src][dst][nbMeasure]
    @param hops3MinRTTPath: number of hops of the min RTT path between each origin destination couple, time series 
    @param diffRTT3Percentage: difference of RTT between the IP path and the  path with the minimum RTT, expressed between each origin destination couple, time series
    @type diffRTT3Percentage:   list, 3-dimensional matrix [src][dst][nbMeasure]   
    @type hops3MinRTTPath: list, 3-dimensional matrix [src][dst][nbMeasure]
    @param nbProbes: number of probes considered
    @type nbProbes: int
    '''
    class MouseXYPosition(plugins.PluginBase):
        """Like MousePosition, but only show the X coordinate"""

        JAVASCRIPT="""
        mpld3.register_plugin("mousexyposition", MouseXYPositionPlugin);
        MouseXYPositionPlugin.prototype = Object.create(mpld3.Plugin.prototype);
        MouseXYPositionPlugin.prototype.constructor = MouseXYPositionPlugin;
        MouseXYPositionPlugin.prototype.requiredProps = [];
        MouseXYPositionPlugin.prototype.defaultProps = {
          fontsize: 12,
          fmt: "0d"
        };
        function MouseXYPositionPlugin(fig, props) {
          mpld3.Plugin.call(this, fig, props);
          }
        MouseXYPositionPlugin.prototype.draw = function() {
            var fig = this.fig;
            var fmt = d3.format(this.props.fmt);
            var coords = fig.canvas.append("text")
                                    .attr("class", "mpld3-coordinates")
                                    .style("text-anchor", "end")
                                    .style("font-size", this.props.fontsize)
                                    .attr("x", this.fig.width - 5)
                                    .attr("y", this.fig.height - 5);

       for (var i = 0; i < this.fig.axes.length; i++) {
              var update_coods= function() {
                  var ax = fig.axes[i];
                  return function(){
                  var pos = d3.mouse(this),
                  x = Math.round(ax.x.invert(pos[0])),
                  y = Math.round(ax.y.invert(pos[1]));
                  coords.text("(src: " + fmt(x) + ", dst: " + fmt(y) + ")");
                };
              }();
              fig.axes[i].baseaxes
                  .on("mousemove", update_coods)
                  .on("mouseout", function() { coords.text(""); });
            }
        };"""
        def __init__(self, fontsize=12, fmt="8.0f"):
            self.dict_ = {"type": "mousexyposition",
                          "fontsize": fontsize,
                          "fmt": fmt}
        
    def onclickTimeTraces(event):
        '''
        On mouse click callback, displays time series for RTT of direct (IP) path and min RTT path, and time series for number of hops of the min RTT path 
        '''
        print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              (event.button, event.x, event.y, event.xdata, event.ydata))
        showDefaultTimeShortestTime(rtt3IPPath, rtt3MinRTTPath, int(np.round(event.ydata)), int(np.round(event.xdata)), picturesPath, htmlPath)
        showPathLength(np.array(hops3MinRTTPath), int(np.round(event.ydata)), int(np.round(event.xdata)), picturesPath, htmlPath)
    
    '''
    matrixMean=np.zeros((nbProbes,nbProbes))
    matrixMaxLength=np.zeros((nbProbes,nbProbes))
    for src in range (nbProbes):
        for dst in range (nbProbes):
            if src==dst or len(np.ma.getdata(rtt3IPPath[src][dst]))==np.ma.count_masked(rtt3IPPath[src][dst])    :
                matrixMean[src][dst] = float('nan')
                matrixMeanLength[src][dst] = float('nan')
            else:
                matrixMean[src][dst] = np.ma.mean(diffRTT3Percentage[src][dst])
                matrixMeanLength[src][dst]= np.ma.mean(hops3MinRTTPath[src][dst])
    '''
    #replace by maked array functions 
    matrixMean=np.ma.filled(np.ma.mean(diffRTT3Percentage, axis=2), fill_value = float('nan'))
    matrixMeanLength=np.ma.filled(np.ma.mean(hops3MinRTTPath, axis=2), fill_value = float('nan'))
    f = plt.figure()
    ax = f.add_subplot(111)
    #imshow portion
    im=ax.imshow(matrixMean, cmap=plt.cm.jet, vmin=0, vmax=100, interpolation='nearest')
    for src in range (nbProbes):
        for dst in range (nbProbes):
            if not np.isnan(float(matrixMeanLength[src][dst]))  :
                c = str(int(np.round(matrixMeanLength[src][dst])))
                ax.text(dst, src, c, va='center', ha='center',weight='bold')
    #set tick marks for grid
    ax.set_xticks(range(nbProbes))
    ax.set_xticklabels(range(nbProbes))
    ax.set_xlabel('Dst probe Id')
    ax.set_yticks(range(nbProbes))
    ax.set_yticklabels(range(nbProbes))
    ax.set_ylabel('Src probe Id')
    #ax.set_title('Colored squares: mean dfference between direct link delay and min delay path (% of direct link delay)\n On top: mean path length of the min delay path')
    f.subplots_adjust(right=0.8)
    cbar_ax = f.add_axes([0.85, 0.15, 0.05, 0.7])
    p = f.colorbar(im,cax=cbar_ax,cmap=plt.cm.jet)
    mpld3.plugins.connect(f, MouseXYPosition())
    #mpld3.save_html(f, htmlPath+'/matrixDifMeanPercent.html')
    mpld3.show()

    try :
        cid = f.canvas.mpl_connect('button_press_event', onclickTimeTraces)
        plt.gcf().autofmt_xdate()
        #f.savefig(picturesPath + '/matrixDifMeanPercent.eps')
        plt.show()
    except: 
        f.canvas.mpl_disconnect(cid)
    

# TO DO PLUGINS    
def showMatrixMeanDelays(rtt3MeanDelay, rtt3MeanShortestDelay, nbProbes, picturesPath, htmlPath):
    '''
    Shows a matrix representation of mean direct delay and mean shortest delay, for all origin destination couples
    @param rtt3MeanDelay: Mean Delay of the direct path, between each origin destination couple
    @type rtt3MeanDelay: list, 2-dimensional matrix [src][dst]
    @param rtt3IPPath: Mean Delay of the minimum delay path, between each origin destination couple
    @type rtt3IPPath: list, 2-dimensional matrix [src][dst]
    @param nbProbes: number of probes considered
    @type nbProbes: int
    '''
    class MouseXYPosition(plugins.PluginBase):
        """Like MousePosition, but only show the X coordinate"""

        JAVASCRIPT="""
        mpld3.register_plugin("mousexyposition", MouseXYPositionPlugin);
        MouseXYPositionPlugin.prototype = Object.create(mpld3.Plugin.prototype);
        MouseXYPositionPlugin.prototype.constructor = MouseXYPositionPlugin;
        MouseXYPositionPlugin.prototype.requiredProps = [];
        MouseXYPositionPlugin.prototype.defaultProps = {
          fontsize: 12,
          fmt: "0d"
        };
        function MouseXYPositionPlugin(fig, props) {
          mpld3.Plugin.call(this, fig, props);
          }
        MouseXYPositionPlugin.prototype.draw = function() {
            var fig = this.fig;
            var fmt = d3.format(this.props.fmt);
            var coords = fig.canvas.append("text")
                                    .attr("class", "mpld3-coordinates")
                                    .style("text-anchor", "end")
                                    .style("font-size", this.props.fontsize)
                                    .attr("x", this.fig.width - 5)
                                    .attr("y", this.fig.height - 5);

       for (var i = 0; i < this.fig.axes.length; i++) {
              var update_coods= function() {
                  var ax = fig.axes[i];
                  return function(){
                  var pos = d3.mouse(this),
                  x = Math.round(ax.x.invert(pos[0])),
                  y = Math.round(ax.y.invert(pos[1]));
                  coords.text("(src: " + fmt(x) + ", dst: " + fmt(y) + ")");
                };
              }();
              fig.axes[i].baseaxes
                  .on("mousemove", update_coods)
                  .on("mouseout", function() { coords.text(""); });
            }
        };"""
        def __init__(self, fontsize=12, fmt="8.0f"):
            self.dict_ = {"type": "mousexyposition",
                          "fontsize": fontsize,
                          "fmt": fmt}
        
    
  
    f,(ax1,ax2)=plt.subplots(1,2)
    vmax=np.max(rtt3MeanDelay)
    vmin=np.min(rtt3MeanShortestDelay)
    print(vmin,vmax)
    ax1.imshow(rtt3MeanDelay, cmap=plt.cm.jet, vmin=vmin, vmax=vmax, interpolation='nearest')
    im=ax2.imshow(rtt3MeanShortestDelay, cmap=plt.cm.jet, vmin=vmin, vmax=vmax, interpolation='nearest')	
    for ax in [ax1,ax2]:
        ax.set_xticks(range(nbProbes))
        ax.set_xticklabels(range(nbProbes))
        ax.set_xlabel('Dst probe Id')
        ax.set_yticks(range(nbProbes))
        ax.set_yticklabels(range(nbProbes))
        ax.set_ylabel('Src probe Id')
    ax1.set_title('Direct Path')
    ax2.set_title('Optimal Path')
    f.subplots_adjust(right=0.8)
    cbar_ax = f.add_axes([0.85, 0.15, 0.05, 0.7])
    p = f.colorbar(im,cax=cbar_ax)
    mpld3.plugins.connect(f, MouseXYPosition())
    mpld3.save_html(f, htmlPath+'/matrixDelays.html')
    #mpld3.show()
    plt.show()

####################################################################################################
#########################################  main  ###################################################
####################################################################################################
if __name__ == "__main__":
    dataID = "20160808_161300"
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

    
    """Show matrix charts"""
    #showMatrixMeanDelays(rtt3MeanDelay, rtt3MeanShortestDelay, myRttDisplay.nbProbes,myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showMatrixDiffRtt(rtt3DiffPercentNew, myRttDisplay.nbProbes, rtt3MaxDiffPercent, rtt3MinDiffPercent, rtt3MeanDiffPercent, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showMatrixDiffRttMinRttPathLength(rtt3ShortestAllDataTimeNew, rtt3AllDataNew, rtt3PathLengthNew, rtt3DiffPercentNew,myRttDisplay.nbProbes, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showMatrixCovRtt(rtt3ShortestAllDataTimeNew ,myRttDisplay.nbProbes , myRttDisplay.picturesPath, myRttDisplay.htmlPath)

    """show charts by function in outputRtt for all data"""
    #showHistoDifPercent(rtt3DiffPercentNew, "all data", myRttDisplay.nbProbes, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showHistoPathLengthAllCouples(rtt3PathLengthNew, "all data", myRttDisplay.nbProbes, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showCumulativenbTimesPercentDifRTT(rtt3DiffPercentNew, myRttDisplay.nbProbes, myRttDisplay.picturesPath, myRttDisplay.htmlPath)    
    #showCumulativeNbcouplesPercentDifRTT(rtt3MeanDiffPercent, rtt3MaxDiffPercent, rtt3MinDiffPercent, myRttDisplay.nbProbes, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showDefaultTimeShortestTime(rtt3AllDataNew, rtt3ShortestAllDataTimeNew, 8, 1, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showPathLength(rtt3PathLengthNew, 8, 1, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showHistoPathLength(rtt3PathLengthNew, 8, 1, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #plotSrcFixed(rtt3DiffPercentNew, rtt3MeanDiffPercent, 8, myRttDisplay.nbProbes, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showDefaultTime(rtt3AllDataNew, 8, 1, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showHistoDefaultTime(rtt3AllDataNew, 8, 1, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #plotSrcFixedForVisu(rtt3MinDiffPercent, rtt3MeanDiffPercent, rtt3MaxDiffPercent, 8, myRttDisplay.nbProbes, myRttDisplay.picturesPath, myRttDisplay.htmlPath)

    


