from pyproj import Proj, transform
import json

class PathVar:
    def __init__(self,data) -> None:
        self.__infor = data
        self.__x = []
        self.__y = []
    
    def get(self,Name):
        return self.__infor[Name]
    
    def set(self, Name, value) -> None:
        self.__infor[Name] = value

    def LatLngToXY(self) -> None:

        for data in self.__infor["lat"]:
            self.__x.append(data)
        for data in self.__infor["lng"]:
            self.__y.append(data)
        crs_4326 = Proj(init='epsg:4326')  # WGS 84
        crs_3405 = Proj(init='epsg:3405')  # CRS 3405
        
        for i in range(len(self.__x)):
            lat = self.__x[i]
            lng = self.__y[i]
            x, y = transform(crs_4326, crs_3405, lng, lat)
            self.__x[i] = x
            self.__y[i] = y
    
    def ToLineString(self):
        x = {"type": "Feature",
            "properties": {}}
        for data in self.__infor["lat"]:
            self.__x.append(data)
        for data in self.__infor["lng"]:
            self.__y.append(data)
        coor = []
       # print(len(self.__x))
        for i in range(len(self.__x)):
            lat = self.__x[i]
            lng = self.__y[i]
            X = lng
            Y = lat
            coor.append([X,Y])
        List = {}
        List["coordinates"] = coor
        List["type"] = "LineString"
        x["geometry"] = List
        return x



class PathVarQuery:
    def __init__(self,jsonFile) -> None:
        self.__listPath = []
        try:
            with open(jsonFile,'r',encoding='utf-8') as f:
                    for line in f:
                        val = json.loads(line)
                        self.__listPath.append(PathVar(val))
        except Exception as e:
            print("erorr",e)
    
    def DisPlay(self):
        for data in self.__listPath:
            data.LatLngToXY()
    
    def JsonToLineString(self,jsonfile) -> None:
        List = []
        for data in self.__listPath:
            List.append(data.ToLineString())
        x = {"type": "FeatureCollection"}
        x["features"] = List

        with open(jsonfile,'w',encoding='utf8') as sv:
            json.dump(x,sv,indent=4,ensure_ascii=False)

