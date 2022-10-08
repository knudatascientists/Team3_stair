from geopy.geocoders import Nominatim

# 유저 정보 입력 클래스
class UserInfo:

    def __init__(self, address, crd):
        self.address = address
        self.loc = crd

    @classmethod # 객체를 생성하지 않고 사용할 때 cls라고 함
    def geocoding(cls, address):
        cls.geolocoder = Nominatim(user_agent = 'South Korea', timeout= 200)
        geo = cls.geolocoder.geocode(address)
        crd = (geo.latitude,geo.longitude)
        return cls(address, crd) # 객체 안에 저장됨 => address는 self.address에 crd는 self.loc에 저장
        # return (address, crd)

    @classmethod
    def geocoding_reverse(cls, lat_lng_str): # 위도경도 데이터를 입력하면 주소를 반환
        cls.geolocoder = Nominatim(user_agent='South Korea', timeout= 200)
        address = cls.geolocoder.reverse(lat_lng_str)
        geo = lat_lng_str.split(', ')
        crd = (float(geo[0]),float(geo[1]))
        return cls(address, crd)
        # return (address, crd)

    def get_user_info(self):
        print('사용자 현재 위치 :', self.address)
        print(f'위도 : {self.loc[0]}, 경도 : {self.loc[1]}')

# user1 = UserInfo.geocoding('대구광역시 산격동 글로벌플라자')
# user1.get_user_info()
        


