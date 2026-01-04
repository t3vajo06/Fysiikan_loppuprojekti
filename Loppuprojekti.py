import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt
from scipy.signal import butter, filtfilt
import folium
from streamlit_folium import st_folium

#Tämä ajetaan streamlit run-komennolla
url = "https://raw.githubusercontent.com/t3vajo06/Fysiikan_loppuprojekti/refs/heads/main/Loppuprojekti.py"

accelerometer_url = "https://raw.githubusercontent.com/t3vajo06/Fysiikan_loppuprojekti/refs/heads/main/Accelerometer.csv"
location_url = "https://raw.githubusercontent.com/t3vajo06/Fysiikan_loppuprojekti/refs/heads/main/Location.csv"

df_acc = pd.read_csv(accelerometer_url)
df_location = pd.read_csv(location_url)
st.title('Fysiikan loppuprojekti')

def butter_lowpass_filter(data, cutoff, nyq, order):
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

data = df_acc['Linear Acceleration y (m/s^2)']
T_tot = df_acc['Time (s)'].max() #Datan kokonaispituus
n = len(df_acc['Time (s)']) #Datapisteet
fs = n/T_tot #Näytteenottotaajuus
nyq = fs/2 #Nyqvistin taajuus eli suurin taajuus joka havaittavissa datasta
order = 3 #Ominaisuus suodattimelle
cutoff = 1/0.4 #Cutoff taajuus, jota suuremmat taajuudet alipäästösuodatin poistaa

data_filt = butter_lowpass_filter(data, cutoff, nyq, order)

#Askelten laskeminen nollatason ylityksillä
jaksot = 0
for i in range(n-1):
    if data_filt[i]/data_filt[i+1] < 0:
        jaksot += 0.5

st.write("Askelmäärä laskettuna suodatuksen avulla:", int(jaksot))

#Tulostetaan keskinopeus
st.write("Keskinopeus:", round(df_location['Velocity (m/s)'].mean(), 1),'m/s' )

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2]) 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 
    return c * r

#Lasketaan kuljettu matka
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
lat1 = df_location['Latitude (°)'].mean()
long1 = df_location['Longitude (°)'].mean()

#Kartan luonti
my_map = folium.Map(location = [lat1,long1], zoom_start=15)

#Kuljettu reitti kartalla:
st.title('Karttakuva')
folium.PolyLine(df_location[['Latitude (°)','Longitude (°)']], color = 'blue', weight = 3).add_to(my_map)
st_map = st_folium(my_map, width = 900, height=650)