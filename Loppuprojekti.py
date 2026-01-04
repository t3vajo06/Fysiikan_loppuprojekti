import streamlit as st
import pandas as pd

Location_url = ""


df_acc = pd.read_csv("Accelerometer.csv")
df_location = pd.read_csv("Location.csv")
st.title('Fysiikan loppuprojekti')

#Tulostetaan keskinopeus
st.write("Keskinopeus:", round(df_location['Velocity (m/s)'].mean(), 1),'m/s' )

from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2]) 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 
    return c * r

#Lasketaan kuljettu matka
import numpy as np
df_location['Distance_calc'] = np.zeros(len(df_location))

#Lasketaan väimatka havaintopisteiden välillä
for i in range(len(df_location)-1):
    lon1 = df_location['Longitude (°)'][i]
    lon2 = df_location['Longitude (°)'][i+1]
    lat1 = df_location['Latitude (°)'][i]
    lat2 = df_location['Latitude (°)'][i+1]
    df_location.loc[i+1,'Distance_calc'] = haversine(lon1, lat1, lon2, lat2)

total_distance = df_location["Distance_calc"].sum()
#Tulostetaan kokonaismatka
st.write("Kokonaismatka:", round(total_distance, 2), "km")






#Kartta
import folium
from streamlit_folium import st_folium
lat1 = df_location['Latitude (°)'].mean()
long1 = df_location['Longitude (°)'].mean()

#Kartan luonti
my_map = folium.Map(location = [lat1,long1], zoom_start=15)

#Kuljettu reitti kartalla:
st.title('Karttakuva')
folium.PolyLine(df_location[['Latitude (°)','Longitude (°)']], color = 'blue', weight = 3).add_to(my_map)
st_map = st_folium(my_map, width = 900, height=650)