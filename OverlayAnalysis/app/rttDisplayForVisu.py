import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import mpld3
from mpld3 import plugins, utils
import collections

#import pandas module----sudo pip install pandas 
import pandas as pd

# Define some CSS to control our custom labels
css = """
.mpld3-tooltip table, .mpld3-tooltip th, .mpld3-tooltip td
{
    font-family:Arial, Helvetica, sans-serif;
    border: 1px solid #ccc;
    text-align: right;
}
.mpld3-tooltip table
{
    border-collapse: collapse;
    position: relative;
}
.mpld3-tooltip th
{
    color: #ffffff;
    background-color: #cccccc;
}
.mpld3-tooltip td
{
    background-color: #ECECEC;
}
"""


def plotSrcFixed(rtt3Min, rtt3Mean, rtt3Max,  src, nbProbes, htmlPath):
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
    path = "../../../../../static/js/mpld3/"
    mpld3.save_html(f, htmlPath+'/' + name + '.html',
                    d3_url=path+"d3.v3.min.js",
                    mpld3_url=path+"mpld3.v0.3git.min.js")
    
# with plugins for points values show in a table commented, to reduce image size
def showDefaultTime(rtt3Data, src, dst, htmlPath):
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
            if total_valid_values == 0:
                html_str = '''
                <!DOCTYPE html>
                <html>
                <body>

                <p>No valide measurement to show direct path delay</p>

                </body>
                </html>'''
                name =str(src)+ "_" +str(dst)
                f_name = htmlPath+'/' + name + '.html'
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
                path = "../../../../../static/js/mpld3/"
                mpld3.save_html(f, htmlPath+'/' + name + '.html',
                            d3_url=path+"d3.v3.min.js",
                            mpld3_url=path+"mpld3.v0.3git.min.js")
        else :
            print ("ValueError")



# DONE
def showHistoDefaultTime(rtt3Data, src, dst, htmlPath):
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
            f_name = htmlPath+'/' + name + '.html'
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
            path = "../../../../../static/js/mpld3/"
            mpld3.save_html(f, htmlPath+'/' + name + '.html',
                            d3_url=path+"d3.v3.min.js",
                            mpld3_url=path+"mpld3.v0.3git.min.js")

               
        
# DONE
def showDefaultTimeShortestTime(rtt3Data, rtt3ShortestTime, src, dst, htmlPath):
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
            name =  str(src)+ "_" +str(dst)+"_DT_ST"
            
            path = "../../../../../static/js/mpld3/"
            mpld3.save_html(f, htmlPath+'/' + name + '.html',
                            d3_url=path+"d3.v3.min.js",
                            mpld3_url=path+"mpld3.v0.3git.min.js")


        else :
            html_str = '''
            <!DOCTYPE html>
            <html>
            <body>

            <p>No valide measurement for this link</p>

            </body>
            </html>'''
            name =  str(src)+ "_" +str(dst)+"_DT_ST"
            f_name = htmlPath+'/' + name + '.html'
            Html_file= open(f_name,"w")
            Html_file.write(html_str)
            Html_file.close()






# DONE
def showHistoPathLength(rtt3ShortestPathLength, src, dst, htmlPath):

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
        name =  str(src)+ "_" +str(dst)+"_HistoPL"
        path = "../../../../../static/js/mpld3/"
        mpld3.save_html(f, htmlPath+'/' + name + '.html',
                        d3_url=path+"d3.v3.min.js",
                        mpld3_url=path+"mpld3.v0.3git.min.js")
    else :
        html_str = '''
        <!DOCTYPE html>
        <html>
        <body>

        <p>No valide measurement for this link</p>

        </body>
        </html>'''
        name =  str(src)+ "_" +str(dst)+"_HistoPL"
        f_name = htmlPath+'/' + name + '.html'
        Html_file= open(f_name,"w")
        Html_file.write(html_str)
        Html_file.close()


# plugins too large
def showPathLength(shortestPathLength, src, dst, htmlPath):
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
        
        #to save image 
        name = str(src)+"_"+str(dst)+"SPL"
        path = "../../../../../static/js/mpld3/"
        mpld3.save_html(f, htmlPath+'/' + name + '.html',
                        d3_url=path+"d3.v3.min.js",
                        mpld3_url=path+"mpld3.v0.3git.min.js")
    else :
        html_str = '''
        <!DOCTYPE html>
        <html>
        <body>

        <p>No valide measurement for this link</p>

        </body>
        </html>'''
        name = str(src)+"_"+str(dst)+"SPL"
        f_name = htmlPath+'/' + name + '.html'
        Html_file= open(f_name,"w")
        Html_file.write(html_str)
        Html_file.close()
    

# TO DO PLUGINS     
def showTraceTwoLinks(rtt3, link1, link2, htmlPath):
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
        #s = mpld3.fig_to_html(f)
        path = "../../../../../static/js/mpld3/"
        mpld3.save_html(f, htmlPath+'/' + name + '.html',
                        d3_url=path+"d3.v3.min.js",
                        mpld3_url=path+"mpld3.v0.3git.min.js")
        #mpld3.show()
        

