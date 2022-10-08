from geopy.geocoders import Nominatim

class UserInfo :

    def __init__(self, address, crd):
        self.address = address
        self.gu = self.address.split(' ')[1]
        self.loc = crd

    # 기능: 주소 변경시 사용자 위치 정보 변경
    def set_add(self, address):
        geo = UserInfo.geolocoder.geocode(address)
        self.address = address
        crd = {"lat": str(geo.latitude), "lng": str(geo.longitude)}
        self.loc = crd
        self.gu = self.address.split(' ')[1]
        
    # 기능: 위/경도 변경시 사용자 위치 정보 변경
    def set_loc(self, lat_lng_str):
        address = UserInfo.geolocoder.reverse(lat_lng_str)
        geo = lat_lng_str.split(', ')
        crd = {"lat": str(geo[0]), "lng": str(geo[1])}
        self.address = address
        self.loc = crd
        self.gu = self.address.split(' ')[1]
        
    # 기능: 주소입력에 따른 사용자 위치정보 생성
    @classmethod
    def geocoding(cls, address):
        cls.geolocoder = Nominatim(user_agent = 'South Korea', timeout= 200)
        geo = cls.geolocoder.geocode(address)
        crd = {"lat": str(geo.latitude), "lng": str(geo.longitude)}
        return cls(address, crd)

    # 기능: 위/경도입력에 따른 사용자 위치정보 생성
    @classmethod
    def geocoding_reverse(cls, lat_lng_str):
        cls.geolocoder = Nominatim(user_agent='South Korea', timeout= 200)
        address = cls.geolocoder.reverse(lat_lng_str)
        geo = lat_lng_str.split(', ')
        crd = {"lat": str(geo[0]), "lng": str(geo[1])}
        return cls(address, crd)

    # 사용자의 위치정보 출력 문자열 반환
    def get_user_info(self):
        print('사용자 현재 위치 :', self.address)
        print(f'위도 : {self.loc["lat"]}, 경도 : {self.loc["lng"]}')
        return f"사용자 현재 위치 : {self.address} \n위도 : {self.loc['lat']}, 경도 : {self.loc['lng']}"


        


