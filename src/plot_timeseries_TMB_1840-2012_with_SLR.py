#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 08:14:38 2021

@author: jeb@geus.dk

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

os.chdir('/Users/jason/Dropbox/TMB_Greenland_1840-2012/')

font_size=16
plt.style.use('default')
# plt.rcParams['font.sans-serif'] = ['Georgia']
plt.rcParams["font.size"] = font_size 
plt.rcParams["mathtext.default"]='regular'

th=1
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 1
plt.rcParams['grid.linewidth'] = th/2.


df=pd.read_csv('./data/Greenland_mass_balance_totals_1840-2012_ver_20141130_with_uncert_via_Kjeldsen_et_al_2015.csv')
print(df.columns)

dfBC=pd.read_csv('./data/Greenland_mass_balance_1840-2011_Box_and_Colgan_2013.txt',delim_whitespace=True)
print(dfBC.columns)

# ---------------------------- cumulate
iyear=1840 ; fyear=2011 ; n_years=fyear-iyear+1

cum=np.zeros((2,n_years))

k=-362.5

temp=0.
for i in range(0,n_years):
	temp+=dfBC.TMB[i]/k
	cum[0,i]=temp
    
temp=0.
for i in range(0,n_years):
	temp+=df.TMB[i]/k
	cum[1,i]=temp
    
fig, ax = plt.subplots(2,1,figsize=(14,11))

cc=0#---------------------------------------------------------------- annual
tit='Greenland land ice total mass balance reconstruction 1840-2012'
ax[0].set_title(tit)

ax[cc].plot(dfBC.Year,dfBC.TMB,c='b',label='Box and Colgan 2013',zorder=10)
ax[cc].plot(df.year,df.TMB,c='r',label='Kjeldsen et al (2015)')
ax[cc].fill_between(df.year, df.TMB-df["TMB 1sigma"], df.TMB+df["TMB 1sigma"],
                 color='r',alpha=0.2,label='Kjeldsen et al (2015) uncertainty')

ax[cc].axhline(y=0,linestyle='--',c='grey')
ax[cc].set_ylabel('Gt y $^{-1}$')

cc+=1#---------------------------------------------------------------- T diff
ax[cc].plot(dfBC.Year[0:n_years],cum[0,:],c='b',label='Box and Colgan 2013',zorder=10)
ax[cc].plot(df.year[0:n_years],cum[1,:],c='r',label='Kjeldsen et al (2015)')
# ax[cc].fill_between(df.year, df.TMB-df["TMB 1sigma"], df.TMB+df["TMB 1sigma"],
#                  color='r',alpha=0.2,label='Kjeldsen et al (2015) uncertainty')

ax[cc].axhline(y=0,linestyle='--',c='grey')
ax[cc].set_ylabel('eustatic sea level, mm')


plt.xlim(1839,2013)
plt.legend(loc=2)


print(f'cumulative SLR Box and Colgan 2013 {"%.1f" % cum[0,n_years-1]}')
print(f'cumulative SLR Kjeldsen et al 2015 {"%.1f" % cum[1,n_years-1]}')

ly='x'

if ly =='x':plt.show()

if ly =='p':
    plt.savefig('./Figs/plot_timeseries_TMB_1840-2012_with_SLR.png', dpi=100, bbox_inches='tight')