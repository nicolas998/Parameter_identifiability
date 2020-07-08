from ifis_tools import asynch_manager as am 
import pandas as pd 


data = am.hlm_dat_process('/Users/nicolas/04_DA/control_prun.sav')
for i in ['et_001']:#setups.index:
    i = str(i)
    data.dat_all2pandas('/Users/nicolas/04_DA/andrew/001', 
        'outputs/et01/',
        start_date='-03-01 01:00',
        start_year = 2008,
        initial_name = 'out_'+str(i)+'_',     
        stages='all',
        nickname = 'po',
        stages_names=['Q'], 
        search = 2)