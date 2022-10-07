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

st.subheader('현재 위치')
add = st.text_input(label = '', value = default_add)
user.set_add(add)
st.text(user.get_user_info())

# st.subheader(f"{user.distict}내의 전기차량 등록수 : {service.get_local_cars()}")

# df = service.find_near_stations(bound_length)
# df = pd.DataFrame({'lat':[float(user.loc['lat'])], 'lon':[float(user.loc['lng'])]})
df = service.load_DB('seoul_loc')
df.rename(columns = {'LAT':'lat', 'LNG':'lon'}, inplace = True)

st.map(df[['lat','lon']])
st_df = st.dataframe(df,width=300,height=300)

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=float(user.loc['lat']),
        longitude=float(user.loc['lng']),
        zoom=15,
        # pitch=50,
    ),
    layers=[
        pdk.Layer(
           'closest',
           data=df.iloc[[0],:],
           get_position='[lon, lat]',
           get_color='[150, 30, 30, 160]',
           radius=70,
        #    elevation_scale=4,
        #    elevation_range=[0, 1000],
        #    pickable=True,
        #    extruded=True,
        ),
        pdk.Layer(
            'all',
            data=df,
            get_position='[lon, lat]',
            get_color='[30, 30, 150, 160]',
            get_radius=70,
        ),
    ],
))
