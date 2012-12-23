from optparse import *
from pylab import *
from math import *
from random import *
from ant_graph import Graph

r = random

#Default Vaules:

ite = 100           #Number of ant movement+evaporation iterations
p = 0.5             #Evaporation Factor
f = 6               #pheromone Power
antNum = 11         #Number of Ants
maxWeight = 100     #Maximum weight of edges
mCases = 100        #Default number of testcases for the multi testcase
dCases = 100        #Default number of iterations for the dynamic testcase



class Ant:
    def __init__(self, graph, position):
        self.position = graph.V[position]
        self.graph = graph

    def move(self):
        "Move the ant from on vertex to a random neighbor and exclude pheromone"
        # Find a new position among the neighbors
        n = len(self.position.neighbors)
        num = int(r()*100%n)
        newPos = self.position.neighbors[num]

        # Leave pheromone trail
        edge = self.graph.find_edge(self.position, newPos)
        edgeWeight = self.graph.get_weight(edge)
        edgeTrail  = self.graph.get_trail(edge)
        pheromoneTrail = pow(edgeWeight,f) / (pow(maxWeight,f-1)) + edgeTrail
        self.graph.set_trail(edge, pheromoneTrail)
        self.graph.runned(edge)

        # Move to new position
        self.position = newPos

def evaporate(graph):
    "Evaporates every edge in the given graph"
    for i in graph.E:
        i.trail = (1 - p) * i.trail

def find_shortest_path(graph, start, end, lead, path=[], cost=0,):
    "Finds the shortest path from start to end via a simple recursive brute force algorithm"
    #Add the new node to the path and the weight of the edge to the cost
    path = path + [start.id]
    if(len(path) > 1):
        last_vertex = graph.V[path[-2]]
        edge = graph.find_edge(last_vertex, start)
        if (lead == 'w'):
            cost = cost + edge.w
        if (lead == 't'):
            cost = cost + edge.trail
    #Check whether the end point has been reached
    if start == end:
        return path, cost
    #Check whether the start point exsists in the graph    
    if graph.V.count(start) == 0:
        return None
    shortest = None
    cheapest = None
    #Spawn new instances for each neighbor to the vertex not already in the path
    for node in graph.V[start.id].neighbors:
        if node.id not in path:
            newpair = find_shortest_path(graph, node, end, lead, path, cost)
            newpath = newpair[0]
            newcost = newpair[1]
            #If the found path is better than the current best, it is replaced
            if newpath:
                if not shortest or newcost < cheapest:
                    shortest = newpath
                    cheapest = newcost
    return shortest, cheapest

def path_weight(graph, path):
    "Function for determining the weight of a path"
    weight = 0
    for i in range(1,len(path)):
        v1 = graph.V[path[i-1]]
        v2 = graph.V[path[i]]
        w = graph.find_edge(v1,v2).w
        weight += w
    return weight


def plot_route(graph, t, w):
    "Function for plotting the pheromone and weighted routes using Matplotlib"

    x = map(lambda x: x.location[0], graph.V)
    y = map(lambda x: x.location[1], graph.V)

    #Plot the graph
    subplot(121)
    title('Pheromone Trail')
    for i in graph.E:
        e_x = [i.v1.location[0], i.v2.location[0]]
        e_y = [i.v1.location[1], i.v2.location[1]]
        plot(e_x, e_y, 'b', zorder=1, lw=2)
    scatter(x,y,s=120, zorder=2)
    #Plot the shortest path using pheromone trails
    x_t = map(lambda x: graph.V[x].location[0], t)
    y_t = map(lambda x: graph.V[x].location[1], t)
    plot(x_t, y_t, 'g', zorder=1, lw=5)
            
    #Plot the graph
    subplot(122)
    title('True Weight')
    for i in graph.E:
        e_x = [i.v1.location[0], i.v2.location[0]]
        e_y = [i.v1.location[1], i.v2.location[1]]
        plot(e_x, e_y, 'b', zorder=1, lw=2)
    scatter(x,y,s=120, zorder=2)
    #Plot the shortest path using weight values
    x_w = map(lambda x: graph.V[x].location[0], w)
    y_w = map(lambda x: graph.V[x].location[1], w)
    plot(x_w, y_w, 'r', zorder=1, lw=5)

    #In a new plot, draw the weight of the edges compared to pheromone values of the edge
    figure()
    t = map(lambda x: x.trail, graph.E)
    w = map(lambda x: x.w, graph.E)    
    plot(t, 'g-', label='Pheromone value')
    plot(w, 'r-', label='True weight value')
    legend()

    show()
    


