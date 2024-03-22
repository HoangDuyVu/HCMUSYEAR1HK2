from cls import RouteVarQuery
from cls import StopQuery
from cls import PathVarQuery
from cls import Graph

#print("You want to access route or stops?")

TheRoute = RouteVarQuery('vars.json')
TheStops = StopQuery('stops.json')
ThePath =  PathVarQuery('paths.json')
TheStops.AddStopInRouteVar(TheRoute)
ThePath.AddPathsInRouteVar(TheRoute)
TheRoute.DisplayAll('out.json')
TheGraph = Graph(TheRoute)

# id = input()
# if id == "route" or id == "Route" or id == "R" or id == "r" or id == '1':
#     #list.DisplayAll()
#     print("Please enter the information you want to search for:")
#     Input = input()
                    
#     list.Sreach(Input)
# else:

#     print("Please enter the information you want to search for:")
#     Input = input()
                    
#     list.Sreach(Input)
