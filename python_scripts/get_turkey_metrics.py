from ifis_tools import database_tools as db 
from ifis_tools import asynch_manager as am 
from ifis_tools import series_tools as ser 
import pandas as pd 
import glob 
import numpy as np 

def get_links2(l):
    links = []
    for i in l:
        links.append(i.split('/')[-1].split('_')[0])
    return links
usgs = db.SQL_USGS_at_IFIS()

#Get the link properties
q = db.sql.SQL("select link_id, travel_time07, up_area from pers_nico.master_lambda_vo")
con = db.DataBaseConnect(user='nicolas', password='10A28Gir0')
Lprop = pd.read_sql(q, con, index_col='link_id')
con.close()

perf = ser.performance(links_prop=Lprop, prop_col_names={'travel_time07':'ttime','up_area':'area'}) 
perf.update_dic('4', 
                base=True, 
                path='/Users/nicolas/Parameter_identifiability/data/hlm_outputs/turkey/*vr4*', 
                abr = '4',
               isDataFrame = True,
               DataFrameColumn = 'Q',
               path2linkFunc = get_links2)
perf.update_dic('5', path='/Users/nicolas/Parameter_identifiability/data/hlm_outputs/turkey/*vr5*', 
                path2linkFunc=get_links2, 
                isDataFrame = True, 
                DataFrameColumn = 'Q')
perf.update_dic('6', path='/Users/nicolas/Parameter_identifiability/data/hlm_outputs/turkey/*vr6*', 
                path2linkFunc=get_links2, 
                isDataFrame = True, 
                DataFrameColumn = 'Q')

M = []
for l in perf.links_eval:
    M.append(perf.eval_by_events(l))

M = pd.concat(M)
M.to_msgpack('/Users/nicolas/Parameter_identifiability/data/processed/turkey_event_met.msg')