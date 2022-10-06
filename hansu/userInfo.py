from geopy.geocoders import Nominatim

class UserInfo :
    def __init__(self, address, crd):
        self.address = address
        self.loc = crd

    @classmethod
    def geocoding(cls, address):
        cls.geolocoder = Nominatim(user_agent = 'South Korea', timeout= 200)
        geo = cls.geolocoder.geocode(address)
        crd = {"lat": str(geo.latitude), "lng": str(geo.longitude)}
        return cls(address, crd)

    @classmethod
    def geocoding_reverse(cls, lat_lng_str):
        cls.geolocoder = Nominatim(user_agent='South Korea', timeout= 200)
        address = cls.geolocoder.reverse(lat_lng_str)
        geo = lat_lng_str.split(', ')
        crd = {"lat": str(geo[0]), "lng": str(geo[1])}
        return cls(address, crd)

    def get_user_info(self):
        print('사용자 현제 위치 :')


