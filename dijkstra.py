import heapq

# returns a tuple: (shortest_distance, pred)
import math
from collections import deque


def dijkstra_modified(source, dest, width, height):
    done = set()
    pq = []
    distance = {(x, y): float("inf") for x in range(width) for y in range(height)}
    is_wall = {(x, y): False for x in range(width) for y in range(height)}
    distance[source] = 0
    heapq.heappush(pq, (distance[source], source))
    pred = {(x, y): -1 for x in range(width) for y in range(height)}

    while pq:
        u = heapq.heappop(pq)
        neighbors = get_neighbors(u, width, height)

        if u not in done:
            done.add(u)

            for v in neighbors:
                cost = math.dist(u[1], v)

                if distance[u[1]] + cost < distance[v]:
                    distance[v] = distance[u[1]] + cost
                    pred[v] = u[1]

                    if v not in done:
                        heapq.heappush(pq, (distance[v], v))

                if v == dest:
                    print("Reached destination")
                    return distance[dest], pred


# Prints out the nodes that are taken on the shortest path from source to dest
def get_shortest_path(pred, source, dest):
    # Backtrack from the dest node to the source node to get the shortest path
    path = deque()
    temp_pred = pred[dest]
    path.appendleft(dest)

    while temp_pred != -1:
        path.appendleft(temp_pred)
        temp_pred = pred[temp_pred]

    return path


def get_neighbors(u, width, height):
    x, y = u[1][0], u[1][1]
    adj = set()

    # # upper bound in range is exclusive not inclusive
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (i, j) != (x, y) and (0 <= i < width and 0 < j < height):
                adj.add((i, j))

    return adj


# print(get_neighbors((0, 1), 7, 7))
# print(get_neighbors((4, 1), 7, 7))
# print(get_neighbors((4, 3), 7, 7))
result = dijkstra_modified((3, 3), (5, 6), 7, 7)
print(result)
print(get_shortest_path(result[1], (3, 3), (5, 6)))
