from rtree import index
from shapely.geometry import Point

# Create an Rtree index
idx = index.Index()

# Insert spatial objects into the index
idx.insert(0, (0, 0, 1, 1), obj=Point(0.5, 0.5))
idx.insert(1, (1, 1, 2, 2), obj=Point(1.5, 1.5))
idx.insert(2, (2, 2, 3, 3), obj=Point(2.5, 2.5))

# Perform a spatial query to find objects intersecting a given bounding box
query_bbox = (0, 0, 1.5, 1.5)
result_ids = list(idx.intersection(query_bbox))

# Retrieve the spatial objects corresponding to the query results
query_results = [idx.get(id).object for id in result_ids]

print("Spatial query results:", query_results)
