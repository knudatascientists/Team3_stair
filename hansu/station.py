import pandas as pd
import numpy as np
import pymysql
from settings import *
from userInfo import UserInfo

class Station:
    def __init__(self, use_DB = True):
        if use_DB:
            self.seoul_loc = self.load_DB('seoul_loc')
            self.구분_명_주소 = self.load_DB('구분_명_주소')
            self.년도별_valuecounts = self.load_DB('년도별_valuecounts')
        else:
            self.seoul_loc = self.load_csv('seoul_loc')
            self.구분_명_주소 = self.load_csv('구분_명_주소')
            self.년도별_valuecounts = self.load_csv('년도별_valuecounts')


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

    def load_csv(self, tabelName):
        tabel = pd.read_csv(data_path + tabelName+'.csv')
        return tabel

    # 기능: 두 지점 사이 거리 계산(유클리드)
    # 입력: 위경도1, 위경도2
    # 출력: distance
    def cal_dis(self, loc1, loc2):
        pass

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

    #
    # 기능: 주소상의 구에 포함되는 자료를 필터링
    # 입력: user_add
    # 출력: 없음
    def get_local_data(self, user_add):
        # self.filter_data =
        pass

    def get_local_cars(self):
        pass

