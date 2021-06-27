import heapdict

G = {'A': ('B', 'H'),
     'B': ('A', 'C', 'H'),
     'C': ('B', 'D', 'F', 'I'),
     'D': ('C', 'E', 'F'),
     'E': ('D', 'F'),
     'F': ('C', 'D', 'E', 'G'),
     'G': ('F', 'H', 'I'),
     'H': ('A', 'B', 'G', 'I'),
     'I': ('C', 'G', 'H'),
     }
W = {('A', 'B'): 4, ('A', 'H'): 8, ('B', 'A'): 4, ('B', 'C'): 8, ('B', 'H'): 11, ('C', 'B'): 8, ('C', 'D'): 7,
     ('C', 'F'): 4, ('C', 'I'): 2, ('D', 'C'): 7,
     ('D', 'E'): 9, ('D', 'F'): 14, ('E', 'D'): 9, ('E', 'F'): 10, ('F', 'C'): 4, ('F', 'D'): 14, ('F', 'E'): 10,
     ('F', 'G'): 2, ('G', 'F'): 2, ('G', 'H'): 1, ('G', 'I'): 6,
     ('H', 'A'): 8, ('H', 'B'): 11, ('H', 'G'): 1, ('H', 'I'): 7, ('I', 'C'): 2, ('I', 'G'): 7, ('I', 'H'): 8}


def dijkstra(G, W, s):
    # s starting vertex
    # G -> graph (adj list) 'A':('B', 'D')
    # W -> weights of the edges
    # Q -> lengths of shortest paths (for priority queue)
    # SP -> length of shortest path
    # P -> predecessor relationship
    # vertex --> list of vertexes
    P = {}
    Q = heapdict.heapdict()
    SP = {}
    for i in G.keys():
        Q[i] = float('inf')
        SP[i] = float('inf')
        P[i] = "null"
    # initalize
    Q[s] = 0
    SP[s] = 0
    while Q:
        lowest_val = Q.peekitem()
        u = lowest_val[0]
        for v in G[u]:
            if SP[v] > SP[u] + W[(u, v)]:
                Q[v] = SP[u] + W[(u, v)]
                SP[v] = SP[u] + W[(u, v)]
                P[v] = u

        Q.popitem()
    return SP

# shortest path to destination
def dijkstra2(G, W, s, l):
    # l vertex that we want to find the shortest path(destination)
    # s starting vertex
    # G -> graph (adj list) 'A':('B', 'D')
    # W -> weights of the edges
    # Q -> weights of the shortest paths (for priority queue)
    # SP -> weights of the shortest paths
    # P -> predecessor relationship
    P = {}
    Q = heapdict.heapdict()
    SP = {}
    for i in G.keys():
        Q[i] = float('inf')
        SP[i] = float('inf')
        P[i] = "null"
    # initalize
    Q[s] = 0
    SP[s] = 0
    while Q:
        lowest_val = Q.peekitem()
        u = lowest_val[0]
        for v in G[u]:
            if u == l:
                break
            else:
                if SP[v] > SP[u] + W[(u, v)]:
                    Q[v] = SP[u] + W[(u, v)]
                    SP[v] = SP[u] + W[(u, v)]
                    P[v] = u

        Q.popitem()
    x = l
    shortest_path = []
    shortest_path.append(l)
    while P[l] != "null":
        shortest_path.append(P[l])
        l = P[l]
    shortest_path.reverse()
    shortest_path.append(SP[x])
    return shortest_path





#shortest path to destination using bi-directional dijkstra search

def dijkstra3(G,W,s,l):
    # l vertex that we want to find the shortest path(destination)
    # s starting vertex
    # G -> graph (adj list) 'A':('B', 'D')
    # W -> weights of the edges
    # Qf -> weights of the shortest paths (for priority queue) forward search
    # Qb -> weights of the shortest paths (for priority queue) backward search
    # SPb -> weights of the shortest paths backward
    # SPf -> weights of the shortest paths forward
    # P -> predecessor relationship
    # mt -> current distance s to l
    Pf = {}
    Pb = {}
    Qf = heapdict.heapdict()
    Qb = heapdict.heapdict()
    SPb = {}
    SPf = {}
    for i in G.keys():
        Qb[i] = float('inf')
        Qf[i] = float('inf')
        SPf[i] = float('inf')
        SPb[i] = float('inf')
        Pf[i] = "null"
        Pb[i] = "null"
    # initalize
    Qb[l] = 0
    Qf[s] = 0
    SPb[l] = 0
    SPf[s] = 0
    mt = float('inf')
    # bridge = A node that is on the shortest path
    bridge = 0
    while Qf and Qb:
        lowest_val_forward = Qf.peekitem()
        lowest_val_backward = Qb.peekitem()
        # u_f, u_b min values, v_b and v_f vertexes that have the min value
        v_b = lowest_val_backward[0]
        v_f = lowest_val_forward[0]
        u_f = lowest_val_forward[1]
        u_b = lowest_val_backward[1]
        if u_f + u_b >= mt:
            break
        #relaxing the edges
        for v in G[v_f]:
            if SPf[v] > SPf[v_f] + W[(v_f, v)]:
                Qf[v] = SPf[v_f] + W[(v_f, v)]
                SPf[v] = SPf[v_f] + W[(v_f, v)]
                Pf[v] = v_f
            if SPf[v_f] + W[(v_f, v)] + SPb[v] < mt:
                mt = SPf[v_f] + W[(v_f, v)] + SPb[v]
                bridge = v
                continue
        # relaxing the edges
        for v in G[v_b]:
            if SPb[v] > SPb[v_b] + W[(v_b, v)]:
                Qb[v] = SPb[v_b] + W[(v_b, v)]
                SPb[v] = SPb[v_b] + W[(v_b, v)]
                Pb[v] = v_b
            if SPb[v_b] + W[(v_b, v)] + SPf[v] < mt:
                mt = SPb[v_b] + W[(v_b, v)] + SPf[v]
                bridge = v
                continue
        Qb.popitem()
        Qf.popitem()
    x = bridge
    shortest_path = []
    shortest_path.append(bridge)
    while Pf[bridge] != "null":
        shortest_path.append(Pf[bridge])
        bridge = Pf[bridge]
    shortest_path.reverse()
    while Pb[x] != "null":
        shortest_path.append(Pb[x])
        x = Pb[x]
    shortest_path.append(mt)
    return shortest_path

print(dijkstra(G, W, 'A'))
print(dijkstra2(G, W, 'C', 'E'))
print(dijkstra3(G, W, 'C', 'E'))
