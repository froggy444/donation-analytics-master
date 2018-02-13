# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np 
import os 

dataset= pd.read_csv(os.curdir +'/input/itcont.txt',delimiter='|', names=['cmte_id','1 ','2 ','3 ','4 ','5 ','6 ','name','8','9 ','zip','12 ','13 ','date','amount','other_id','16 ','17 ','18 ','19 ','20'],dtype={'zip':object})
dataset['zip']=dataset['zip'].str[0:5]
dataset['date']=dataset['date'] % 10000
dataset=dataset[['cmte_id','name','zip','date','amount','other_id']]
#==============================================================================
# dataset['date_length']= dataset['date'].str.len()
# 
# dataset['lower']=dataset['date_length']-4
# dataset['upper']=dataset['date_length']-1
# dataset['year']= dataset['date'].str[dataset.lower:dataset.upper]
#==============================================================================
dataset
           
#==============================================================================
# #if dataset[dataset['zip'].str.len()==5 | dataset['other_id'] == 'NaN' | dataset['name']!='NaN' | dataset['amount']!='NaN' |  dataset['zip']!='NaN' | dataset['date']!='NaN']:
#     dataset['valid']==true
# else:
#     dataset['valid']==false
# 
#==============================================================================
#asc=dataset.drop(dataset[dataset.valid=false])
#dataset['name']
asc=dataset.groupby(['name','zip']).size().reset_index(name='counts')
dataset2=dataset

newasc=asc.drop(asc[asc.counts < 2].index)
repeated_donors=newasc['name']
asc['repeat_donor']= np.where(asc['name'].isin(repeated_donors), 'yes', 'no')








