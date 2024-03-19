import json
from cls import RouteVar 
from cls import RouteVarQuery

list = RouteVarQuery('/Users/macbookpro/Documents/HCMUS/W05/vars.json')
#list.DisplayAll()
#list.Sreach()

print("Please enter the information you want to search for:")
Input = input()
                
list.Sreach(Input)