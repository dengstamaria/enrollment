# -*- coding: utf-8 -*-
"""
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
df_schoolz = pd.read_csv('Masterlist of Schools Elementary.csv')

#rename column names
df_raw.columns =  ['Region','Division','Class','2012','2011','2010','2009','2008','2007','2006','2005']

#create another df to show divisions per region
df_mod = df_raw.query('Region != Division & Class == "Total"')
df_mod[['Region','Division']] =  df_mod[['Region','Division']].replace("Subtotal",'',regex=True) #removed the Subtotal string from the columns

df_mod = df_mod[df_mod['Region'] != "National Grand total"] # remove the grand total row

#df_schoolz contains the region: NIR (Negros Island Region). This will be merged with Region VI to be compatible with the original dataset (df_raw).
#df_schoolList will represent 1 school per region.
df_schoolList = df_schoolz['region'].replace("NIR","Region VI",regex=True)
df_schoolList = pd.DataFrame(df_schoolList.value_counts()).reset_index()
df_schoolList.columns = ['Region','Num_of_Schools']

#insert the lat,long column to df_mod via merge
df_modLatLong = pd.merge(df_mod,df_LatLong,how='left')

#insert 'Num_of_Schools' to df_modLatLong
df_mod2 = pd.merge(df_modLatLong,df_schoolList,how='left')

#add Island information
island_dict = {
        'NCR':'Luzon',
        'CAR':'Luzon',
        'Region I':'Luzon',
        'Region II':'Luzon',
        'Region III':'Luzon',
        'Region IV-A':'Luzon',
        'Region IV-B':'Luzon',
        'Region V':'Luzon',
        'Region VI':'Visayas',
        'Region VII':'Visayas',
        'Region VIII':'Visayas',
        'Region IX':'Mindanao',
        'Region X':'Mindanao',
        'Region XII':'Mindanao',
        'Region XI':'Mindanao',
        'ARMM':'Mindanao',
        'CARAGA':'Mindanao',         

}

def islandfunc(region):
    return island_dict[region]

df_mod2['Island']= df_mod2['Region'].apply(islandfunc)


#reshape the dataset for visualization
df_mod3 = (df_mod2[['Region','Division','Island','Num_of_Schools','lat_lng','2005','2006','2007','2008','2009','2010','2011','2012']]).set_index(['Region','Division','lat_lng','Island','Num_of_Schools'])

df_mod3 = df_mod3.stack()

df_mod3 = pd.DataFrame(df_mod3)

df_mod3.columns = ['Number']

df_mod3.index.names = ['Region','Division','lat_lng','Island','Num_of_Schools','Year']

df_mod3.to_csv('dataset.csv')


