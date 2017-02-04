#Karuna Ramkumar, 800906857, k@uncc.edu
import sys,getopt,struct, heapq
##from Graph import Graph
####from Heap import MinHeap
##from Vertex import Vertex
##from Edge import Edge
from Queue import Queue


class Graph:
    def __init__(self):#stores all graph related information
        self.vertices = {}#vertices
        self.edges = {}#edges
        self.adjList = {}#adjacency list
        #they are initialized empty and then appended with information as and when we add an element
        
    def addvertex(self,vertexName,vertex):
        #add a new vertex
        self.vertices[vertexName] = vertex
        
    def addedge(self,edgeKey,Edge):
        #add a new edge
        self.edges[edgeKey] = Edge

    def deleteedge(self,vertex1,vertex2):
        #to delete the edge
        del self.edges[(vertex1,vertex2)]
        self.adjList[vertex1].remove(vertex2)

    def updateedge(self,head,tail,time):#update edge is called whenever a new addedge query occurs
        if not self.vertices.has_key(head):
            #if a vertex not in list occurs
            self.addvertex(head,Vertex(head,True))
        if not self.vertices.has_key(tail):
            
            self.addvertex(tail,Vertex(tail,True))
        if self.edges.has_key((head,tail)):
            #if edge is already present
            self.edges[(head,tail)].transmit_time = float(time)
        else:
            #if we need to create a new edge
            self.addedge((head,tail),Edge(head,tail,time,True))
            self.add_adj_list(head,tail)
            self.add_adj_list(tail,None)

    def edgedown(self,head,tail):#sets the edge flag down
        self.edges[(head,tail)].up = False

    def edgeup(self,head,tail):#sets the edge flag up
        self.edges[(head,tail)].up = True

    def vertexup(self,vertex):#sets the vertex flag up
        self.vertices[vertex].up = True

    def vertexdown(self,vertex):#sets the vertex flag down
        self.vertices[vertex].up = False

    def add_adj_list(self,vertex1,vertex2):#updates the adjacency list
        if not vertex2 == None:
            self.adjList.setdefault(vertex1,[]).append(vertex2)
        else:
            self.adjList.setdefault(vertex1,[])

    def reachable(self):#called when query reachable is posted
        for vertex in (sorted(self.vertices.keys())):
            if self.vertices[vertex].up == True:
                self.reachable_vertices(vertex)
                
    def reachable_vertices(self,vertex):#checks all the status flags and prints
                                        #a list of all the reachable vertices
        #Running time O(V+E) for BFS
        """We use BFS for this implementation. But worst case running time when all vertices
            are up is O(V*(V+E))"""
        status_flag = {}
        reachable_node_list = {}
        q = Queue()
        filtered_dict = {key: val for key,val in self.vertices.items() if (key != vertex and val.up == True)}
        for i in self.vertices.keys():
            status_flag[i] = "flag1"
        status_flag[vertex] = "up"
        q.put(vertex)
        #checks for reachable vertices
        while not q.empty():
            u = q.get()
            for v in sorted(self.adjList[u]):
                if status_flag[v] == "flag1" and self.vertices[v].up == True and self.edges[(u,v)].up == True:
                    status_flag[v] == "up"
                    q.put(v)
                    reachable_node_list[v] =v
            status_flag[u] = "done"
        print vertex
        for vertex_list in sorted(reachable_node_list.keys()):
            print " ", vertex_list
            
    def dijkstra(self,source,destination):#Dijkstras algorithm implementation
        pq = MinHeap()#done using priority queue binary min heap
        for vertex in self.vertices.keys():
            self.vertices[vertex].prevVertex = None
            self.vertices[vertex].time = float('inf')
            #initially all edges have infinite distance
        self.vertices[source].time = 0.0
        traverse = []
        #add all elements to the heap and then perform dijkstra
        filtered_dict = {key: val for key,val in self.vertices.items() if val.up == True}
        pq.addelements(filtered_dict)
        while pq.vertex_list:
            u = pq.extractMin()
            for v in self.adjList[u.name]:
                if self.vertices[v].up == True and self.edges[(u.name,v)].up == True:
                    if self.vertices[v].time > (self.vertices[u.name].time + self.edges[(u.name,v)].transmit_time) :
                        self.vertices[v].time = self.vertices[u.name].time + self.edges[(u.name,v)].transmit_time
                        self.vertices[v].prevVertex = u
                        pq.decreaseKey(self.vertices[v])
        node = self.vertices[destination]
        while node.prevVertex is not None:
            traverse.append(node.name)
            node = node.prevVertex
        traverse.append(node.name)
        traverse.reverse()
        print " ".join([str(vert) for vert in traverse]),self.vertices[destination].time
        
    def printGraph(self):#called by print query
        for vertices in (sorted(self.vertices.keys())):#sorted is used to alphabetically sort
            print (self.vertices[vertices].name), "DOWN" if (self.vertices[vertices].up == False) else ""
            for adj_vertices in sorted(self.adjList[vertices]):#for printing all elements of graph
              print " ", adj_vertices,self.edges[(vertices,adj_vertices)].transmit_time, "DOWN" if (self.edges[(vertices,adj_vertices)].up == False) else ""


