from cProfile import label
from turtle import color
from userInfo import UserInfo
from station import Station
from settings import *
import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np


service = Station()
user = UserInfo.geocoding(default_add)

st.title('Electric Automobile Station')

# st.subheader('현재 위치')
add = st.text_input(label = '현재 위치', value = default_add)
user.set_add(add)
st.text(user.get_user_info())

# st.subheader(f"{user.distict}내의 전기차량 등록수 : {service.get_local_cars()}")


df = service.station_df((float(user.loc['lat']),float(user.loc['lng'])))
df.rename(columns = {'LAT':'lat', 'LNG':'lon'}, inplace = True)
# st.map(df[['lat', 'lon']])

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=float(user.loc['lat']),
        longitude=float(user.loc['lng']),
        zoom=14,

    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=pd.DataFrame({'lat':[float(user.loc['lat'])],'lon':[float(user.loc['lng'])]}),
           get_position='[lon, lat]',
           get_color='[200, 30, 30, 160]',
           radius=100,
           elevation_scale=4,
           elevation_range=[0, 1000],
           pickable=True,
           extruded=True,
        ),       
        pdk.Layer(
            'ScatterplotLayer',
            data=df.loc[[0],['lat', 'lon']],
            get_position='[lon, lat]',
            get_color='[150, 30, 30, 160]',
            get_radius=70,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=df.loc[1:,['lat', 'lon']],
            get_position='[lon, lat]',
            get_color='[30, 30, 150, 160]',
            get_radius=70,
        ),
    ],
))
st_df = st.dataframe(df,width=900,height=300)
