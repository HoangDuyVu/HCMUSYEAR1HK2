import json
from cls import RouteVar 
from cls import RouteVarQuery
from cls import StopQuery

print("You want to access route or stops?")

id = input()
if id == "route" or id == "Route" or id == "R" or id == "r" or id == '1':
    list = RouteVarQuery('/Users/macbookpro/Documents/HCMUS/W05/vars.json')
    #list.DisplayAll()

    print("Please enter the information you want to search for:")
    Input = input()
                    
    list.Sreach(Input)
else:
    list = StopQuery('/Users/macbookpro/Documents/HCMUS/W05/stops.json')

    print("Please enter the information you want to search for:")
    Input = input()
                    
    list.Sreach(Input)
