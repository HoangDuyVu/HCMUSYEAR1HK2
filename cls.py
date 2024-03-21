import json
import csv
import jsonlines
from pyproj import Proj, transform
from shapely.geometry import Point

def LatLngToXY(lat, lng):
    crs_4326 = Proj(init='epsg:4326')  # WGS 84
    crs_3405 = Proj(init='epsg:3405')  # CRS 3405
    x, y = transform(crs_4326, crs_3405, lng, lat)
    return x, y 

class RouteVar:
    def __init__(self, data) -> None:
        self.__TotalInfor = data
        self.__stringInfor = f"{json.dumps(data,ensure_ascii=False)}"

    def get(self, proper):
        return self.__TotalInfor[proper]
    def getTotal(self):
        return self.__TotalInfor
    def set(self, proper, value) -> None:
        self.__TotalInfor[proper] = value

    def get_stringInfor(self):
        return self.__stringInfor

class RouteVarQuery:
    def __init__(self, filejson) -> None:
        self.listRoute = []
        try:
            with open(filejson,'r', encoding='utf8') as f:
                for line in f:
                    val = json.loads(line)
                    self.listRoute.append(RouteVar(val))
        except Exception as e:
            print("erorr",e)
    
    def DisplayAll(self) -> None:
        for data in self.listRoute:
            print(data.get_stringInfor())

    def Display_csv(self,listOut,csvfile):
        with open(csvfile,'w',newline='') as sv:
            csv_writer = csv.writer(sv)
            for data in listOut:
                csv_writer.writerow(data.getTotal())

    def Display_json(self,listOut,jsonfile):
            
        # with open(jsonfile,'w',encoding='utf8') as sv:
        #     json.dump(List,sv,indent=4,ensure_ascii=False)
        with jsonlines.open(jsonfile, mode='w') as writer:
            for data in listOut:
                writer.write(data.getTotal())

    def Sreach(self,Input):

        if (len(Input) == 0):
            self.Display_csv(self.listRoute,"out.csv")
            self.Display_json(self.listRoute,"out.json")
        else:
            Ouput = []
            for data in self.listRoute:
                A = data.get_stringInfor()
              #  print(A,'\n',Input)
                if (A.find(Input) != -1):
                    Ouput.append(data)
            self.Display_csv(Ouput,"out.csv")
            self.Display_json(Ouput,"out.json")

class Stop:
    def __init__(self,data) -> None:
        self.__data = data
        self.__String = f"{json.dumps(data,ensure_ascii=False)}"
    
    def Get(self,proper):
        return self.__data[proper]
    
    def GetStops(self):
        return self.__data
    
    def Set(self,proper,value) -> None:
        self.__data[proper] = value
    
    def GetString(self):
        return self.__String

class StopQuery:
    def __init__(self,filejson) -> None:
        self.__listStops = []
        try:
            with open(filejson,'r', encoding='utf8') as f:
                for data in f:
                    val = json.loads(data)
                    self.__listStops.append(Stop(val))
        except Exception as e:
            print("erorr",e)

    def Display_csv(self,listOut,csvfile):
        with open(csvfile,'w',newline='') as sv:
            csv_writer = csv.writer(sv)
            for data in listOut:
                csv_writer.writerow(data.GetStops())

    def Display_json(self,listOut,jsonfile):

        list = []
        for data in listOut:
            list.append(data.GetStops())
        with open(jsonfile,'w',encoding='utf8') as sv:
            json.dump(list,sv,indent=4,ensure_ascii=False)
        # with jsonlines.open(jsonfile, mode='w') as writer:
        #     for data in listOut:
        #         writer.write(data.GetStops())

    def Sreach(self,Input):
        if (len(Input) == 0):
            self.Display_csv(self.__listStops,"out.csv")
            self.Display_json(self.__listStops,"out.json")
        else:
            Ouput = []
            for data in self.__listStops:
                A = data.GetString()
              #  print(A,'\n',Input)
                if (A.find(Input) != -1):
                    Ouput.append(data)
            self.Display_csv(Ouput,"out.csv")
            self.Display_json(Ouput,"out.json")

class PathVar:
    def __init__(self,data) -> None:
        self.__infor = data
        self.__x = []
        self.__y = []
    
    def get(self,Name):
        return self.__infor[Name]
    
    def set(self, Name, value) -> None:
        self.__infor[Name] = value
    
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
            point = Point(X, Y)
           # print(point)
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

