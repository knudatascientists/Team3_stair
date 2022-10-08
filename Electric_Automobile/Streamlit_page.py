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
add = st.text_input(label = '현재 위치(서울시 00구 ...)', value = default_add)
try:
    user.set_add(add)
    st.text(user.get_user_info())
except:
    st.text('주소 입력 오류!')

service.make_res_car_df(add, user)
t, gu_res_car_cnt = service.get_gu_info(user)
st.text(t)
st.dataframe(gu_res_car_cnt)

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
           radius=30,
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
            get_radius=25,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=df.loc[1:,['lat', 'lon']],
            get_position='[lon, lat]',
            get_color='[30, 30, 150, 160]',
            get_radius=20,
        ),
    ],
))
st_df = st.dataframe(df,width=900,height=300)
