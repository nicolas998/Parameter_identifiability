import read_dat as rd
from ifis_tools import series_tools as ser 
import pandas as pd 
import numpy as np 
import glob

path = '/Users/nicolas/Parameter_identifiability/data/'
#Get the information of the links and the simulated streamflow for the reference scenario
Qref = pd.read_msgpack(path+'processed/qref_all_sta_vr4.msg')
prop = pd.read_msgpack(path+'processed/links_prop.msg')
dates = pd.read_msgpack(path+'processed/south_event_dates.msg')
dates_start = dates['start'].values
dates_end = dates['end'].values
perf = ser.performance()

#Get the list of the control points list 
Ne, Nrec = rd.get_size(path + 'for_hlm/south_skunk/events/out_1_1.dat')
control, data = rd.get_data(path + 'for_hlm/south_skunk/events/out_1_1.dat', Ne, Nrec)

#Define functions to read the data
def get_event_data(path, event, links_list):
    #Read the list of existing dat for the event
    L = glob.glob(path+str(event)+'.dat')
    L.sort()
    #Read the data of the scenarios for the event
    di = {}
    for p in L:
        case = p.split('out')[-1].split('_')[1]
        ncont, nint = rd.get_size(p)
        cont, data = rd.get_data(p, ncont, nint)
        Dd = pd.DataFrame(data.T, index=Qref[dates_start[event-1]:dates_end[event-1]].index, columns=cont)
        di.update({case: Dd[links_list]})
    return di

def get_performance(path, event, control):
    #Read the data
    data = get_event_data(path, event, control)
    idx = data['1'].index

    KGE = []
    DIS = []
    #Iterates through the scenarios
    for k in data.keys():
        #Iterates through the stations    
        K = []; D = []
        for sta in control:
            K.append(perf.__func_KGE__(Qref[sta][idx], data[k][sta]))
            dt = perf.__func_qpeakTimeDiff__(Qref[sta][idx], data[k][sta]) / prop.loc[sta]['ttime']
            dq = perf.__func_qpeakMagDiff__(Qref[sta][idx], data[k][sta])
            D.append(1-np.sqrt((dt**2) + (dq**2)))
        KGE.append(K)
        DIS.append(D)
    KGE = pd.DataFrame(np.array(KGE).T, index=control, columns=list(data.keys()))
    DIS = pd.DataFrame(np.array(DIS).T, index=control, columns=list(data.keys()))
    return KGE, DIS

#Read the data and obtain the performance, then writes the results to some tables
k,d = get_performance(path + 'for_hlm/south_skunk/events/out_*_',1, control)
d.to_msgpack(path + 'hlm_outputs/south/scenarios_level5/perf_qp_dist_1.msg')
k.to_msgpack(path + 'hlm_outputs/south/scenarios_level5/perf_kge_1.msg')

