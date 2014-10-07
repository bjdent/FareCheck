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

#yofc = pd.DataFrame()
#def makeDF(x):
#	if(x['fp']=="YOFC"):
#		yofc.append(x)
		
#yofc = nf.apply(makeDF, axis=1)
#print yofc.info()

increase = float(raw_input('Enter percentage increase: '))
nf['CALCur'] = nf['OLDur'].apply(lambda x: x*(1+increase))
nf['CALCr'] = nf['CALCur'].apply(lambda x: round(x,0))
#print of.info()
nf.to_csv('output.csv')