from ifis_tools import asynch_manager as am 
import pandas as pd 

names = {'south': {'path': '/Users/nicolas/Parameter_identifiability/data/for_hlm/south_skunk/'},
        'turkey':{'path':'/Users/nicolas/Parameter_identifiability/data/for_hlm/turkey/'}} 

name = 'south' #Choose between south and turkey
setup = '4' #Choose betweeen 4, 5 and 6

data = am.hlm_dat_process(names[name]['path'] + 'control_vr4.sav')
data.dat_all2pandas(names[name]['path'], 
    '/Users/nicolas/Parameter_identifiability/data/hlm_outputs/'+name+'/',
    start_date='-03-01 01:00',
    start_year = 2002,
    initial_name = 'out_'+setup+'_',     
    stages='all',
    nickname = 'vr'+setup,
    stages_names=['Q'], 
    search = 2)