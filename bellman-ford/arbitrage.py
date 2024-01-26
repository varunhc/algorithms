from math import log10

def bfa(graph, vertices, src, dest):
    dist = {}
    for i in vertices:
        dist[i] = float("inf")
    dist[src] = 0
    for i in range(len(vertices)):
        for j in graph:
            if dist[j]==float("inf"):
                continue
            for edge in graph[j]:
                newDistance = dist[j]+edge[1]
                if newDistance<dist[edge[0]]:
                    dist[edge[0]] = newDistance

    if dist[dest]==float("inf"):
        return -1
    return 10**((-1)*dist[dest])


inp = "USD,CAD,1.3;USD,GBP,0.71;USD,JPY,109;GBP,JPY,155"
src = "USD"
dest = "JPY"

graph = {}
vertices = set()
for i in inp.split(";"):
    s, d, w = i.split(",")
    if s in graph:
        graph[s].append([d, (-1)*log10(float(w))])
    else:
        graph[s] = [[d, (-1)*log10(float(w))]]
    if s not in vertices:
        vertices.add(s)
    if d not in vertices:
        vertices.add(d)
print(round(bfa(graph, vertices, src, dest), 2))
