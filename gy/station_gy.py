import pandas as pd
import pymysql
from settings import *
from haversine import haversine

# SQL 연결 클래스
class Station_gy:
    # 생성자
    # 객체를 만들면 객체 안에는 sql에서 불러온 DB들이 저장되어 있다. 
    def __init__(self, use_DB = True):
        if use_DB:
            self.car_register_df=self.load_DB('car_register')
            self.count_df=self.load_DB('count')
            self.charge_address_df=self.load_DB('charge_address')
            self.seoul_loc_df=self.load_DB('seoul_loc')
            self.speed_df=self.load_DB('speed')

    # DB에 있는 데이터 불러오기 함수
    # SQL에 있는 tableName을 입력하면 바로 파이썬으로 불러올수 있음
    def load_DB(self, tableName):
        conn = pymysql.connect(host=host_IP, user=user_ID, password=password, db=db_name, charset=charset) # mysql과 연결
        cur = conn.cursor() # Cursor객체를 가기고 옴
        sql = f"SELECT * FROM {tableName}"
        cur.execute(sql) # sql문장을 DB서버에 전송
        rows = cur.fetchall() # 서버로부터 가져온 데이터를 코드에서 활용 => fetchall(), fetchone(), fetchmany() 등을 이용함
        table = pd.DataFrame(rows, columns = [t[0] for t in cur.description]) 
        # description => 각 필드(칼럼) 특징 알아보기 (필드명,데이터형_코드, 표시크기, 내부크기, 정확도, 비율, nullable)
        cur.close() # 메시지 큐에서 연결된 리소스를 해제할 수 있도록 커서 닫기
        conn.close() # sql연결 닫기
        return table

    # SQL에 저장된 테이블들의 이름을 볼 수 있음
    def get_table_names(self):
        conn = pymysql.connect(host=host_IP, user =user_ID, password =password, db =db_name, charset =charset)
        cur = conn.cursor()
        cur.execute(f'SHOW TABLES IN {db_name}') # 데이터베이스 안에 있는 테이블 이름을 보여주는 쿼리문
        rows = cur.fetchall()
        tableList = [tb[0] for tb in rows]
        cur.close()
        conn.close()
        return tableList

    # 폴더에 저장되어 있는 csv파일의 이름을 폴더에서 바로 불러오는 함수
    # 그냥 파일로 csv파일을 객체로 만드는 함수
    # 저희가 쓰는 파일은 5개인데 csv파일로 되어 있는 것들이 없으므로 굳이 필요 없음
    def load_csv(self, tableName):
        table = pd.read_csv(data_path + tableName+'.csv')
        return table

    # 기능: 두 지점 사이 거리 계산(유클리드)
    # 입력: 위경도1, 위경도2
    # 출력: 떨어진 거리(km)
    def cal_dis(self, loc1, loc2):
        self.loc1=loc1
        self.loc2=loc2

        return haversine(self.loc1, self.loc2) # 위경도 데이터를 km거리로 반환
    
    # 기능: 거리에 따른
    # 입력: 유저위치정보
    # 출력: 충전소 정보 데이터 프레임
    def station_df(self,user_loc):
        # 떨어진 거리의 새로운 열 만들기
        for k in [1,3,5]:
            for i in range(len(self.seoul_loc_df)):
                self.seoul_loc_df.loc[i,'dis(km)']=self.cal_dis(user_loc,(self.seoul_loc_df.iloc[i,1],self.seoul_loc_df.iloc[i,2]))
            result_df=self.seoul_loc_df[self.seoul_loc_df['dis(km)']<=k]

            if len(result_df)==0:
                print(f"주변 {k}km내에 있는 충전소가 없습니다.")
                print(f"주변 {k+2}km내에 있는 충전소를 찾습니다.")
            elif len(result_df)==0 and k==5:
                print(f"주변 {k}km내에 있는 충전소가 없습니다.")
                print(f"다른 곳으로 이동 후 다시 정보를 입력해주세요.")
            else:
                break
        
        # 주소데이터를 열로 만들기
        result_df=pd.merge(result_df,self.charge_address_df,how='inner')

        # 충전구분 정보를 열로 만들기
        for i in range(len(result_df)):
            if list(self.speed_df.station).count(result_df.station[i])>=2:
                result_df.loc[i,'speed']='완속/급속'
            else:
                result_df.loc[i,'speed']=self.speed_df.loc[i,'speed']
        
        result_df=result_df.sort_values('dis(km)')
        return result_df

    # 기능: 서울시 구별 등록차량 개수
    # 입력: 사용자 위치 정보
    # 출력: 해당 구의 등록된 차량 개수
    def res_car_cnt(self,address):
        gu=address.split(' ')[1]
        res_car_df=self.car_register_df.iloc[[self.car_register_df.ind[i]-1 for i in range(len(self.car_register_df)) if self.car_register_df.loc[i,'dong'].split(' ')[1]==gu],]

        return res_car_df

    # 기능: 서울시 구별 등록차량 개수 (차량 종류별)
    # 입력: 해당 구의 데프
    # 출력: 차량 종류별
    def gu_res_car_cnt(self,re_car_data):
        gu_res_car_df=pd.DataFrame(re_car_data.groupby('fuel').count()['dong'])
        gu_res_car_df=gu_res_car_df.T
        gu_res_car_df.index=['count']
        
        return gu_res_car_df
