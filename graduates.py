# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 17:39:11 2018

@author: 10009174
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter 

df_raw = pd.read_csv('data.csv')

#cleaning up the dataset

#renaming columns
df_raw.columns =  ['Region','Division','Class','2012','2011','2010','2009','2008','2007','2006','2005']

#every region has a subtotal row in the dataset. This is done to remove those subtotals.
df_mod = df_raw[df_raw['Region'] != df_raw['Division']].dropna()

#all gender dataset
df_total = df_mod[df_mod['Class'] == 'Total'] #choose all rows with Class = Total
df_total = df_total[['Region','Division','2005','2006','2007','2008','2009','2010','2011','2012']]


#all male dataset
df_male = df_mod[df_mod['Class'] == 'Male'] #choole all rows with Class = Male
df_male = df_male[['Region','Division','2005','2006','2007','2008','2009','2010','2011','2012']]

#all female dataset
df_female = df_mod[df_mod['Class'] == 'Female'] #choole all rows with Class = Female
df_female = df_female[['Region','Division','2005','2006','2007','2008','2009','2010','2011','2012']]


#summarized datasets
female_enrolees = df_female.groupby(['Region','Division']).sum()
male_enrolees = df_male.groupby(['Region','Division']).sum()
total_enrolees = df_total.groupby(['Region']).sum()

#df transform
total_summary = total_enrolees.T
total_summary['total'] = total_summary.sum(axis=1)

#plot the total_summary
fig, ax = plt.subplots()
#fig = plt.figure()  # an empty figure with no axes

plt.plot(total_summary['total'])

plt.ylim(ymin=0)
plt.ylim(ymax=15000000)
#plt.xlabel('Year')
plt.ylabel('number of enrolees')
plt.yticks(np.arange(0, 15000000, step=1000000))
#plt.yticks([]) #hide yticks

#change yticks to 1M, 2M etc

ax.bar(total_summary.index,total_summary['total'])
# Remove the plot frame lines. 
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)


