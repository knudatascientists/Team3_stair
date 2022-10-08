import pandas as pd
import numpy as np
import pymysql
from settings import *
from userInfo import UserInfo
from haversine import haversine

class Station:
    def __init__(self, use_DB = True):
        self.res_car_df = pd.DataFrame()
        self.length = 0
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
    def make_station_df(self,user_loc):

        # 떨어진 거리의 새로운 열 만들기
        for k in [1,3,5]:
            for i in range(len(self.seoul_loc_df)):
                self.seoul_loc_df.loc[i,'distant distance(km)']=haversine(user_loc,(self.seoul_loc_df.iloc[i,1],self.seoul_loc_df.iloc[i,2]))
            result_df=self.seoul_loc_df[self.seoul_loc_df['distant distance(km)']<=k]

            if len(result_df)==0:
                # print(f"주변 {k}km내에 있는 충전소가 없습니다.")
                # print(f"주변 {k+2}km내에 있는 충전소를 찾습니다.")
                pass
            elif len(result_df)==0 and k==5:
                # print(f"주변 {k}km내에 있는 충전소가 없습니다.")
                # print(f"다른곳으로 이동 후 다시 정보를 입력해주세요.")
                return pd.DataFrame(columns = ['station', 'LNG', 'LAT', 'distant', 'distance(km)', 'address', 'speed'])
            else:
                self.length = k
                break
        
        # 주소데이터를 열로 만들기
        result_df=pd.merge(result_df,self.charge_address_df,how='inner')

        # 충전구분 정보를 열로 만들기
        for i in range(len(result_df)):
            if list(self.speed_df.station).count(result_df.station[i])>=2:
                result_df.loc[i,'speed']='완속/급속'
            else:
                result_df.loc[i,'speed']=self.speed_df.loc[i,'speed']
        
        self.result_df=result_df.sort_values('distant distance(km)',ascending=True).reset_index(drop = True)
        self.result_df.rename(columns = {'LAT':'lat', 'LNG':'lon'}, inplace = True)

    # 기능: 가장 가까운 위치의 충전소 위치를 반환
    # 입력: 없음
    # 출력: DataFrame
    def get_closest_st(self):
        closest_st = self.result_df.loc[[0],['lat', 'lon']]
        return closest_st


    # 기능: 서울시 구별 등록차량 정보 필터링
    # 입력: 사용자 위치 정보
    def make_res_car_df(self,address, user):
        gu=address.split(' ')[1]
        if gu != user.gu or len(self.res_car_df)==0:
            self.res_car_df=self.car_register_df.iloc[[self.car_register_df.ind[i]-1 for i in range(len(self.car_register_df)) if self.car_register_df.loc[i,'dong'].split(' ')[1]==gu],]
        self.gu_res_car_cnt = self.get_res_car_cnt()

    # 기능: 서울시 구별 등록차량 개수 (차량 종류별)
    # 입력: 해당 구의 등록정보
    # 출력: 차량 종류별 등록정보
    def get_res_car_cnt(self):
        gu_res_car_cnt=pd.DataFrame(self.res_car_df.groupby('fuel').count()['dong'])
        gu_res_car_cnt=gu_res_car_cnt.T
        gu_res_car_cnt.index=['count']        
        return gu_res_car_cnt


    def get_gu_info(self, user):
        t = f"{user.gu} 내의 전기차량 등록수 : {len(self.res_car_df)} 개"
        return t, self.gu_res_car_cnt

