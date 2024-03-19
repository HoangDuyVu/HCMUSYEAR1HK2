import json
import csv
import pandas as pd

class RouteVar:
    def __init__(self, data) -> None:
        self.__RouteId = data["RouteId"]
        self.__RouteVarId = data["RouteVarId"]
        self.__RouteVarName = data["RouteVarName"]
        self.__RouteVarShortName = data["RouteVarShortName"]
        self.__RouteNo = data["RouteNo"]
        self.__StartStop = data["StartStop"]
        self.__EndStop = data["EndStop"]
        self.__Distance = data["Distance"]
        self.__Outbound = data["Outbound"]
        self.__RunningTime = data["RunningTime"]
        self.__TotalInfor = data

    def get(self, proper):
        return self.__TotalInfor[proper]
    def getTotal(self) -> None:
        return self.__TotalInfor
    def set(self, proper, value) -> None:
        self.__TotalInfor[proper] = value

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
    
    def DisplayAll(self) -> None:
        for data in self.listRoute:
            print(data.getTotal())

    def Display_csv(self,listOut,csvfile):
        with open(csvfile,'w',newline='') as sv:
            csv_writer = csv.writer(sv)
            for data in listOut:
                csv_writer.writerow(data.getTotal())

    def Display_json(self,listOut,jsonfile):

        List = []
        for data in listOut:
            List.append(data.getTotal())
            
        with open(jsonfile,'w',encoding='utf8') as sv:
            json.dump(List,sv,indent=4,ensure_ascii=False)

    def Sreach(self):
        self.Display_csv(self.listRoute,'out.csv')
        self.Display_json(self.listRoute,'out.json')
    



             