def showPathInformation(src, dst, informationDict, htmlPath):
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
    def autolabel(rects, ylabels, ax):
        # attach some text labels
        for i in range(len(rects)):
            height = rects[i].get_height()
            ax.text(rects[i].get_x() + rects[i].get_width()/2., height,
                    '%s' % ylabels[i],
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
        autolabel(rects1, ylabels1, ax1)
        plt.suptitle('Shortest routes path nbTimes, meanTime representation')
        name1 =  str(src)+ "_" +str(dst)+"meanTime_pathInformation"
        path = "../../../../../static/js/mpld3/"
        mpld3.save_html(f, htmlPath+'/' + name1 + '.html',
                        d3_url=path+"d3.v3.min.js",
                        mpld3_url=path+"mpld3.v0.3git.min.js")

        #mpld3.show()
        
        
        f1=plt.figure(2)
        ax2 = f1.add_subplot(111)
        rects2 = ax2.bar(x-0.5*width, y , width, color='b')
        ax2.set_ylabel('nbTimes appear')
        ax2.set_xticks(x)
        ax2.set_xticklabels(xticklabels)
        autolabel(rects2, ylabels2, ax2)
        plt.suptitle('Shortest routes path nbTimes, meanDiffpercent representation')
        #plt.show()
        #f.show()
        name2 =  str(src)+ "_" +str(dst)+"meanDiffpercent_pathInformation"
        path = "../../../../../static/js/mpld3/"
        mpld3.save_html(f1, htmlPath+'/' + name2 + '.html',
                        d3_url=path+"d3.v3.min.js",
                        mpld3_url=path+"mpld3.v0.3git.min.js")
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
        f_name = htmlPath+'/' + name1 + '.html'
        Html_file= open(f_name,"w")
        Html_file.write(html_str)
        Html_file.close()
        
        f_name2 = htmlPath+'/' + name2 + '.html'
        Html_file2= open(f_name2,"w")
        Html_file2.write(html_str)
        Html_file2.close()
        




####################################################################################################
#########################################  Examples  ###################################################
####################################################################################################
    
    """Load data from json files"""
    # rtt3AllDataNew = myRttDisplay.rtt3AllDataFile.read_data()
    # rtt3ShortestAllDataTimeNew = myRttDisplay.rtt3ShortestTimeFile.read_data()
    # rtt3PathLengthNew = myRttDisplay.rtt3LengthPathFile.read_data()
    # rtt3DifferenceNew = myRttDisplay.rtt3DifferenceFile.read_data()
    # rtt3DiffPercentNew = myRttDisplay.rtt3DiffPercentFile.read_data()
    """Load data from json files"""
    # rtt3MaxDiffPercent = myRttDisplay.rtt3MaxdiffPercentFile.read_data()
    # rtt3MinDiffPercent = myRttDisplay.rtt3MindiffPercentFile.read_data()
    # rtt3MeanDiffPercent = myRttDisplay.rtt3MeandiffPercentFile.read_data()
    
    """Show matrix charts"""
    #showMatrixDiffRtt(rtt3DiffPercentNew, myRttDisplay.nbProbes, rtt3MaxDiffPercent, rtt3MinDiffPercent, rtt3MeanDiffPercent, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showMatrixDiffRttMinRttPathLength(rtt3ShortestAllDataTimeNew, rtt3AllDataNew, rtt3PathLengthNew, rtt3DiffPercentNew,myRttDisplay.nbProbes, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showMatrixCovRtt(rtt3ShortestAllDataTimeNew ,myRttDisplay.nbProbes , myRttDisplay.picturesPath, myRttDisplay.htmlPath)

    """show charts by function in outputRtt for all data"""
    #s = showHistoDifPerccent(rtt3DiffPercentNew, "all data", myRttDisplay.nbProbes, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showHistoPathLengthAllCouples(rtt3PathLengthNew, "all data", myRttDisplay.nbProbes, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showCumulativenbTimesPercentDifRTT(rtt3DiffPercentNew, myRttDisplay.nbProbes, myRttDisplay.picturesPath, myRttDisplay.htmlPath)    
    #showCumulativeNbcouplesPercentDifRTT(rtt3MeanDiffPercent, rtt3MaxDiffPercent, rtt3MinDiffPercent, myRttDisplay.nbProbes, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showDefaultTimeShortestTime(rtt3AllDataNew, rtt3ShortestAllDataTimeNew, 8, 1, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showPathLength(rtt3PathLengthNew, 8, 1, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showHistoPathLength(rtt3PathLengthNew, 8, 1, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #plotSrcFixed(rtt3MinDiffPercent, rtt3MeanDiffPercent, rtt3MaxDiffPercent, 8, myRttDisplay.nbProbes, myRttDisplay.picturesPath, myRttDisplay.htmlPath)
    #showDefaultTime(rtt3AllDataNew, 8, 1, myRttDisplay.picturesPath, myRttDisplay.htmlPath)

    