class Edge:#Stores edge information for each object created in the main section
    def __init__(self,sourcevertex,destvertex,transmit_time,up):
        self.sourcevertex = sourcevertex
        self.destvertex = destvertex
        self.transmit_time = float(transmit_time)
        self.up = up
    def __hash__(self):
        return hash((self.sourcevertex,self.destvertex))
    def __eq__(self, other):
        return (self.sourcevertex,self.destvertex,self.transmit_time,self.up) == (other.sourcevertex,other.destvertex,other.transmit_time,other.up)
    

class Vertex:#Stores vertex information for each object created in the main section
    def __init__(self,name,flag):
        self.name = name
        self.up = flag
        self.prev_vertex = None
        self.transmit_time = float('inf')
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        return (self.time) == (other.time)
    def __lt__(self, other):
        return (self.time) < (other.time)
    def __le__(self, other):
        return (self.time) <= (other.time)
    def __ge__(self, other):
        return (self.time) >= (other.time)
    def __gt__(self, other):
        return (self.time) > (other.time)
    def __ne__(self, other):
        return (self.time) != (other.time)


#Binary Min heap priority Queue(Makes the running time of Dijkstra to be O((V+E)Log V))
class MinHeap:
    #Initializing a vertex list construct
    def __init__(self):
        self.vertex_list = []
        
#Add new elements to queue
    def addelements(self,vertices_list):
        for key,value in vertices_list.items():
            if value.up == True:
                self.Insert(value)
                
    def Insert(self,value):
        #insert them to the heap. Called by addelements function
        self.vertex_list.append(value)
        self.shiftDown(0, len(self.vertex_list)-1)
        

#Extract Minimum element out of the queue. Running time O(1)
    def extractMin(self):
        lastelement = self.vertex_list.pop()    
        if self.vertex_list:
            returnelement = self.vertex_list[0]
            self.vertex_list[0] = lastelement
            self.shiftUp(0)#min heapify after popping element
        else:
            returnelement = lastelement
        return returnelement
    
    def decreaseKey(self,vertexValue):
        """Running time O(log n). Used in dijkstras function
        to place the element in proper position"""
        keyindex = self.vertex_list.index(vertexValue)
        while keyindex >0 and self.vertex_list[(keyindex-1)/2]> self.vertex_list[keyindex]:
            temp = self.vertex_list[keyindex]
            self.vertex_list[keyindex] = self.vertex_list[(keyindex-1)/2]
            self.vertex_list[(keyindex-1)/2] = temp
            keyindex= (keyindex-1)/2
#Shift elements to a lower position. Heapify operations and to restore heap order
    def shiftDown(self, start, end):
        newelement = self.vertex_list[end]
        while end  > start:
            index = (end-1)/ 2
            parent_node = self.vertex_list[index]
            if newelement < parent_node:
                self.vertex_list[end] = parent_node
                end = index
                continue
            break
        self.vertex_list[end] = newelement
        
    def shiftUp(self, position):#Shiftup is also used for Heapify and restore heap order.
        #It is used to shift an element to higher position
        end = len(self.vertex_list)
        start_posn = position
        newitem = self.vertex_list[position]
        child = 2*position + 1    
        while child < end:
            right = child + 1
            if right < end and not self.vertex_list[child] < self.vertex_list[right]:
                child = right
            self.vertex_list[position] = self.vertex_list[child]
            position = child
            child = 2*position + 1
        self.vertex_list[position] = newitem
        #new item is inserted by shifting parent node down
        self.shiftDown(start_posn, position)




abc = sys.argv[1] #import file name
source = open('%s' % abc, 'r')  # open a file by the given name
##    input_data = []
##    data = source.readlines()  # store the contents of the file in data
##    for i in data:
##        input_data.extend(i.split())
##    

g = Graph()#initialize the graph
for i in source:#till elements end in text file
    v1 = Vertex(i.split()[0],True)
    v2 = Vertex(i.split()[1],True)
    #Add the vertices and edges to the graph
    g.addvertex(v1.name,v1)
    g.addvertex(v2.name,v2)
    e1 = Edge(i.split()[0],i.split()[1],i.split()[2],True)
    e2 = Edge(i.split()[1],i.split()[0],i.split()[2],True)
    g.addedge((v1.name,v2.name),e1)
    g.addedge((v2.name,v1.name),e2)
    g.add_adj_list(v1.name,v2.name)
    g.add_adj_list(v2.name,v1.name)
source.close()   #close the file opened   
   

while(1):#runs until quit is given as a query
    
    print('Enter your query')
    c = raw_input()
    command=c.split()
    if command[0] in 'addedge':
        g.updateedge(command[1],command[2],command[3])
    elif command[0] in 'deleteedge':
        g.deleteedge(command[1],command[2])
    elif command[0] in 'edgedown':
        g.edgedown(command[1],command[2])
    elif command[0] in 'edgeup':
        g.edgeup(command[1],command[2])
    elif command[0] in 'vertexdown':
        g.vertexdown(command[1])
    elif command[0] in 'vertexup':
        g.vertexup(command[1])
    elif command[0] in 'path':
        g.dijkstra(command[1],command[2])
    elif command[0] in 'print':
        g.printGraph()
    elif command[0] in 'reachable':
        g.reachable()
    elif command[0] in 'quit':
        exit()
    else:
        print "Please provide a valid query to the graph"
    