def create_test_graph():
    "Create and fill in the standard test graph"
    g = Graph()

    g.add_vertex(0, [0,0])

    g.add_vertex(1, [0,4])
    g.add_vertex(2, [2,3])
    g.add_vertex(3, [3,2])

    g.add_vertex(4, [1,6])
    g.add_vertex(5, [2,6])
    g.add_vertex(6, [5,6])
    g.add_vertex(7, [7,4])

    g.add_vertex(8,  [2,8])
    g.add_vertex(9,  [4,8])
    g.add_vertex(10, [6,8])


    g.add_edge(0, 1, 40)
    g.add_edge(1, 2, 67)
    g.add_edge(2, 3, 12)
    g.add_edge(3, 0, 27)
    
    g.add_edge(1, 4, 11)
    g.add_edge(4, 2, 5 ) 
    g.add_edge(2, 5, 82)
    g.add_edge(2, 6, 75)
    g.add_edge(3, 7, 91)

    g.add_edge(4, 5, 15)
    g.add_edge(5, 6, 20)
    g.add_edge(6, 7, 41)
    
    g.add_edge(4, 8, 30)
    g.add_edge(5, 9, 27)
    g.add_edge(5, 10, 35)
    g.add_edge(6, 10, 45)

    g.add_edge(8, 9 , 30)
    g.add_edge(9, 10, 17)

    return g

def test_pheromones():
    "Display pheromone exclusion and evaporation formulas"
    pheromoneList = []
    for i in range(1,maxWeight+1):
        l = pow(i,f) / (pow(maxWeight,f-1))
        pheromoneList.append(l)
    print pheromoneList
    plot(pheromoneList, 'g-')

    pheromoneList = []
    for i in range(1,maxWeight+1):
        l = (1 - p) * i     #EVAPORATION HAPPENS HERE. DETERMINING FACTOR.
        pheromoneList.append(l)
    plot(pheromoneList, 'r-')

    show()


    
def single_case():
    "Method for testing with a single case"

    g = create_test_graph()

    ants = []
    graph_vertices = len(g.V)

    for i in range(antNum):
        place = int(r()*100%graph_vertices)
        a = Ant(g, place)
        ants.append(a)

    for i in range(ite):
        for i in ants:
            i.move()    
        evaporate(g)

    g.show_graph()

    pairW = find_shortest_path(g, g.V[0], g.V[10], 'w')
    pairT = find_shortest_path(g, g.V[0], g.V[10], 't')

    print "FOUND WEIGHT PATH:"
    print pairW

    print "FOUND PHEROMONE PATH:"
    print pairT

    weight = path_weight(g, pairT[0])

    print "ANTS OFF BY: " + str(weight) + " - " + str(pairW[1]) + " = " + str(weight - pairW[1])
    plot_route(g, pairT[0], pairW[0])


def multi_case(caseNo):
    "Method for testing multiple testcases"
    results = []

    g = create_test_graph()
    ants = []
    graph_vertices = len(g.V)

    for i in range(antNum):
        place = int(r()*100%graph_vertices)
        a = Ant(g, place)
        ants.append(a)

    for i in range(caseNo):
        g.reset()
        for j in range(ite):
            for a in ants:
                a.move()    
            evaporate(g)

        pairW = find_shortest_path(g, g.V[0], g.V[10], 'w')
        pairT = find_shortest_path(g, g.V[0], g.V[10], 't')

        weight = path_weight(g, pairT[0])

        results.append(weight - pairW[1])

        if((i+1) % 10 == 0):
            print "TEST CASE: " + str(i+1) + " FINISHED"

    averageResult = float(sum(results))/len(results)
    averageList = []
    for i in results:
        averageList.append(averageResult)

    print ""
    print "FINAL RESULTS: " + str(results)
    print "AVERAGE: " + str(averageResult)

    avg = "Average: " + str(averageResult)
    plot(results, 'b-', label="Pheromone path diffrentiation")
    plot(averageList, 'r-', label=avg)
    legend()

    show()

