import json
import os

import requests

from app import app
from app.jsonFile import JsonFile
from app.rttDisplayForVisu import plotSrcFixed, showDefaultTime, showHistoDefaultTime, showDefaultTimeShortestTime, showPathInformation
from app.rttDisplayForVisu import *

def load_location(probe):
    # Free API for 1000 daily requests
    loc = requests.get('http://ipinfo.io/' + probe['ip_address'])
    probe['location'] = json.loads(loc.content.replace('\n', ''))
    root = app.config['STATIC_ROOT']
    with open(root + 'ref/countries.json') as country_f:
        countries = json.load(country_f)
    probe['location']['country_name'] = countries[probe['location']['country']]


def get_one_to_all_graph(msm_name, nb_probes, probe_id):
    root = app.config['DATA_ROOT']
    f_name = root + msm_name + '/graphs/generated/src_' + str(probe_id) \
        + '_difPercentage.html'
    if not os.path.isfile(f_name):
        create_one_to_all_graph(msm_name, nb_probes, probe_id)
    with open(f_name, 'r') as graph_file:
        probe_gr_html = graph_file.read()
    return probe_gr_html


def create_one_to_all_graph(msm_name, nb_probes, probe_id):
    root = app.config['DATA_ROOT'] + msm_name
    json_path = root + '/output/'

    rtt3Max = JsonFile(json_path + 'MaxdiffPercent.json').read_data()
    rtt3Min = JsonFile(json_path + 'MindiffPercent.json').read_data()
    rtt3Avg = JsonFile(json_path + 'MeandiffPercent.json').read_data()
    html_path = root + '/graphs/generated'
    if not os.path.isdir(html_path):
        os.mkdir(html_path)

    plotSrcFixed(rtt3Min, rtt3Avg, rtt3Max,
                 probe_id,
                 nb_probes,
                 html_path)


def create_rtt_graph(msm_name, src, dst):
    root = app.config['DATA_ROOT'] + msm_name
    json_path = root + '/output/'
    html_path = root + '/graphs/generated'
    rtt_3_diff_percent_new = JsonFile(json_path + 'AllData.json').read_data()
    showDefaultTime(rtt_3_diff_percent_new, src, dst, html_path)


def get_rtt_graph(msm_name, src, dst):
    root = app.config['DATA_ROOT'] + msm_name
    html_path = root + '/graphs/generated'
    f_name = html_path + '/' + str(src) + '_' + str(dst) + '.html'
    if not os.path.isfile(f_name):
        create_rtt_graph(msm_name, src, dst)
    with open(f_name, 'r') as graph_file:
        probe_gr_html = graph_file.read()
    return probe_gr_html

def create_rttHisto_graph(msm_name, src, dst):
    root = app.config['DATA_ROOT'] + msm_name
    json_path = root + '/output/'
    html_path = root + '/graphs/generated'
    rtt_3_diff_percent_new = JsonFile(json_path + 'AllData.json').read_data()
    showHistoDefaultTime(rtt_3_diff_percent_new, src, dst, html_path)


def get_rttHisto_graph(msm_name, src, dst):
    print 'enter histo get histo'
    root = app.config['DATA_ROOT'] + msm_name
    html_path = root + '/graphs/generated'
    f_name = html_path + '/' + str(src)+ "_" +str(dst)+"_Histo"+ '.html'
    if not os.path.isfile(f_name):
        create_rttHisto_graph(msm_name, src, dst)
    with open(f_name, 'r') as graph_file:
        probe_gr_html = graph_file.read()
    return probe_gr_html

def create_rttShortest_graph(msm_name, src, dst):
    root = app.config['DATA_ROOT'] + msm_name
    json_path = root + '/output/'
    html_path = root + '/graphs/generated'
    rtt_3_alldata_new = JsonFile(json_path + 'AllData.json').read_data()
    rtt_3_shortest = JsonFile(json_path + 'ShortestTime.json').read_data()
    showDefaultTimeShortestTime(rtt_3_alldata_new, rtt_3_shortest, src, dst, html_path)


def get_rttShortest_graph(msm_name, src, dst):
    root = app.config['DATA_ROOT'] + msm_name
    html_path = root + '/graphs/generated'
    name =  str(src)+ "_" +str(dst)+"_DT_ST"
    f_name = html_path + '/' + name+ '.html'
    if not os.path.isfile(f_name):
        create_rttShortest_graph(msm_name, src, dst)
    with open(f_name, 'r') as graph_file:
        probe_gr_html = graph_file.read()
    return probe_gr_html


def create_shortestPL_graph(msm_name, src, dst):
    root = app.config['DATA_ROOT'] + msm_name
    json_path = root + '/output/'
    html_path = root + '/graphs/generated'
    rtt_3_shortest = JsonFile(json_path + 'ShortestPathLength.json').read_data()
    showPathLength( rtt_3_shortest, src, dst, html_path)


def get_shortestPL_graph(msm_name, src, dst):
    root = app.config['DATA_ROOT'] + msm_name
    html_path = root + '/graphs/generated'
    name = str(src)+"_"+str(dst)+"SPL"
    f_name = html_path + '/' + name+ '.html'
    if not os.path.isfile(f_name):
        create_shortestPL_graph(msm_name, src, dst)
    with open(f_name, 'r') as graph_file:
        probe_gr_html = graph_file.read()
    return probe_gr_html

def create_shortestPLHisto_graph(msm_name, src, dst):
    root = app.config['DATA_ROOT'] + msm_name
    json_path = root + '/output/'
    html_path = root + '/graphs/generated'
    rtt_3_shortest = JsonFile(json_path + 'ShortestPathLength.json').read_data()
    showHistoPathLength( rtt_3_shortest, src, dst, html_path)


def get_shortestPLHisto_graph(msm_name, src, dst):
    root = app.config['DATA_ROOT'] + msm_name
    html_path = root + '/graphs/generated'
    name =  str(src)+ "_" +str(dst)+"_HistoPL"
    f_name = html_path + '/' + name+ '.html'
    if not os.path.isfile(f_name):
        create_shortestPLHisto_graph(msm_name, src, dst)
    with open(f_name, 'r') as graph_file:
        probe_gr_html = graph_file.read()
    return probe_gr_html

def create_PathInformation_graph(msm_name, src, dst):
    root = app.config['DATA_ROOT'] + msm_name
    json_path = root + '/calculateData/'
    html_path = root + '/graphs/generated'
    with open (json_path + 'informationDictResult.json', "r") as fs:
        print 'enter read'
        informationDict = json.load(fs)
    showPathInformation(src, dst, informationDict, html_path) 


def get_PathInformation_graph(msm_name, src, dst):
    print "enter get_PathInformation_graph"
    root = app.config['DATA_ROOT'] + msm_name
    html_path = root + '/graphs/generated'
    name1 =  str(src)+ "_" +str(dst)+"meanTime_pathInformation"
    name2 =  str(src)+ "_" +str(dst)+"meanDiffpercent_pathInformation"
    f_name1 = html_path + '/' + name1+ '.html'
    f_name2 = html_path + '/' + name2+ '.html'
    filesList = [f_name1, f_name2]
    filesExist = [f for f in filesList if (os.path.isfile(f) and os.path.getsize(f)>0)]
    filesNoExist = list(set(filesExist)^set(filesList))
    if filesNoExist:
        create_PathInformation_graph(msm_name, src, dst)
    with open(f_name1, 'r') as graph_file1:
        probe_gr_html1 = graph_file1.read()
    with open(f_name2, 'r') as graph_file2:
        probe_gr_html2 = graph_file2.read()
    return probe_gr_html1, probe_gr_html2
















