import numpy as np
import pandas as pd
import pylab as P
import csv as csv

of = pd.read_csv('oldfares.csv', header=None, index_col=None)
nf = pd.read_csv('newfares.csv', header=None, index_col=None)
of.columns = ['rt','o','d','fp','OLDur','OLDr','OLDeff','OLDdis','yn']
nf.columns = ['rt','o','d','fp','ur','r','eff','dis','yn']

#Calculation expressions
#First level calculations (off YOFC)
aof1c = .90
bof1c = .80
dof1c = .60

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

aof1.to_csv('output.csv')