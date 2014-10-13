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
aof1c = .77
bof1c = .59
dof1c = .45
#Third level calculations (off YOFC)
jc = .5
#Fourth level calculations (off second level calcs)
#YOF9 = YOFC+5
#Fifth level calculations
ue45c = 8
uemnc = 18
#Ninth level calculations
eo8nc = .75
#Sleeper calculations
vac = .85
vbc = .70
vcc = .55
vdc = .40
dac = .87
dbc = .74
dcc = .61
ddc = .48

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

def bizclass(x):
	if((x['DOF1r']*jc)<15):
		return 15
	else:
		return (x['DOF1r']*jc)
		
def errorcheck(x):
	if(x['r'] == x['CALCr']):
		return "Correct"
	else:
		return "Error"
		
def initcheck(x):
	if(x['intcheck'] == "Correct"):
		return "Correct"
	else:
		return "Error"

of['mktfp'] = of.apply(marketfp, axis=1)
nf['mktfp'] = nf.apply(marketfp, axis=1)
of = of.drop(['yn','o','d','rt', 'fp'], axis=1)
nf = nf.drop(['yn'], axis=1)
nf = pd.merge(nf, of, on='mktfp')
nf['mkt'] = nf.apply(market, axis=1)

#Calculate YOFC base increase
yofc = pd.DataFrame()
yofc = nf[(nf.fp == 'YOFC')]
increase = float(raw_input('Enter Y percentage increase: '))
yofc['CALCur'] = yofc['OLDur'].apply(lambda x: x*(1+increase))
yofc['CALCr'] = yofc['CALCur'].apply(lambda x: round(x,0))
yofc['check'] = yofc.apply(errorcheck, axis=1)
yofc['derivedcheck'] = "Nonderived"

#Create duplicate frame for import testing use
yofccalc = pd.DataFrame()
yofccalc = yofc
yofccalc = yofccalc.drop(['eff','dis','OLDur','OLDr','OLDeff','OLDdis','rt','o','d','fp','ur','r','mktfp','derivedcheck'], axis=1)
yofccalc.columns = ['mkt','YOFCur','YOFCr','intcheck']

#Calculate DS base increase
ds = pd.DataFrame()
ds = nf[(nf.fp == 'DS')]
increase = float(raw_input('Enter DS percentage increase: '))
ds['CALCur'] = ds['OLDur'].apply(lambda x: x*(1+increase))
ds['CALCr'] = ds['CALCur'].apply(lambda x: round(x,0))
ds['check'] = ds.apply(errorcheck, axis=1)
ds['derivedcheck'] = "Nonderived"

#Create duplicate DS frame for import testing use
dscalc = pd.DataFrame()
dscalc = ds
dscalc = dscalc.drop(['eff','dis','OLDur','OLDr','OLDeff','OLDdis','rt','o','d','fp','ur','r','mktfp','derivedcheck'], axis=1)
dscalc.columns = ['mkt','DSur','DSr','intcheck']

#Calculate VS base increase
vs = pd.DataFrame()
vs = nf[(nf.fp == 'VS')]
increase = float(raw_input('Enter VS percentage increase: '))
vs['CALCur'] = vs['OLDur'].apply(lambda x: x*(1+increase))
vs['CALCr'] = vs['CALCur'].apply(lambda x: round(x,0))
vs['check'] = vs.apply(errorcheck, axis=1)
vs['derivedcheck'] = "Nonderived"

#Create duplicate VS frame for import testing use
vscalc = pd.DataFrame()
vscalc = vs
vscalc = vscalc.drop(['eff','dis','OLDur','OLDr','OLDeff','OLDdis','rt','o','d','fp','ur','r','mktfp','derivedcheck'], axis=1)
vscalc.columns = ['mkt','VSur','VSr','intcheck']

#Calculate VA
va = pd.DataFrame()
va = nf[(nf.fp == 'VA')]
va = pd.merge(va, vscalc, on='mkt')
va['CALCur'] = va['VSr'].apply(lambda x: x*(vac))
va['CALCr'] = va['CALCur'].apply(lambda x: round(x,0))
va['derivedcheck'] = va.apply(initcheck, axis=1)
va = va.drop(['VSur', 'VSr','intcheck'], axis=1)
va['check'] = va.apply(errorcheck, axis=1)

#Calculate VB
vb = pd.DataFrame()
vb = nf[(nf.fp == 'VB')]
vb = pd.merge(vb, vscalc, on='mkt')
vb['CALCur'] = vb['VSr'].apply(lambda x: x*(vbc))
vb['CALCr'] = vb['CALCur'].apply(lambda x: round(x,0))
vb['derivedcheck'] = vb.apply(initcheck, axis=1)
vb = vb.drop(['VSur', 'VSr','intcheck'], axis=1)
vb['check'] = vb.apply(errorcheck, axis=1)

