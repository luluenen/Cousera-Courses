from flask import render_template, request

from app import app
from app.probe import load_location, get_one_to_all_graph, get_rtt_graph, get_rttHisto_graph, get_rttShortest_graph, get_shortestPL_graph, get_PathInformation_graph, get_shortestPLHisto_graph
from .measures import Measure

msm = Measure()
msm.load_measure_list()


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
                           measures=msm.measures_info)


@app.route('/measure/<int:m_index>')
def full_info(m_index):
    msm.load_msm_creation(m_index)
    probe_l = msm.measures_info[m_index]['more'][0]
    for probe in probe_l:
        load_location(probe)
    return render_template('msm_index.html',
                           id=m_index,
                           measure=msm.measures_info[m_index])


@app.route('/measure/<int:m_index>/parameters')
def show_params(m_index):
    return render_template('parameters.html',
                           id=m_index,
                           measure=msm.measures_info[m_index])


@app.route('/measure/<int:m_index>/probes')
def probes(m_index):
    try:
        probe_l = msm.measures_info[m_index]['more'][0]
    except KeyError:
        msm.load_msm_creation(m_index)
        probe_l = msm.measures_info[m_index]['more'][0]
    if 'location' not in probe_l[0]:
        for probe in probe_l:
            load_location(probe)
    return render_template('probes.html',
                           id=m_index,
                           probes=probe_l)


@app.route('/measure/<int:m_index>/probes/<int:probe_id>')
def view_probe(m_index, probe_id):
    try:
        probe = msm.measures_info[m_index]['more'][0][probe_id]
    except KeyError:
        msm.load_msm_creation(m_index)
        probe = msm.measures_info[m_index]['more'][0][probe_id]
    if 'location' not in probe:
        load_location(probe)
    msm_name = msm.measures_info[m_index]['creation_time']
    probes_l = msm.measures_info[m_index]['more'][0]
    return render_template('probe.html',
                           id=m_index,
                           probe_id=probe_id,
                           probe=probe,
                           probes_list=probes_l,
                           msm_name=msm_name)


@app.route('/measure/<int:m_index>/probes/<int:probe_id>/rtt_to/<int:dest_id>')
def show_rtt_graph(m_index, probe_id, dest_id):
    msm_name = msm.measures_info[m_index]['creation_time']
    html_graph = get_rtt_graph(msm_name, probe_id, dest_id)
    htmlHisto_graph = get_rttHisto_graph(msm_name, probe_id, dest_id)
    return render_template('rtt_graph.html', html_graph=html_graph, htmlHisto_graph=htmlHisto_graph)

@app.route('/measure/<int:m_index>/probes/improvement_from/<int:probe_id>')
def show_improvement_graph(m_index, probe_id):
    msm_name = msm.measures_info[m_index]['creation_time']
    html_graph = get_one_to_all_graph(msm_name,
                                     msm.measures_info[m_index]['nb_probes'],
                                     probe_id)
    return render_template('graph_base.html', my_graph=html_graph)



@app.route('/measure/<int:m_index>/shortest_path')
def shortest_path(m_index):
    path = app.config['DATA_ROOT'] \
           + msm.measures_info[m_index]['creation_time'] + '/'

    # with open(path + app.config['MATRIX_MIN'], 'r') as m_min_f:
    #     min_mtx_html = m_min_f.read()
    with open(path + app.config['MATRIX_AVG'], 'r') as m_avg_f:
        avg_mtx_html = m_avg_f.read()
    # with open(path + app.config['MATRIX_MAX'], 'r') as m_max_f:
    #     max_mtx_html = m_max_f.read()
    with open(path + app.config['PATH_LEN'], 'r') as p_len_f:
        path_len = p_len_f.read()
        
    try:
        probe_l = msm.measures_info[m_index]['more'][0]
    except KeyError:
        msm.load_msm_creation(m_index)
        probe_l = msm.measures_info[m_index]['more'][0]

    return render_template('shortest_path.html',
                           id=m_index,
                           measure=msm.measures_info[m_index],
                           # min_mtx=min_mtx_html,
                           avg_mtx=avg_mtx_html,
                           path_len=path_len,
                           probes=probe_l)
                           # max_mtx=max_mtx_html)


@app.route('/measure/<int:m_index>/improvements')
def improvements(m_index):
    path = app.config['DATA_ROOT'] \
           + msm.measures_info[m_index]['creation_time'] + '/'

    with open(path + app.config['HISTO_DIFF'], 'r') as hist_f:
        hist_html = hist_f.read()

    with open(path + app.config['CUMUL_COUPLES'], 'r') as cumul_f:
        cumul_html = cumul_f.read()

    try:
        probe_l = msm.measures_info[m_index]['more'][0]
    except KeyError:
        msm.load_msm_creation(m_index)
        probe_l = msm.measures_info[m_index]['more'][0]

    return render_template('improvements.html',
                           id=m_index,
                           measure=msm.measures_info[m_index],
                           hist_graph=hist_html,
                           cumul_graph=cumul_html,
                           probes=probe_l)


@app.route('/measure/<int:m_index>/correlation')
def correlation(m_index):
    path = app.config['DATA_ROOT'] \
           + msm.measures_info[m_index]['creation_time'] + '/'

    with open(path + app.config['HISTO_COV'], 'r') as cov_f:
        cov_html = cov_f.read()
    image_matrix_cov_src = path + app.config['MATRIX_COV']

    return render_template('correlation.html',
                           id=m_index,
                           measure=msm.measures_info[m_index],
                           cov_graph=cov_html, image_matrix_cov_src=image_matrix_cov_src)


@app.route('/measure/<int:m_index>/shortest_path/post', methods = ['POST'])
def post(m_index):
    # Get the parsed contents of the form data
    data = request.form
    # Render template
    keys = data.keys()
    srcId = data[keys[1]]
    dstId = data[keys[0]]
    msm_name = msm.measures_info[m_index]['creation_time']
    html_graph1 = get_rttShortest_graph(msm_name, int(srcId), int(dstId))
    html_graph2 = get_shortestPL_graph(msm_name, int(srcId), int(dstId))
    html_graph5=get_shortestPLHisto_graph(msm_name, int(srcId), int(dstId))
    html_graph3, html_graph4 = get_PathInformation_graph (msm_name, int(srcId), int(dstId))
    return render_template('link_shortest.html',
                           id=m_index,
                           measure=msm.measures_info[m_index],
                           srcId=srcId,
                           dstId=dstId,
                           shortest_graph = html_graph1,
                           html_graph2 = html_graph2,
                           html_graph3 = html_graph3,
                           html_graph4 = html_graph4,
                           html_graph5 = html_graph5
                           )



