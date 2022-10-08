import pandas as pd
import numpy as np
import pymysql
from settings import *
from userInfo import UserInfo
from haversine import haversine

class Station:
    def __init__(self, use_DB = True):
        if use_DB:
            self.car_register_df=self.load_DB('car_register')
            self.count_df=self.load_DB('count')
            self.charge_address_df=self.load_DB('charge_address')
            self.seoul_loc_df=self.load_DB('seoul_loc')
            self.speed_df=self.load_DB('speed')
            


    def load_DB(self, tableName):
        conn = pymysql.connect(host=host_IP, user =user_ID, password =password, db =db_name, charset =charset)
        cur = conn.cursor()
        sql = f"SELECT * FROM {tableName}"
        cur.execute(sql)
        rows = cur.fetchall()
        table = pd.DataFrame(rows, columns = [t[0] for t in cur.description])
        cur.close()
        conn.close()
        return table

    def get_table_names(self):
        conn = pymysql.connect(host=host_IP, user =user_ID, password =password, db =db_name, charset =charset)
        cur = conn.cursor()
        cur.execute(f'SHOW TABLES IN {db_name}')
        rows = cur.fetchall()
        tableList = [tb[0] for tb in rows]
        cur.close()
        conn.close()
        return tableList

    def load_csv(self, tableName):
        table = pd.read_csv(data_path + tableName+'.csv')
        return table


    # SQL에 저장된 테이블의 전체를 볼 수 있음

# 기능: 거리에 따른
    # 입력: 유저위치정보
    # 출력: 충전소 정보 데이터 프레임
    def station_df(self,user_loc):
        # 떨어진 거리의 새로운 열 만들기
        for k in [1,3,5]:
            for i in range(len(self.seoul_loc_df)):
                self.seoul_loc_df.loc[i,'distant distance(km)']=haversine(user_loc,(self.seoul_loc_df.iloc[i,1],self.seoul_loc_df.iloc[i,2]))
            result_df=self.seoul_loc_df[self.seoul_loc_df['distant distance(km)']<=k]

            if len(result_df)==0:
                # print(f"주변 {k}km내에 있는 충전소가 없습니다.")
                # print(f"주변 {k+2}km내에 있는 충전소를 찾습니다.")
                pass
            elif len(result_df)==0 and k==7:
                # print(f"주변 {k}km내에 있는 충전소가 없습니다.")
                # print(f"다른곳으로 이동 후 다시 정보를 입력해주세요.")
                pass
            else:
                return pd.DataFrame(columns = ['station', 'LNG', 'LAT', 'distant', 'distance(km)', 'address', 'speed'])
        
        # 주소데이터를 열로 만들기
        result_df=pd.merge(result_df,self.charge_address_df,how='inner')

        # 충전구분 정보를 열로 만들기
        for i in range(len(result_df)):
            if list(self.speed_df.station).count(result_df.station[i])>=2:
                result_df.loc[i,'speed']='완속/급속'
            else:
                result_df.loc[i,'speed']=self.speed_df.loc[i,'speed']
        
        result_df=result_df.sort_values('distant distance(km)',ascending=True).reset_index(drop = True)
        return result_df




    # 기능: 주소상의 구에 포함되는 자료를 필터링
    # 입력: user_add
    # 출력: 없음
    def get_local_data(self, user_add):
        # self.filter_data =
        pass

    # 기능: 필터링 된 자료에서 등록정보, 충전소 정보 반환
    # 입력: 없음
    # 출력: 차량 등록정보, DataFrame(station_name, station_add, station_loc)
    def get_local_cars(self):
        pass