#Calculate VC
vc = pd.DataFrame()
vc = nf[(nf.fp == 'VC')]
vc = pd.merge(vc, vscalc, on='mkt')
vc['CALCur'] = vc['VSr'].apply(lambda x: x*(vcc))
vc['CALCr'] = vc['CALCur'].apply(lambda x: round(x,0))
vc['derivedcheck'] = vc.apply(initcheck, axis=1)
vc = vc.drop(['VSur', 'VSr','intcheck'], axis=1)
vc['check'] = vc.apply(errorcheck, axis=1)

#Calculate VD
vd = pd.DataFrame()
vd = nf[(nf.fp == 'VD')]
vd = pd.merge(vd, vscalc, on='mkt')
vd['CALCur'] = vd['VSr'].apply(lambda x: x*(vdc))
vd['CALCr'] = vd['CALCur'].apply(lambda x: round(x,0))
vd['derivedcheck'] = vd.apply(initcheck, axis=1)
vd = vd.drop(['VSur', 'VSr','intcheck'], axis=1)
vd['check'] = vd.apply(errorcheck, axis=1)

#Calculate DA
da = pd.DataFrame()
da = nf[(nf.fp == 'DA')]
da = pd.merge(da, dscalc, on='mkt')
da['CALCur'] = da['DSr'].apply(lambda x: x*(dac))
da['CALCr'] = da['CALCur'].apply(lambda x: round(x,0))
da['derivedcheck'] = da.apply(initcheck, axis=1)
da = da.drop(['DSur', 'DSr','intcheck'], axis=1)
da['check'] = da.apply(errorcheck, axis=1)

#Calculate DB
db = pd.DataFrame()
db = nf[(nf.fp == 'DB')]
db = pd.merge(db, dscalc, on='mkt')
db['CALCur'] = db['DSr'].apply(lambda x: x*(dbc))
db['CALCr'] = db['CALCur'].apply(lambda x: round(x,0))
db['derivedcheck'] = db.apply(initcheck, axis=1)
db = db.drop(['DSur', 'DSr','intcheck'], axis=1)
db['check'] = db.apply(errorcheck, axis=1)

#Calculate DC
dc = pd.DataFrame()
dc = nf[(nf.fp == 'DC')]
dc = pd.merge(dc, dscalc, on='mkt')
dc['CALCur'] = dc['DSr'].apply(lambda x: x*(dcc))
dc['CALCr'] = dc['CALCur'].apply(lambda x: round(x,0))
dc['derivedcheck'] = dc.apply(initcheck, axis=1)
dc = dc.drop(['DSur', 'DSr','intcheck'], axis=1)
dc['check'] = dc.apply(errorcheck, axis=1)

#Calculate DD
dd = pd.DataFrame()
dd = nf[(nf.fp == 'DD')]
dd = pd.merge(dd, dscalc, on='mkt')
dd['CALCur'] = dd['DSr'].apply(lambda x: x*(ddc))
dd['CALCr'] = dd['CALCur'].apply(lambda x: round(x,0))
dd['derivedcheck'] = dd.apply(initcheck, axis=1)
dd = dd.drop(['DSur', 'DSr','intcheck'], axis=1)
dd['check'] = dd.apply(errorcheck, axis=1)

#Calculate AOF1
aof1 = pd.DataFrame()
aof1 = nf[(nf.fp == 'AOF1')]
aof1 = pd.merge(aof1, yofccalc, on='mkt')
aof1['CALCur'] = aof1['YOFCr'].apply(lambda x: x*(aof1c))
aof1['CALCr'] = aof1['CALCur'].apply(lambda x: round(x,0))
aof1['derivedcheck'] = aof1.apply(initcheck, axis=1)
aof1 = aof1.drop(['YOFCur', 'YOFCr', 'intcheck'], axis=1)
aof1['check'] = aof1.apply(errorcheck, axis=1)

#Calculate BOF1
bof1 = pd.DataFrame()
bof1 = nf[(nf.fp == 'BOF1')]
bof1 = pd.merge(bof1, yofccalc, on='mkt')
bof1['CALCur'] = bof1['YOFCr'].apply(lambda x: x*(bof1c))
bof1['CALCr'] = bof1['CALCur'].apply(lambda x: round(x,0))
bof1['derivedcheck'] = bof1.apply(initcheck, axis=1)
bof1 = bof1.drop(['YOFCur', 'YOFCr', 'intcheck'], axis=1)
bof1['check'] = bof1.apply(errorcheck, axis=1)

