import json
import csv
import jsonlines

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
            self.Display_csv(self.__listStops,"/Users/macbookpro/Documents/HCMUS/W05/out.csv")
            self.Display_json(self.__listStops,"/Users/macbookpro/Documents/HCMUS/W05/out.json")
        else:
            Ouput = []
            for data in self.__listStops:
                A = data.GetString()
              #  print(A,'\n',Input)
                if (A.find(Input) != -1):
                    Ouput.append(data)
            self.Display_csv(Ouput,"/Users/macbookpro/Documents/HCMUS/W05/out.csv")
            self.Display_json(Ouput,"/Users/macbookpro/Documents/HCMUS/W05/out.json")