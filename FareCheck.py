import numpy as np
import pandas as pd
import pylab as P
import csv as csv

of = pd.read_csv('oldfares.csv', header=None, index_col=None)
nf = pd.read_csv('newfares.csv', header=None, index_col=None)
of.columns = ['rt','o','d','fp','OLDur','OLDr','OLDeff','OLDdis','yn']
nf.columns = ['rt','o','d','fp','ur','r','eff','dis','yn']

#Calculation expressions
#Second level calculations (off YOFC)
aof1c = .88
bof1c = .73
dof1c = .51
#Third level calculations (off YOFC)
jc = .26
#Fourth level calculations (off second level calcs)
#YOF9 = YOFC+5
#Fifth level calculations
ue45c = 8
uemnc = 18
#Ninth level calculations
eo8nc = .75

def marketfp(x):
	if(x['o']<x['d']):
		return x['o']+x['d']+x['fp']
	else:
		return x['d']+x['o']+x['fp']

def market(x):
	if(x['o']<x['d']):
		return x['o']+x['d']
	else:
		return x['d']+x['o']

of['mktfp'] = of.apply(marketfp, axis=1)
nf['mktfp'] = nf.apply(marketfp, axis=1)
of = of.drop(['yn','o','d','rt', 'fp'], axis=1)
nf = nf.drop(['yn'], axis=1)
nf = pd.merge(nf, of, on='mktfp')
nf['mkt'] = nf.apply(market, axis=1)

#Calculate YOFC base increase
yofc = pd.DataFrame()
yofc = nf[(nf.fp == 'YOFC')]
increase = float(raw_input('Enter percentage increase: '))
yofc['CALCur'] = yofc['OLDur'].apply(lambda x: x*(1+increase))
yofc['CALCr'] = yofc['CALCur'].apply(lambda x: round(x,0))

#Create duplicate frame for import testing use
yofccalc = pd.DataFrame()
yofccalc = yofc
yofccalc = yofccalc.drop(['eff','dis','OLDur','OLDr','OLDeff','OLDdis','rt','o','d','fp','ur','r','mktfp'], axis=1)
yofccalc.columns = ['mkt','YOFCur','YOFCr']

#Calculate AOF1
aof1 = pd.DataFrame()
aof1 = nf[(nf.fp == 'AOF1')]
aof1 = pd.merge(aof1, yofccalc, on='mkt')
aof1['CALCur'] = aof1['YOFCr'].apply(lambda x: x*(aof1c))
aof1['CALCr'] = aof1['CALCur'].apply(lambda x: round(x,0))
aof1 = aof1.drop(['YOFCur', 'YOFCr'], axis=1)

#Calculate BOF1
bof1 = pd.DataFrame()
bof1 = nf[(nf.fp == 'BOF1')]
bof1 = pd.merge(bof1, yofccalc, on='mkt')
bof1['CALCur'] = bof1['YOFCr'].apply(lambda x: x*(bof1c))
bof1['CALCr'] = bof1['CALCur'].apply(lambda x: round(x,0))
bof1 = bof1.drop(['YOFCur', 'YOFCr'], axis=1)

#Calculate DOF1
dof1 = pd.DataFrame()
dof1 = nf[(nf.fp == 'DOF1')]
dof1 = pd.merge(dof1, yofccalc, on='mkt')
dof1['CALCur'] = dof1['YOFCr'].apply(lambda x: x*(dof1c))
dof1['CALCr'] = dof1['CALCur'].apply(lambda x: round(x,0))
dof1 = dof1.drop(['YOFCur', 'YOFCr'], axis=1)

#Calculate J
j = pd.DataFrame()
j = nf[(nf.fp == 'J')]
j = pd.merge(j,yofccalc, on='mkt')
j['CALCur'] = j['YOFCr'].apply(lambda x: x*(jc))
j['CALCr'] = j['CALCur'].apply(lambda x: round(x,0))
j = j.drop(['YOFCur', 'YOFCr'], axis=1)

#Calculate YOF9
yof9 = pd.DataFrame()
yof9 = nf[(nf.fp == 'YOF9')]
yof9 = pd.merge(yof9,yofccalc, on='mkt')
yof9['CALCur'] = yof9['YOFCr'].apply(lambda x: x + 5)
yof9['CALCr'] = yof9['CALCur'].apply(lambda x: round(x,0))
yof9 = yof9.drop(['YOFCur', 'YOFCr'], axis=1)