#Calculate DOF1
dof1 = pd.DataFrame()
dof1 = nf[(nf.fp == 'DOF1')]
dof1 = pd.merge(dof1, yofccalc, on='mkt')
dof1['CALCur'] = dof1['YOFCr'].apply(lambda x: x*(dof1c))
dof1['CALCr'] = dof1['CALCur'].apply(lambda x: round(x,0))
dof1['derivedcheck'] = dof1.apply(initcheck, axis=1)
dof1 = dof1.drop(['YOFCur', 'YOFCr', 'intcheck'], axis=1)
dof1['check'] = dof1.apply(errorcheck, axis=1)

#Create duplicate frame for import testing use
aof1calc = pd.DataFrame()
aof1calc = aof1
aof1calc = aof1calc.drop(['eff','dis','OLDur','OLDr','OLDeff','OLDdis','rt','o','d','fp','ur','r','mktfp','check'], axis=1)
aof1calc.columns = ['mkt','AOF1ur','AOF1r','intcheck']
#Create duplicate frame for import testing use
bof1calc = pd.DataFrame()
bof1calc = bof1
bof1calc = bof1calc.drop(['eff','dis','OLDur','OLDr','OLDeff','OLDdis','rt','o','d','fp','ur','r','mktfp','check'], axis=1)
bof1calc.columns = ['mkt','BOF1ur','BOF1r','intcheck']
#Create duplicate frame for import testing use
dof1calc = pd.DataFrame()
dof1calc = dof1
dof1calc = dof1calc.drop(['eff','dis','OLDur','OLDr','OLDeff','OLDdis','rt','o','d','fp','ur','r','mktfp','check'], axis=1)
dof1calc.columns = ['mkt','DOF1ur','DOF1r','intcheck']
'''
#Calculate J (off of Y)
j = pd.DataFrame()
j = nf[(nf.fp == 'J')]
j = pd.merge(j,yofccalc, on='mkt')
j['CALCur'] = j['YOFCr'].apply(lambda x: x*(jc))
j['CALCr'] = j['CALCur'].apply(lambda x: round(x,0))
j = j.drop(['YOFCur', 'YOFCr'], axis=1)
j['check'] = j.apply(errorcheck, axis=1)

#Calculate YOF9
yof9 = pd.DataFrame()
yof9 = nf[(nf.fp == 'YOF9')]
yof9 = pd.merge(yof9,yofccalc, on='mkt')
yof9['CALCur'] = yof9['YOFCr'].apply(lambda x: x + 5)
yof9['CALCr'] = yof9['CALCur'].apply(lambda x: round(x,0))
yof9 = yof9.drop(['YOFCur', 'YOFCr'], axis=1)
yof9['check'] = yof9.apply(errorcheck, axis=1)

#Calculate AOF9
aof9 = pd.DataFrame()
aof9 = nf[(nf.fp == 'AOF9')]
aof9 = pd.merge(aof9,aof1calc, on='mkt')
aof9['CALCur'] = aof9['AOF1r'].apply(lambda x: x + 5)
aof9['CALCr'] = aof9['CALCur'].apply(lambda x: round(x,0))
aof9 = aof9.drop(['AOF1ur', 'AOF1r'], axis=1)
aof9['check'] = aof9.apply(errorcheck, axis=1)

#Calculate BOF9
bof9 = pd.DataFrame()
bof9 = nf[(nf.fp == 'BOF9')]
bof9 = pd.merge(bof9,bof1calc, on='mkt')
bof9['CALCur'] = bof9['BOF1r'].apply(lambda x: x + 5)
bof9['CALCr'] = bof9['CALCur'].apply(lambda x: round(x,0))
bof9 = bof9.drop(['BOF1ur', 'BOF1r'], axis=1)
bof9['check'] = bof9.apply(errorcheck, axis=1)

#Calculate DOF9
dof9 = pd.DataFrame()
dof9 = nf[(nf.fp == 'DOF9')]
dof9 = pd.merge(dof9,dof1calc, on='mkt')
dof9['CALCur'] = dof9['DOF1r'].apply(lambda x: x + 5)
dof9['CALCr'] = dof9['CALCur'].apply(lambda x: round(x,0))
dof9 = dof9.drop(['DOF1ur', 'DOF1r'], axis=1)
dof9['check'] = dof9.apply(errorcheck, axis=1)
'''

