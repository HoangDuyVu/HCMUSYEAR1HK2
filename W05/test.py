import math
import heapq

def euclidean_distance(x1, y1, x2, y2):
    # Tính khoảng cách Euclid giữa hai điểm (x1, y1) và (x2, y2)
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def input_graph_with_coordinates():
    graph = {}
    num_vertices = int(input("Nhập số lượng đỉnh của đồ thị: "))
    num_edges = int(input("Nhập số lượng cạnh của đồ thị: "))
    
    for i in range(num_vertices):
        print(f"Nhập thông tin cho đỉnh thứ {i + 1}:")
        vertex_name = input("Tên đỉnh: ")
        x, y = map(float, input("Nhập tọa độ x và y: ").split())
        graph[(x, y)] = vertex_name
    
    for i in range(num_edges):
        print(f"Nhập thông tin cho cạnh thứ {i + 1}:")
        start_vertex_coords = tuple(map(float, input("Nhập tọa độ x và y của đỉnh xuất phát: ").split()))
        end_vertex_coords = tuple(map(float, input("Nhập tọa độ x và y của đỉnh kết thúc: ").split()))
        
        # Tính toán khoảng cách Euclid giữa hai đỉnh và sử dụng nó làm trọng số của cạnh
        weight = euclidean_distance(start_vertex_coords[0], start_vertex_coords[1], end_vertex_coords[0], end_vertex_coords[1])
        
        # Thêm cạnh vào đồ thị
        if graph[start_vertex_coords] not in graph:
            graph[graph[start_vertex_coords]] = {}
        graph[graph[start_vertex_coords]][graph[end_vertex_coords]] = weight
        
        # Đảo ngược cạnh nếu đồ thị là vô hướng
        if graph[end_vertex_coords] not in graph:
            graph[graph[end_vertex_coords]] = {}
        graph[graph[end_vertex_coords]][graph[start_vertex_coords]] = weight
    
    return graph

def dijkstra_with_coordinates(graph, start):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    pq = [(0, start)]
    
    while pq:
        current_distance, current_vertex = heapq.heappop(pq)
        
        if current_distance > distances[current_vertex]:
            continue
        
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return distances

# Nhập đồ thị từ bàn phím với các cạnh được chỉ định bằng độ dài
graph = input_graph_with_coordinates()
print("Đồ thị bạn vừa nhập là:")
print(graph)

# Áp dụng thuật toán Dijkstra cho đồ thị đã nhập
#start_vertex = input("Nhập
