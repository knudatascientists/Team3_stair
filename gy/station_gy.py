import pandas as pd
import numpy as np
import pymysql
from settings import *
from userInfo_gy import UserInfo
from haversine import haversine

# SQL 연결 클래스
class Station_gy:
    # 그냥 파일로 csv파일을 객체로 만드는 함수
    # 저희가 쓰는 파일은 5개인데 csv파일로 되어 있는 것들이 없으므로 굳이 필요 없음
    def __init__(self, use_DB = True):
        if use_DB:
            # self.seoul_loc = self.load_DB('seoul_loc')
            pass
        else:
            self.car_register_df=self.load_DB('car_register')
            self.count_df=self.load_DB('count')
            self.charge_address_df=self.load_DB('charge_address')
            self.seoul_loc_df=self.load_DB('seoul_loc')
            self.speed_df=self.load_DB('speed')

    # SQL에서 tabelName을 입력하면 바로 파이썬으로 불러올수 있음
    def load_DB(self, tabelName):
        conn = pymysql.connect(host=host_IP, user =user_ID, password =password, db =db_name, charset =charset)
        cur = conn.cursor()
        sql = f"SELECT * FROM {tabelName}"
        cur.execute(sql)
        rows = cur.fetchall()
        tabel = pd.DataFrame(rows, columns = [t[0] for t in cur.description])
        cur.close()
        conn.close()
        return tabel

    # SQL에 저장된 테이블의 전체를 볼 수 있음
    def get_tabel_names(self):
        conn = pymysql.connect(host=host_IP, user =user_ID, password =password, db =db_name, charset =charset)
        cur = conn.cursor()
        cur.execute(f'SHOW TABLES IN {db_name}')
        rows = cur.fetchall()
        tableList = [tb[0] for tb in rows]
        cur.close()
        conn.close()
        return tableList

    # 객체로 만든 csv파일의 이름을 폴더에서 바로 불러오는 함수
    def load_csv(self, tabelName):
        tabel = pd.read_csv(data_path + tabelName+'.csv')
        return tabel

    # 기능: 두 지점 사이 거리 계산(유클리드)
    # 입력: 위경도1, 위경도2
    # 출력: 떨어진 거리(km)
    def cal_dis(self, loc1, loc2):
        self.loc1=loc1
        self.loc2=loc2

        return haversine(self.loc1,self.loc2) # 위경도 데이터를 km거리로 반환
    
    # 기능: 거리에 따른
    # 입력: 유저위치정보
    # 출력: 충전소 정보 데이터 프레임
    def station_df(self,user_loc):
        # 떨어진 거리의 새로운 열 만들기
        for k in [3,5,7]:
            for i in range(len(self.seoul_loc_df)):
                self.seoul_loc_df.loc[i,'distant distance(km)']=self.cal_dis(user_loc,(self.seoul_loc_df.iloc[i,1],self.seoul_loc_df.iloc[i,2]))
            result_df=self.seoul_loc_df[self.seoul_loc_df['distant distance(km)']<=k]

            if len(result_df)==0:
                print(f"주변 {k}km내에 있는 충전소가 없습니다.")
                print(f"주변 {k+2}km내에 있는 충전소를 찾습니다.")
            elif len(result_df)==0 and k==7:
                print(f"주변 {k}km내에 있는 충전소가 없습니다.")
                print(f"다른곳으로 이동 후 다시 정보를 입력해주세요.")
            else:
                break


        # if len(result_df)==0:
        #     print(f"주변 5km내에 있는 충전소가 없습니다.")
        #     for i in range(len(self.seoul_loc_df)):
        #         self.seoul_loc_df.loc[i,'distant distance(km)']=self.cal_dis(user_loc,(self.seoul_loc_df.iloc[i,1],self.seoul_loc_df.iloc[i,2]))
        #     result_df=self.seoul_loc_df[self.seoul_loc_df['distant distance(km)']<=5.0]
        # else:
        #     print(f"주변 3km내에 있는 충전소를 보여줍니다.")

        # if len(result_df)==0:
        #     print(f"주변 5km내에 있는 충전소가 없습니다.")
        #     for i in range(len(self.seoul_loc_df)):
        #         self.seoul_loc_df.loc[i,'distant distance(km)']=self.cal_dis(user_loc,(self.seoul_loc_df.iloc[i,1],self.seoul_loc_df.iloc[i,2]))
        #     result_df=self.seoul_loc_df[self.seoul_loc_df['distant distance(km)']<=7.0]
        # else:
        #     print(f"주변 3km내에 있는 충전소를 보여줍니다.")
        
        # if len(result_df)==0:
        #     print(f"주변 7km내에 있는 충전소를 보여줍니다.")
        
        # 주소데이터를 열로 만들기
        result_df=pd.merge(result_df,self.charge_address_df,how='inner')

        # 충전구분 정보를 열로 만들기
        for i in range(len(result_df)):
            if list(self.speed_df.station).count(result_df.station[i])>=2:
                result_df.loc[i,'speed']='완속/급속'
            else:
                result_df.loc[i,'speed']=self.speed_df.loc[i,'speed']
        
        result_df=result_df.sort_values('distant distance(km)',ascending=False)
        return result_df

    # 기능: 사용자 위치에서 각 충전소까지 거리 데이터에 추가
    # 입력: user_loc
    # 출력: 없음
    def get_station_dis(self, user_loc):
        pass

    # 기능: 계산된 거리중 가장 가까운 충전소의 정보를 반환
    # 입력: 없음
    # 출력: station_name, station_add, station_loc
    def find_close_station(self):
        pass

    # 기능: 계산된 거리중 범위 내의 충전소들 정보를 반환
    # 입력: length
    # 출력: DataFrame(station_name, station_add, station_loc)
    def find_near_stations(self, length):
        pass

    # 기능: 주소상의 구에 포함되는 자료를 필터링
    # 입력: user_add
    # 출력: 없음
    def get_local_data(self, user_add):
        # self.filter_data =
        pass

    def get_local_cars(self):
        pass