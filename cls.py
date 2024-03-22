import json
import csv
import jsonlines
import math
import heapq
import pyproj
from pyproj import Transformer
from shapely.geometry import Point

source_proj = pyproj.CRS.from_epsg(4326)
target_proj = pyproj.CRS.from_epsg(3405)  # UTM zone 49N
transformer = pyproj.Transformer.from_crs(source_proj, target_proj, always_xy=True)
def LatLngToXY(lat, lng):
    """
    Converts latitude and longitude to x and y coordinates using pyproj.
    """
    x, y = transformer.transform(lng, lat)
    return x, y

def euclidean_distance(x1, y1, x2, y2):
    # Tính khoảng cách Euclid giữa hai điểm (x1, y1) và (x2, y2)
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

class RouteVar:
    def __init__(self, data) -> None:
        self.TotalInfor = data
        self.stringInfor = f"{json.dumps(data,ensure_ascii=False)}"
        self.Stops = {}
        self.Path = {}
        self.EDGE = []

    def Get(self, proper):
        return self.TotalInfor[proper]
    def getTotal(self):
        return self.TotalInfor
    def set(self, proper, value) -> None:
        self.TotalInfor[proper] = value
    def setStops(self,data):
        self.Stops = data
    def setPath(self,data):
        self.Path = data 

    def get_stringInfor(self):
        return self.stringInfor

class RouteVarQuery:
    def __init__(self, filejson) -> None:
        self.listRoute = []
        try:
            with open(filejson,'r', encoding='utf8') as f:
                for line in f:
                    val = json.loads(line)
                    for data in val:
                        self.listRoute.append(RouteVar(data))
        except Exception as e:
            print("erorr",e)
    
    def DisplayAll(self,jsonfile) -> None:
        with open(jsonfile,'w',encoding='utf8') as sv:
            for data in self.listRoute:
                json.dump(data.getTotal(),sv,indent=4,ensure_ascii=False)
                json.dump(data.Stops,sv,indent=4,ensure_ascii=False)
                json.dump(data.Path,sv,indent=4,ensure_ascii=False)
                


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
    def AddStopInRouteVar(self,TheRoute):
        for data in self.__listStops:
            for value in TheRoute.listRoute:
                if int(data.Get("RouteId")) == value.TotalInfor['RouteId'] and int(data.Get("RouteVarId")) == value.TotalInfor['RouteVarId']:
                    value.setStops(data.GetStops())
                    #print(value.Stops)
                    break


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
        self.infor = data
        self.__x = []
        self.__y = []
    
    def Get(self,Name):
        return self.infor[Name]
    
    def set(self, Name, value) -> None:
        self.infor[Name] = value
    
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
        self.listPath = []
        try:
            with open(jsonFile,'r',encoding='utf-8') as f:
                    for line in f:
                        val = json.loads(line)
                        self.listPath.append(PathVar(val))
        except Exception as e:
            print("erorr",e)
    
    def DisPlay(self):
        for data in self.listPath:
            data.LatLngToXY()
    
    def JsonToLineString(self,jsonfile) -> None:
        List = []
        for data in self.listPath:
            List.append(data.ToLineString())
        x = {"type": "FeatureCollection"}
        x["features"] = List

        with open(jsonfile,'w',encoding='utf8') as sv:
            json.dump(x,sv,indent=4,ensure_ascii=False)
    
    def AddPathsInRouteVar(self,TheRoute):
       for data in self.listPath:
            for value in TheRoute.listRoute:
                if int(data.Get("RouteId")) == value.TotalInfor['RouteId'] and int(data.Get("RouteVarId")) == value.TotalInfor['RouteVarId']:
                    value.setPath(data.infor)
                    #$print(value.Path)
                    break

class Graph:
    def __init__(self,TheRoute) -> None:
        self.IdStop = {}
        self.Graph = {}
        for data in TheRoute.listRoute:
            for val in data.Stops["Stops"]:
                self.IdStop[val["StopId"]] = [val["Lng"],val["Lat"]]
            Sz = len(data.Path["lat"])
            a = 0
            Dis = 0
            TotalDis = 0
            HsTime = 0
            Hs = 0
            Time = 0
            DDis = 0
            DDTime = 0
            #data.EDGE.append([data.Stops["Stops"][a]["Lng"],data.Stops["Stops"][a]["Lat"],data.Stops["Stops"][a]["StopId"]])
            for i in range(1,Sz):
                x1, y1 = LatLngToXY(data.Path["lat"][i - 1],data.Path["lng"][i - 1])
                x2,y2 = LatLngToXY(data.Path["lat"][i],data.Path["lng"][i])
                TotalDis += euclidean_distance(x1,y1,x2,y2)
                #print(x1,' ',y1,' ',x2,' ',y2)
            
            Hs = data.TotalInfor["Distance"]/TotalDis
            HsTime = data.TotalInfor["RunningTime"]/TotalDis
            print(Hs,' ',data.TotalInfor["Distance"], ' ',TotalDis,' ',data.TotalInfor["RunningTime"])
            x1, y1 = LatLngToXY(data.Stops["Stops"][a]["Lat"],data.Stops["Stops"][a]["Lng"])

            #print(len(data.Stops["Stops"]),' ',Sz)
            for i in range(Sz):
                if (a + 1 == len(data.Stops["Stops"])):
                    break

                if (abs(data.Stops["Stops"][a + 1]["Lat"] - data.Path["lat"][i]) <= (-1e-4 - 3e3) or i == Sz - 1):
                    if (data.Stops["Stops"][a]["StopId"] not in self.Graph):
                        self.Graph[data.Stops["Stops"][a]["StopId"]] = []
                    self.Graph[data.Stops["Stops"][a]["StopId"]].append((data.Stops["Stops"][a + 1]["StopId"],Dis,Time))
                    #print(data.Stops["Stops"][a]["StopId"],' ',data.Stops["Stops"][a + 1]["StopId"],' ',Dis)
                    DDis += Dis
                    DDTime += Time
                    Dis = 0
                    x1, y1 = LatLngToXY(data.Stops["Stops"][a + 1]["Lat"],data.Stops["Stops"][a + 1]["Lng"])
                    a += 1

                #x1, y1 = LatLngToXY(data.Stops["Stops"][a + 1]["Lat"],data.Stops["Stops"][a + 1]["Lng"])
                x2,y2 = LatLngToXY(data.Path["lat"][i],data.Path["lng"][i])
                Dis = Dis + euclidean_distance(x1,y1,x2,y2)*Hs
                Time = Time + euclidean_distance(x1,y1,x2,y2)*HsTime
                x1 = x2
                y1 = y2
            
            print(DDis,' ',DDTime)
            #break





