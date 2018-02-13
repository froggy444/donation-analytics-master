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


dataset['repeat_donor']= np.where(dataset['name'].isin(repeated_donors), 'yes', 'no')

#filtering individual donors 
group_donor=dataset['other_id']
group_donor=group_donor.dropna()

dataset['individual']=np.where(dataset['other_id'].isin(group_donor)  , 'no', 'yes' )
dataset=dataset[dataset.individual=='yes']
#dataset=dataset.loc[dataset['other_id']=='']


#filtering for null conditions 

dataset=dataset[['cmte_id','name','zip','date','amount','repeat_donor']]
dataset.dropna()

#filtering for repeated donors 
dataset=dataset[dataset.repeat_donor=='yes']

yeard=dataset[dataset.date==2018]
yeard2=dataset[dataset.date==2018]

yeard2['running_total']=yeard2['amount']
yeard2['running_percentile']=yeard2['amount']
yeard2['total_cont']=1

#cmp={'zip':[dataset['zip']],'date':[dataset['date']],'amount':[dataset['amount']]}
#
#twod_list=[dataset['cmte_id']]
# twod_list.append(cmp)
length=2
arr=np.array(yeard['amount'])

#        yeard['running_total']=yeard['amount']
#        yeard['running_percentile']=yeard['amount']
#        yeard['total_cont']=yeard['amount']
##    yeard['total']=yeard.cumsum(axis:{index(0),columns(2)}) 
#    else:
percentile1=pd.read_csv(os.curdir +'/input/percentile.txt', names=['perc'], dtype={'perc':int})

s=int(percentile1.iloc[:].values)


for i in range(length):
    if  i==1:
        yeard['running_total']=arr.sum()
        yeard['running_percentile']=np.round(np.percentile(arr,s,interpolation='nearest'))
        yeard['total_cont']=len(arr)



yeard=yeard[['cmte_id','zip','date','running_percentile','running_total','total_cont']]

yeard2=yeard2[['cmte_id','zip','date','running_percentile','running_total','total_cont']]
yeard=yeard[:-1]
yeard2=yeard2[:-1]

y=pd.concat([yeard2,yeard],axis=0)

y.to_csv(os.curdir +'/output/repeat_donors.txt',header=False,index=False, sep='|')

