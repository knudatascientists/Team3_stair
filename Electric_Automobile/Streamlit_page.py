from userInfo import UserInfo
from station import Station
from settings import *
import streamlit as st
import pandas as pd
import numpy as np


service = Station()
user = UserInfo.geocoding(default_add)

st.title('Electric Automobile Station')

st.subheader('현재 위치')
add = st.text_input(label = '', value = default_add)
user.set_add(add)
st.text(user.get_user_info())


df = pd.DataFrame({'lat':float(user.loc['lat']), 'lon':float(user.loc['lng'])})
st.map(df)
st_df = st.dataframe(df,width=300,height=300)

# 변동 적용
# st_df.dataframe(df)
st_df

