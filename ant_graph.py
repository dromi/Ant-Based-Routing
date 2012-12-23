class Graph:
    def __init__(self):
        self.E = []
        self.V = []

    def add_vertex(self, identify, location):
        v = Vertex(identify, location)
        self.V.append(v)

    def add_edge(self, v1, v2, weight):
        e = Edge(self.V[v1], self.V[v2], weight)    
        self.E.append(e)

    def find_edge(self, v1, v2):
        for i in self.E:
            if ((i.v1 == v1 and i.v2 == v2) or (i.v1 == v2 and i.v2 == v1)):
                return i

    def get_weight(self, edge):
        return edge.w

    def set_weight(self, edge, newWeight):
        edge.w = newWeight

    def get_trail(self, edge):
        return edge.trail

    def set_trail(self, edge, pheromone):
        edge.trail += pheromone

    def runned(self, edge):
        edge.runs += 1

    def reset(self):
        for i in self.E:
            i.trail = 0
            i.runs = 0
            
    def show_graph(self):
        print "DISPLAYING GRAPH:"
        print "VERTICES: " + str(len(self.V)) + " EDGES: " + str(len(self.E))
        print ""
        for i in range(len(self.E)):
            w = self.E[i].w
            t = self.E[i].trail
            r = self.E[i].runs
            print "NO: " + str(i) + ": " + str(w) + "\t-\t" + str(t) +  "\t EDGE RUNS: " + str(r)

class Edge:
    def __init__(self, v1, v2, weight):
        self.v1 = v1
        self.v2 = v2
        self.w = weight
        self.trail = 0
        self.runs = 0
        v1.new_neighbor(v2)
        v2.new_neighbor(v1)


class Vertex:
    def __init__(self, identify, location):
        self.neighbors = []
        self.id = identify
        self.location = location
    def new_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