def dynamic_case(iterations, agressive):
    "Method for testing a dynamic testcase"
    g = create_test_graph()

    ants = []
    graph_vertices = len(g.V)

    for i in range(antNum):
        place = int(r()*100%graph_vertices)
        a = Ant(g, place)
        ants.append(a)
    

    "Keep ants rolling through graph until the shortest path is found"
    diff = inf
    while(diff > 0):
        g.reset()
        for j in range(ite):
            for a in ants:
                a.move()    
            evaporate(g)

        pairW = find_shortest_path(g, g.V[0], g.V[10], 'w')
        pairT = find_shortest_path(g, g.V[0], g.V[10], 't')
        weight = path_weight(g, pairT[0])

        diff = weight - pairW[1]

    "Alter edges in the graph to reroute the shortest path"

    if (agressive):
        for e in g.E:
            randWeight = int(r()*100)
            e.w = randWeight
    else:

        edge = g.find_edge(g.V[1], g.V[2])
        g.set_weight(edge, 3)

        edge = g.find_edge(g.V[2], g.V[4])
        g.set_weight(edge, 99)

        edge = g.find_edge(g.V[4], g.V[5])
        g.set_weight(edge, 64)

        edge = g.find_edge(g.V[9], g.V[10])
        g.set_weight(edge, 36)

    g.show_graph()
    
    
    results = []
    "first result is incerted before any ant movement"
    pairW = find_shortest_path(g, g.V[0], g.V[10], 'w')
    pairT = find_shortest_path(g, g.V[0], g.V[10], 't')
    weight = path_weight(g, pairT[0])
    diff = weight - pairW[1]

    print "INITIAL:"
    print "ANTS OFF BY: " + str(weight) + " - " + str(pairW[1]) + " = " + str(weight - pairW[1])
    plot_route(g, pairT[0], pairW[0])

    results.append(diff)

    for i in range(iterations):

        for a in ants:
            a.move()
        evaporate(g)

        pairW = find_shortest_path(g, g.V[0], g.V[10], 'w')
        pairT = find_shortest_path(g, g.V[0], g.V[10], 't')


        weight = path_weight(g, pairT[0])
        print "ITERATION: " + str(i)
        print "ANTS OFF BY: " + str(weight) + " - " + str(pairW[1]) + " = " + str(weight - pairW[1])
        results.append(weight - pairW[1])

    plot(results, label="Pheromone path diffrentiation")
    legend()
    show()    


def main():
    
    parser = OptionParser()

    parser.add_option("-s", "--single", action="store_false", help="run a single ant-testcase", dest="use_multi", default=False)
    parser.add_option("-p", "--pheromone-test", action="store_true", help="plot the formulas used for pheromone trailing & evaporation", dest="test_pheromone", default=False)
    
    multiGroup = OptionGroup(parser, "Options for running tests of multiple cases")
    multiGroup.add_option("-m", "--multi", action="store_true", help="run a series of multiple ant-testcases", dest="use_multi", default=False)
    multiGroup.add_option("-c", "--cases", dest="case_No", help="define the number of testcases, default = 100", default=mCases)
    parser.add_option_group(multiGroup)

    dynGroup = OptionGroup(parser, "Options for dynamically changing test cases")
    dynGroup.add_option("-d", "--dynamic-test", action="store_true", help="run a dynamically changing ant-testcase", dest="test_dynamism", default=False)
    dynGroup.add_option("-i", "--iterations", dest="dynamic_ite", help="define the number of iterations, default = 100", default=dCases)
    dynGroup.add_option("-r", "--randomized", action="store_true", dest="agressive", 
                        help="the changes to the test graph are made by random, instead of using predefined changes", default=False)
    parser.add_option_group(dynGroup)
    
    (options, args) = parser.parse_args()

    if options.use_multi:
        multi_case(int(options.case_No))
    elif options.test_pheromone:
        test_pheromones()
    elif options.test_dynamism:
        dynamic_case(int(options.dynamic_ite), options.agressive)
    else:
        single_case()


if __name__ == "__main__":
    main()
