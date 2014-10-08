import numpy as np
import pandas as pd
import pylab as P
import csv as csv

of = pd.read_csv('oldfares.csv', header=None, index_col=None)
nf = pd.read_csv('newfares.csv', header=None, index_col=None)
of.columns = ['rt','o','d','fp','OLDur','OLDr','OLDeff','OLDdis','yn']
nf.columns = ['rt','o','d','fp','ur','r','eff','dis','yn']

def market(x):
	if(x['o']<x['d']):
		return x['o']+x['d']+x['fp']
	else:
		return x['d']+x['o']+x['fp']

of['mkt'] = of.apply(market, axis=1)
nf['mkt'] = nf.apply(market, axis=1)
of = of.drop(['yn','o','d','rt','fp'], axis=1)
nf = nf.drop(['yn'], axis=1)
nf = pd.merge(nf, of, on='mkt')

#Calculate YOFC base increase
yofc = pd.DataFrame()
yofc = nf[(nf.fp == 'YOFC')]
increase = float(raw_input('Enter percentage increase: '))
yofc['CALCur'] = yofc['OLDur'].apply(lambda x: x*(1+increase))
yofc['CALCr'] = yofc['CALCur'].apply(lambda x: round(x,0))


nf.to_csv('output.csv')