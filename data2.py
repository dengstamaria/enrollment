# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 15:09:27 2019

@author: 10009174
Oblective is to clean the data use Google Data Studio for visualization

data set notes:
- Each region has a subtotal row added
- National Grand total is the sum of all totals

Cities were manually renamed from:
Pangasinan I, Lingayen
Pangasinan II, Binalonan
City of Naga, Cebu

to:
Lingayen
Binalonan
City of Naga

this is to avoid errors on concat for geo map
"""
import pandas as pd

#read data
df_raw = pd.read_csv('data.csv')
df_LatLong = pd.read_csv('ph.csv')

#rename column names
df_raw.columns =  ['Region','Division','Class','2012','2011','2010','2009','2008','2007','2006','2005']

#create another df to show divisions per region
df_mod = df_raw.query('Region != Division & Class == "Total"')
df_mod[['Region','Division']] =  df_mod[['Region','Division']].replace("Subtotal",'',regex=True) #removed the Subtotal string from the columns

df_mod = df_mod[df_mod['Region'] != "National Grand total"] # remove the grand total row

#insert the lat,long column to df_mod via merge
df_modLatLong = pd.merge(df_mod,df_LatLong,how='left')

#reshape the dataset for visualization
df_mod2 = (df_modLatLong[['Region','Division','lat_lng','2005','2006','2007','2008','2009','2010','2011','2012']]).set_index(['Region','Division','lat_lng'])


df_mod2 = df_mod2.stack()
df_mod2 = pd.DataFrame(df_mod2)
df_mod2.columns = ['Number']
df_mod2.index.names = ['Region','Division','lat_lng','Year']
df_mod2.to_csv('dataset.csv')


