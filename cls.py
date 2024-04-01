import json
import csv
import jsonlines
import math
import heapq
import pyproj
from pyproj import Transformer
from shapely.geometry import Point

import pyproj
from pyproj import Transformer
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
        List = []
        for data in listOut:
            List.append(data.getTotal())
        
        with open(csvfile,'w',newline='') as sv:
            ok = 0
            for data in List:
                fieldnames = data.keys()
                writer = csv.DictWriter(sv,fieldnames=fieldnames)
                if ok == 0:
                    writer.writeheader()
                    ok = 1
                writer.writerow(data)

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
    
    def SreachbyProper(self, proper, val):
        List = []
        for data in self.listRoute:
            if (data.Get(proper) == val):
                List.append(data)
            self.Display_json(List,"out.json")

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

        List = []
        for data in listOut:
            List.append(data.GetStops())
        
        with open(csvfile,'w',newline='') as sv:
            ok = 0
            for data in List:
                fieldnames = data.keys()
                writer = csv.DictWriter(sv,fieldnames=fieldnames)
                if ok == 0:
                    writer.writeheader()
                    ok = 1
                writer.writerow(data)

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

    def SreachbyProper(self, proper, val):
        List = []
        for data in self.__listStops:
            if (data.Get(proper) == val):
                List.append(data)
        self.Display_json(List,"out.json")
        self.Display_csv(List,"out.csv")

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
        self.adj = [[] for _ in range(8000)]
        self.StopsID = [0 for _ in range(8000)]
        self.Dis = [[(0,0) for _ in range(8000)] for _ in range(8000)]
        self.Trace = [[0 for _ in range(8000)] for _ in range(8000)]
        count = 0
        for data in TheRoute.listRoute:
            Sz = len(data.Path["lat"])
            Sz2 = len(data.Stops["Stops"])

            for value in data.Stops["Stops"]:
                self.StopsID[value["StopId"]] = [value["Lat"],value["Lng"]]
            
            for i in range(Sz2 - 1):
                value = data.Stops["Stops"][i]
                self.adj[value["StopId"]].append([data.Stops["Stops"][i + 1]["StopId"],data.TotalInfor["RouteId"],data.TotalInfor["RouteVarId"]])

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

    def DijkSra(self):
        d = 0
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
                        self.Trace[start][neighbor_name] = current_vertex
                        distances[neighbor_name] = distances[current_vertex] + neighbor[1]
                        heapq.heappush(pq, (time,neighbor_name))
            
            for i in self.Graph:
                self.Dis[start][i] = (times[i],distances[i])

    def OutAllPair(self, Option):
        if (Option == 1):
            JsonOut = {}
            AllStart = []             
            
            for start in self.Graph:
                List = []
                for i in self.Graph:
                    if (self.Dis[start][i][0] >= 1e9):
                        continue
                    x = {}
                    x["To StopID"] = i
                    x["Time"] = self.Dis[start][i][0]
                    x["Distance"] = self.Dis[start][i][1]
                    List.append(x)
                
                Stops = {}
                Stops["StopID"] = start
                Stops["The shortest "] = List
                AllStart.append(Stops)

            JsonOut["Dijkstra"] = AllStart

            with open('dijkstra.json','w',encoding='utf8') as sv:
                json.dump(JsonOut,sv,indent=4,ensure_ascii=False)
        else: 
            JsonOut = {}
            with jsonlines.open('dijkstra.json', mode='w') as writer:
                for start in self.Graph:
                    
                    Stops = {}
                    Stops["To StopID"] = []
                    Stops["Time"] = []
                    for i in self.Graph:
                        if (self.Dis[start][i][0] >= 1e9):
                            continue
                        Stops["To StopID"].append(i)
                        Stops["Time"].append(self.Dis[start][i][0])
                    
                    Stops["StopID"] = start
                    writer.write(Stops)
            
    
    def ShortestAB(self,start_stop,end_stop):
        OutJson = {}
        OutJson["Lat"] = []
        OutJson["Lng"] = []
        OutJson["StopID"] = []
        OutJson["Running Time: "] = self.Dis[start_stop][end_stop][0]
        OutJson["Distance: "] = self.Dis[start_stop][end_stop][1]

        if (self.Dis[start_stop][end_stop][0] > 1e9):
            return 
        List = []
        List.append(end_stop)
        while (start_stop != end_stop):
            List.append(self.Trace[start_stop][end_stop])
            end_stop = self.Trace[start_stop][end_stop]
        List.reverse()
        for data in List:
            OutJson["Lat"].append(self.StopsID[data][0])
            OutJson["Lng"].append(self.StopsID[data][1])
            OutJson["StopID"].append(data)
        
        Route = []
        for i in range(len(List) - 1):
            for data in self.adj[List[i]]:
                if (data[0] == List[i + 1]):
                    Route.append((data[1],data[2]))
                    break
        OutJson["RouteId"] = []
        OutJson["RouteVarId"] = []
        for data in Route:
            OutJson["RouteId"].append(data[0])
            OutJson["RouteVarId"].append(data[1])
        
        with jsonlines.open('shortestAB.json', mode='w') as sv:
            sv.write(OutJson)
    def topVertexPop(self,k):
        Count = [[0 for _ in range(2)] for _ in range(8000)]
        for u in self.Graph:
            for v in self.Graph:
                if (self.Dis[u][v][0] < 1e9 and u != v):
                    x = u
                    y = v
                    Count[y][0] += 1
                    while x != y:
                        if (y == 0):
                            #print("co")
                            break
                        Count[self.Trace[u][y]][0] += 1 
                        y = self.Trace[u][y]
        
        for i in range(8000):
            Count[i][1] = i

        Count.sort()
        Count.reverse()

        JsonOut = {}
        JsonOut["Top vertex:"] = []
        for i in range(k):
            List = {}
            List["Top"] = i
            List["StopID"] = Count[i][1]
            List["Number"] = Count[i][0]
            JsonOut["Top vertex:"].append(List)
            print(Count[i][1],' ',Count[i][0])  
        with open('topK.json','w',encoding='utf8') as sv:
            json.dump(JsonOut,sv,indent=4,ensure_ascii=False)     








