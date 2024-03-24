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
        self.Graph = {}
        count = 0
        for data in TheRoute.listRoute:
            Sz = len(data.Path["lat"])
            Sz2 = len(data.Stops["Stops"])

            List = []
            i,j,d = (0,0,0)
            while i < Sz  or j < Sz2:
                if (i == Sz or d == 0):
                    x1, y1 = LatLngToXY(data.Stops["Stops"][j]["Lat"],data.Stops["Stops"][j]["Lng"])
                    List.append([x1,y1,data.Stops["Stops"][j]["StopId"]])
                    j += 1
                elif (j == Sz2):
                    x1, y1 = LatLngToXY(data.Path["lat"][i],data.Path["lng"][i])
                    List.append([x1,y1,-1])
                    i += 1
                else:
                    x1,y1 = List[d - 1][0],List[d - 1][1]
                    x2,y2 = LatLngToXY(data.Path["lat"][i],data.Path["lng"][i])
                    x3,y3 = LatLngToXY(data.Stops["Stops"][j]["Lat"],data.Stops["Stops"][j]["Lng"])
                    if (euclidean_distance(x1,y1,x2,y2) < euclidean_distance(x1,y1,x3,y3)):
                        List.append([x2,y2,-1])
                        i += 1
                    else:
                        List.append([x3,y3,data.Stops["Stops"][j]["StopId"]])
                        j += 1
                d += 1
            
            #print(d)
            TotalDis = 0
            TotalTime = 0
            for i in range(1,d):
                TotalDis += euclidean_distance(List[i - 1][0],List[i - 1][1],List[i][0],List[i][1])
                TotalTime += euclidean_distance(List[i - 1][0],List[i - 1][1],List[i][0],List[i][1])
            Hs = data.TotalInfor["Distance"]/TotalDis
            HsTime = data.TotalInfor["RunningTime"]*60/TotalTime

            Dis, Time = 0,0
            PrevId = List[0][2]
            for i in range(1,d):
                Dis += euclidean_distance(List[i - 1][0],List[i - 1][1],List[i][0],List[i][1])*Hs
                Time += euclidean_distance(List[i - 1][0],List[i - 1][1],List[i][0],List[i][1])*HsTime
                if (List[i][2] != -1):
                    u = List[i][2]
                    v = PrevId
                    if (v not in self.Graph):
                        self.Graph[v] = []
                    if (u not in self.Graph):
                        self.Graph[u] = []
                    self.Graph[v].append((u,Dis,Time))
                    PrevId = u
                    Dis, Time = 0,0
                    count += 1
        print(count)

    def DijkSra(self):
        d = 0
        JsonOut = {}
        AllStart = []
        for start in self.Graph:
            distances = {vertex: float('infinity') for vertex in self.Graph}
            times = {vertex: float('infinity') for vertex in self.Graph}
            times[start] = 0
            distances[start] = 0
            pq = [(0, start)]
            while pq:
                d += 1
                current_time, current_vertex = heapq.heappop(pq)
                
                if current_time > times[current_vertex]:
                    continue
                
                for neighbor in self.Graph[current_vertex]:
                    time = current_time + neighbor[2]
                    neighbor_name = neighbor[0]
                    if time < times[neighbor_name]:
                        times[neighbor_name] = time
                        distances[neighbor_name] = distances[current_vertex] + neighbor[1]
                        heapq.heappush(pq, (time,neighbor_name))
            List = []
            for i in self.Graph:
                if (times[i] >= 1e9):
                    continue
                x = {}
                x["To StopID"] = i
                x["Time"] = times[i]
                x["Distance"] = distances[i]
                List.append(x)
            
            Stops = {}
            Stops["StopID"] = start
            Stops["The shortest "] = List
            AllStart.append(Stops)
            break
        JsonOut["Dijkstra"] = AllStart

        with open('dijkstra.json','w',encoding='utf8') as sv:
            json.dump(JsonOut,sv,indent=4,ensure_ascii=False)
            

        #    break
        #print(d)






