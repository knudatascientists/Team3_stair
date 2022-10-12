from geopy.geocoders import Nominatim

# 유저 정보 입력 클래스
class UserInfo:
    def __init__(self, address, crd):
        self.address = address
        self.loc = crd

    # 객체를 생성하지 않고 사용할 때 cls라고 함
    @classmethod
    def geocoding(cls, address): # 사용자의 주소정보를 입력
        cls.geolocoder = Nominatim(user_agent = 'South Korea', timeout= 200)
        geo = cls.geolocoder.geocode(address)
        crd = (geo.latitude,geo.longitude)
        return cls(address, crd) # 객체 안에 저장됨 => address는 self.address에 crd는 self.loc에 저장
        # return (address, crd)

    @classmethod
    def geocoding_reverse(cls, lat_lng_str): # 사용자의 위경도 데이터를 입력
        cls.geolocoder = Nominatim(user_agent='South Korea', timeout= 200)
        address = cls.geolocoder.reverse(lat_lng_str)
        geo = lat_lng_str.split(', ')
        crd = (float(geo[0]),float(geo[1]))
        return cls(address, crd)
        # return (address, crd)

    def get_user_info(self):
        print('사용자 현재 위치 :', self.address)
        print(f'위도 : {self.loc[0]}, 경도 : {self.loc[1]}')

# Nominatim함수의 timeout옵션은 예외발생하기전 대기하는 시간을 의미
# geocode는 Nominatim함수 안에 있는 메소드로
# geo변수안에는 .을 치면 안에 있는 여러개의 메서드들을 불러올수 있다.
# geo.latitude(위도)와 geo.longigude(경도)가 대표적인 ex 입니다.