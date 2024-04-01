from cls import RouteVarQuery
from cls import StopQuery
from cls import PathVarQuery
from cls import Graph
import time
start_time = time.time()

#print("You want to access route or stops?")

TheRoute = RouteVarQuery('vars.json')
TheStops = StopQuery('stops.json')
ThePath =  PathVarQuery('paths.json')
TheStops.AddStopInRouteVar(TheRoute)
ThePath.AddPathsInRouteVar(TheRoute)
TheGraph = Graph(TheRoute)
TheGraph.DijkSra()
#TheGraph.OutAllPair(2)
#TheGraph.ShortestAB(1,35)
TheGraph.topVertexPop(10)

end_time = time.time()
execution_time = end_time - start_time
print("Time Running:", execution_time, "Second")