#Create duplicate frame for import testing use
aof1calc = pd.DataFrame()
aof1calc = aof1
aof1calc = aof1calc.drop(['eff','dis','OLDur','OLDr','OLDeff','OLDdis','rt','o','d','fp','ur','r','mktfp'], axis=1)
aof1calc.columns = ['mkt','AOF1ur','AOF1r']

#Calculate AOF9
aof9 = pd.DataFrame()
aof9 = nf[(nf.fp == 'AOF9')]
aof9 = pd.merge(aof9,aof1calc, on='mkt')
aof9['CALCur'] = aof9['AOF1r'].apply(lambda x: x + 5)
aof9['CALCr'] = aof9['CALCur'].apply(lambda x: round(x,0))
aof9 = aof9.drop(['AOF1ur', 'AOF1r'], axis=1)

#Create duplicate frame for import testing use
bof1calc = pd.DataFrame()
bof1calc = bof1
bof1calc = bof1calc.drop(['eff','dis','OLDur','OLDr','OLDeff','OLDdis','rt','o','d','fp','ur','r','mktfp'], axis=1)
bof1calc.columns = ['mkt','BOF1ur','BOF1r']

#Calculate BOF9
bof9 = pd.DataFrame()
bof9 = nf[(nf.fp == 'BOF9')]
bof9 = pd.merge(bof9,bof1calc, on='mkt')
bof9['CALCur'] = bof9['BOF1r'].apply(lambda x: x + 5)
bof9['CALCr'] = bof9['CALCur'].apply(lambda x: round(x,0))
bof9 = bof9.drop(['BOF1ur', 'BOF1r'], axis=1)
bof9.info()

#Create duplicate frame for import testing use
dof1calc = pd.DataFrame()
dof1calc = dof1
dof1calc = dof1calc.drop(['eff','dis','OLDur','OLDr','OLDeff','OLDdis','rt','o','d','fp','ur','r','mktfp'], axis=1)
dof1calc.columns = ['mkt','DOF1ur','DOF1r']

#Calculate DOF9
dof9 = pd.DataFrame()
dof9 = nf[(nf.fp == 'DOF9')]
dof9 = pd.merge(dof9,dof1calc, on='mkt')
dof9['CALCur'] = dof9['DOF1r'].apply(lambda x: x + 5)
dof9['CALCr'] = dof9['CALCur'].apply(lambda x: round(x,0))
dof9 = dof9.drop(['DOF1ur', 'DOF1r'], axis=1)

#Calculate UE45
ue45 = pd.DataFrame()
ue45 = nf[(nf.fp == 'UE45')]
ue45 = pd.merge(ue45,bof1calc, on='mkt')
ue45['CALCur'] = ue45['BOF1r'].apply(lambda x: x * ue45c)
ue45['CALCr'] = ue45['CALCur'].apply(lambda x: round(x,0))
ue45 = ue45.drop(['BOF1ur', 'BOF1r'], axis=1)

#Calculate UEMN
uemn = pd.DataFrame()
uemn = nf[(nf.fp == 'UEMN')]
uemn = pd.merge(uemn,bof1calc, on='mkt')
uemn['CALCur'] = uemn['BOF1r'].apply(lambda x: x * uemnc)
uemn['CALCr'] = uemn['CALCur'].apply(lambda x: round(x,0))
uemn = uemn.drop(['BOF1ur', 'BOF1r'], axis=1)

#Calculate EO8N
eo8n = pd.DataFrame()
eo8n = nf[(nf.fp == 'EO8N')]
eo8n = pd.merge(eo8n,dof1calc, on='mkt')
eo8n['CALCur'] = eo8n['DOF1r'].apply(lambda x: x * eo8nc)
eo8n['CALCr'] = eo8n['CALCur'].apply(lambda x: round(x,0))
eo8n = eo8n.drop(['DOF1ur', 'DOF1r'], axis=1)

#Combine all fareplans into one DataFrame and export to .csv
output = pd.DataFrame()
output = pd.concat([yofc, aof1, bof1, dof1, j, yof9, aof9, bof9, dof9, ue45, uemn, eo8n], ignore_index=True)
output.to_csv('output.csv')