import json
import csv
import pandas as pd

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

        List = []
        for data in listOut:
            List.append(data.getTotal())
            
        with open(jsonfile,'w',encoding='utf8') as sv:
            json.dump(List,sv,indent=4,ensure_ascii=False)

    def Sreach(self,Input):

        if (len(Input) == 0):
            self.Display_csv(self.listRoute,"/Users/macbookpro/Documents/HCMUS/W05/out.csv")
            self.Display_json(self.listRoute,"/Users/macbookpro/Documents/HCMUS/W05/out.json")
        else:
            Ouput = []
            for data in self.listRoute:
                A = data.get_stringInfor()
              #  print(A,'\n',Input)
                if (A.find(Input) != -1):
                    Ouput.append(data)
            self.Display_csv(Ouput,"/Users/macbookpro/Documents/HCMUS/W05/out.csv")
            self.Display_json(Ouput,"/Users/macbookpro/Documents/HCMUS/W05/out.json")

class Stop:
    def __init__(self,data) -> None:
        Stop.__data = data
    
    def get(self,proper):
        return Stop.__data[proper]
    
    def getStops(self):
        return Stop.__data
    
    def set(self,proper,value) -> None:
        Stop.__data[proper] = value
    



             