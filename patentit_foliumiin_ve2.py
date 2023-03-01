# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 19:57:42 2022

@author: larij
"""

# wgs: 4326
# pseudomercator: 3857

import requests as req 
import pandas as pd
#import json
import folium
#import geopandas as gpd
import numpy as np

# Url, josta data haetaan
url = 'https://api.patentsview.org/patents/query?q={"_and":[{"_gte":{"patent_date":"2020-01-01"}},{"_text_any":{"patent_abstract":"quantum"}},{"cpc_subsection_id":"G06"}]}&f=["assignee_organization","patent_title","assignee_city","assignee_country","assignee_lastknown_latitude","assignee_lastknown_longitude"]&o={"per_page":10000}'

# Alustetaan data json-muotoon ja lyhennetään sitä hieman
data = req.get(url).json()
data2 = data['patents']

# Tehdään dataframe ja poistetaan ne rivit, joissa ei ole sijaintidataa
df = pd.json_normalize(data2, record_path=['assignees'],meta=['patent_title'])
#df = pd.json_normalize(data2)
df['assignee_lastknown_latitude'].replace('', np.nan, inplace=True)
df.dropna(subset=['assignee_lastknown_latitude'], inplace=True)

# Tehdään pohjakartta
m = folium.Map(location=[0.0, 0.0],zoom_start=2,crs='EPSG3857',pointer_events=True)

# Tehdään taso, jolla patentit viedään kartalle, nimi on vähän outo
plantslayer = folium.FeatureGroup("Power Plants").add_to(m)

for itr in range(len(df)):
    latVal = df.iloc[itr]['assignee_lastknown_latitude']
    lngVal = df.iloc[itr]['assignee_lastknown_longitude']
    yritys = df.iloc[itr]['assignee_organization']
    nimi = df.iloc[itr]['patent_title']
    folium.Circle(location=[latVal,lngVal],radius=20,weight=5,fill=False,tooltip=[yritys,nimi]).add_to(plantslayer)
    
# Tehdään tooltip

# Tallennetaan kartta
m.save("/var/www/html/foliumkartta.html")