#Calculate J
j = pd.DataFrame()
j = nf[(nf.fp == 'J')]
j = pd.merge(j,dof1calc, on='mkt')
j['CALCur'] = j.apply(bizclass, axis=1)
j['CALCr'] = j['CALCur'].apply(lambda x: round(x,0))
j['derivedcheck'] = j.apply(initcheck, axis=1)
j = j.drop(['DOF1ur', 'DOF1r','intcheck'], axis=1)
j['check'] = j.apply(errorcheck, axis=1)
'''
#Calculate UE45
ue45 = pd.DataFrame()
ue45 = nf[(nf.fp == 'UE45')]
ue45 = pd.merge(ue45,bof1calc, on='mkt')
ue45['CALCur'] = ue45['BOF1r'].apply(lambda x: x * ue45c)
ue45['CALCr'] = ue45['CALCur'].apply(lambda x: round(x,0))
ue45 = ue45.drop(['BOF1ur', 'BOF1r'], axis=1)
ue45['check'] = ue45.apply(errorcheck, axis=1)

#Calculate UEMN
uemn = pd.DataFrame()
uemn = nf[(nf.fp == 'UEMN')]
uemn = pd.merge(uemn,bof1calc, on='mkt')
uemn['CALCur'] = uemn['BOF1r'].apply(lambda x: x * uemnc)
uemn['CALCr'] = uemn['CALCur'].apply(lambda x: round(x,0))
uemn = uemn.drop(['BOF1ur', 'BOF1r'], axis=1)
uemn['check'] = uemn.apply(errorcheck, axis=1)

#Calculate EO8N
eo8n = pd.DataFrame()
eo8n = nf[(nf.fp == 'EO8N')]
eo8n = pd.merge(eo8n,dof1calc, on='mkt')
eo8n['CALCur'] = eo8n['DOF1r'].apply(lambda x: x * eo8nc)
eo8n['CALCr'] = eo8n['CALCur'].apply(lambda x: round(x,0))
eo8n = eo8n.drop(['DOF1ur', 'DOF1r'], axis=1)
eo8n['check'] = eo8n.apply(errorcheck, axis=1)
'''

#Calculate OBOF
obof = pd.DataFrame()
obof = nf[(nf.fp == 'OBOF')]
obof = pd.merge(obof,yofccalc, on='mkt')
obof['CALCur'] = obof['YOFCr'].apply(lambda x: x * 1.5)
obof['CALCr'] = obof['CALCur'].apply(lambda x: round(x,0))
obof['derivedcheck'] = obof.apply(initcheck, axis=1)
obof = obof.drop(['YOFCur', 'YOFCr','intcheck'], axis=1)
obof['check'] = obof.apply(errorcheck, axis=1)

#Calculate OBBF
obbf = pd.DataFrame()
obbf = nf[(nf.fp == 'OBBF')]
obbf = pd.merge(obbf,yofccalc, on='mkt')
obbf['CALCur'] = obbf['YOFCr'].apply(lambda x: x)
obbf['CALCr'] = obbf['CALCur'].apply(lambda x: round(x,0))
obbf['derivedcheck'] = obbf.apply(initcheck, axis=1)
obbf = obbf.drop(['YOFCur', 'YOFCr','intcheck'], axis=1)
obbf['check'] = obbf.apply(errorcheck, axis=1)

#Calculate OBBS
obbs = pd.DataFrame()
obbs = nf[(nf.fp == 'OBBS')]
obbs = pd.merge(obbs,j, on=['mkt','rt','o','d'])
obbs['CALCur'] = obbs['CALCr']
obbs['CALCr'] = obbs['CALCur'].apply(lambda x: round(x,0))
obbs['derivedcheck'] = obbs['check']
obbs = obbs.drop(['fp_y', 'ur_y','r_y','eff_y','dis_y','mktfp_y','OLDur_y','OLDr_y','OLDeff_y','OLDdis_y','check'], axis=1)
obbs.columns = ['rt','o','d','fp','ur','r','eff','dis','mktfp','OLDur','OLDr','OLDeff','OLDdis','mkt','CALCur','CALCr','derivedcheck']
obbs['check'] = obbs.apply(errorcheck, axis=1)

#Combine all fareplans into one DataFrame and export to .csv
output = pd.DataFrame()
output = pd.concat([yofc, aof1, bof1, dof1, j, obof, obbf, obbs, vs, va, vb, vc, vd, ds, da, db, dc, dd], ignore_index=True)
#yof9, aof9, bof9, dof9, ue45, uemn, eo8n
output = output.drop(['eff','dis','OLDeff','OLDdis'], axis=1)
output = output[['rt','mktfp','mkt','o','d','fp','ur','r','OLDur','OLDr','CALCur','CALCr','check','derivedcheck']]

output.to_csv('output.csv')
print output[output['check'] == "Error"].count