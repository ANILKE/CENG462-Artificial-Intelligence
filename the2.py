class AdjList:  # Class for keeping adjacency list:
    def __init__(self, xAxis, yAxis, name,cost):
        self.vertexXAxis = xAxis  # X-axis of the adjacent node
        self.vertexYAxis = yAxis  # Y-axis of the adjacent node
        self.type = name  # Type of the adjacent node(Start,End,Useable,Obstacle)
        self.cost=cost    #cost of last path
        self.next=None
class Graph:  # Class for Graph
    def __init__(self, grid):
        self.V = len(grid)*len(grid)  # Vertex Number
        self.graph = []  # Adjacency list of graph which contains every customer and start and finish
        for i in range(len(grid)): #Convert gride. Add vertices
            for j in range(len(grid)):
                if(grid[i][j]!='Useable' and grid[i][j]!='End' and grid[i][j]!='Start' and grid[i][j]!='Obstacle'):
                    self.graph.append(AdjList(i, j,grid[i][j] , int(grid[i][j])))
                else:
                    self.graph.append(AdjList(i, j, grid[i][j], 1))
        # Adjacency List

    # Function to add an edge in an undirected graph
    def add_edge(self, src_num, destx, desty, dest_type,cost):  # Function to add new edges
        # Adding the dest node to the source node
        node = AdjList(destx, desty, dest_type,cost)
        node.next = None
        oldnode = self.graph[src_num]
        while oldnode != None:  #find end of the edge list
            addhere = oldnode
            oldnode = oldnode.next
        addhere.next = node #add new edge to end of the edge list

    def print(self):
        for i in range(self.V):
            node=self.graph[i]
            while node:
                print("XAxis:"+str(node.vertexXAxis)+" YAxis:"+str(node.vertexYAxis)+" Type:"+str(node.type)+"---->",end =" ")
                node=node.next
            print(str(i)+"th vertice finished\n")

def getGrid(problem_file_name):  # Parser for input to convert it into a grid table (Works for Single Line Inputs!)
    try:
        file = open(problem_file_name, 'r')
        rawinput = file.read().split("\n")
        locations = {0: 'Start', 1: 'End', 2: 'Obstacle', 3: 'Useable'}  # Dictionary for types

        row_count = int((len(rawinput[0]) + 1) / 2)

        column_count=row_count
        grid = [[locations[3]] * column_count  for i in range(row_count)] #create grid by row number(column number=row number since it is a square grid)
        row=0
        for inputrows in rawinput:
            column =0
            for j in range(len(rawinput[0])):
                if (inputrows[j] == "\t"):
                    continue
                else:
                    #implement the list by type of input
                    if inputrows[j] == '.':
                        grid[row][column] = locations[3]

                    elif inputrows[j] == '#':
                        grid[row][column] = locations[2]

                    elif inputrows[j] == 'E':
                        grid[row][column] = locations[1]

                    elif inputrows[j] == 'S':
                        grid[row][column] = locations[0]
                    else :
                        grid[row][column] = inputrows[j]
                    column+=1
            row += 1

        return grid
    except:
        print("Cannot Open File")

def GraphCreater(grid):
    vertice_count=len(grid)*len(grid)
    owngraph = Graph( grid) #initialize the graph with parsed input grid
    src_number = 0

    for ownvertex in owngraph.graph: #for every vertice except finish node add a edge to other vertices
        if (ownvertex.type != "Obstacle"):

            #Top Left Edge
            if(ownvertex.vertexXAxis==0 and ownvertex.vertexYAxis==0):
                if(grid[ownvertex.vertexXAxis][ownvertex.vertexYAxis+1] !="Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis, ownvertex.vertexYAxis+1, grid[ownvertex.vertexXAxis][ownvertex.vertexYAxis+1],1)
                if (grid[ownvertex.vertexXAxis+1][ownvertex.vertexYAxis] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis+1, ownvertex.vertexYAxis ,grid[ownvertex.vertexXAxis+1][ownvertex.vertexYAxis],1)
            # Top Right Edge
            elif(ownvertex.vertexXAxis==0 and ownvertex.vertexYAxis==len(grid)-1):
                if (grid[ownvertex.vertexXAxis][ownvertex.vertexYAxis-1] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis, ownvertex.vertexYAxis - 1,
                                      grid[ownvertex.vertexXAxis][ownvertex.vertexYAxis - 1],1)
                if (grid[ownvertex.vertexXAxis + 1][ownvertex.vertexYAxis] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis + 1, ownvertex.vertexYAxis,
                                      grid[ownvertex.vertexXAxis + 1][ownvertex.vertexYAxis],1)
            # Bottom Left Edge
            elif (ownvertex.vertexXAxis ==len(grid)-1  and ownvertex.vertexYAxis == 0):
                if (grid[ownvertex.vertexXAxis-1][ownvertex.vertexYAxis] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis-1, ownvertex.vertexYAxis ,
                                      grid[ownvertex.vertexXAxis-1][ownvertex.vertexYAxis],1)
                if (grid[ownvertex.vertexXAxis ][ownvertex.vertexYAxis] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis, ownvertex.vertexYAxis+1,
                                      grid[ownvertex.vertexXAxis][ownvertex.vertexYAxis+1],1)
            # Bottom Right Edge
            elif (ownvertex.vertexXAxis == len(grid)-1 and ownvertex.vertexYAxis == len(grid)):
                if (grid[ownvertex.vertexXAxis][ownvertex.vertexYAxis-1] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis, ownvertex.vertexYAxis-1 ,
                                      grid[ownvertex.vertexXAxis][ownvertex.vertexYAxis-1],1)
                if (grid[ownvertex.vertexXAxis-1][ownvertex.vertexYAxis] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis-1, ownvertex.vertexYAxis,
                                      grid[ownvertex.vertexXAxis-1][ownvertex.vertexYAxis],1)
            # Top Edges
            elif (ownvertex.vertexXAxis ==0):
                if (grid[ownvertex.vertexXAxis][ownvertex.vertexYAxis - 1] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis, ownvertex.vertexYAxis - 1,
                                      grid[ownvertex.vertexXAxis][ownvertex.vertexYAxis - 1],1)
                if (grid[ownvertex.vertexXAxis][ownvertex.vertexYAxis+1] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis, ownvertex.vertexYAxis+1,
                                      grid[ownvertex.vertexXAxis ][ownvertex.vertexYAxis+1],1)
                if (grid[ownvertex.vertexXAxis+1][ownvertex.vertexYAxis] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis + 1, ownvertex.vertexYAxis,
                                      grid[ownvertex.vertexXAxis + 1][ownvertex.vertexYAxis],1)
            # Bottom Edges
            elif(ownvertex.vertexXAxis==len(grid)-1):
                if (grid[ownvertex.vertexXAxis][ownvertex.vertexYAxis - 1] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis, ownvertex.vertexYAxis - 1,
                                      grid[ownvertex.vertexXAxis][ownvertex.vertexYAxis - 1],1)
                if (grid[ownvertex.vertexXAxis-1][ownvertex.vertexYAxis] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis-1, ownvertex.vertexYAxis,
                                      grid[ownvertex.vertexXAxis-1 ][ownvertex.vertexYAxis],1)
                if (grid[ownvertex.vertexXAxis][ownvertex.vertexYAxis+1] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis, ownvertex.vertexYAxis+1,
                                      grid[ownvertex.vertexXAxis][ownvertex.vertexYAxis+1],1)
            # Left Edges
            elif(ownvertex.vertexYAxis==0):
                if (grid[ownvertex.vertexXAxis-1][ownvertex.vertexYAxis ] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis-1, ownvertex.vertexYAxis ,
                                      grid[ownvertex.vertexXAxis-1][ownvertex.vertexYAxis ],1)
                if (grid[ownvertex.vertexXAxis][ownvertex.vertexYAxis+1] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis, ownvertex.vertexYAxis+1,
                                      grid[ownvertex.vertexXAxis ][ownvertex.vertexYAxis+1],1)
                if (grid[ownvertex.vertexXAxis+1][ownvertex.vertexYAxis] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis+1, ownvertex.vertexYAxis,
                                      grid[ownvertex.vertexXAxis+1][ownvertex.vertexYAxis],1)
            #Right edges
            elif(ownvertex.vertexYAxis==len(grid)-1):
                if (grid[ownvertex.vertexXAxis][ownvertex.vertexYAxis - 1] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis, ownvertex.vertexYAxis - 1,
                                      grid[ownvertex.vertexXAxis][ownvertex.vertexYAxis - 1],1)
                if (grid[ownvertex.vertexXAxis-1][ownvertex.vertexYAxis] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis-1, ownvertex.vertexYAxis,
                                      grid[ownvertex.vertexXAxis-1 ][ownvertex.vertexYAxis],1)
                if (grid[ownvertex.vertexXAxis + 1][ownvertex.vertexYAxis] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis + 1, ownvertex.vertexYAxis,
                                      grid[ownvertex.vertexXAxis + 1][ownvertex.vertexYAxis],1)

            # Edges that have 4 neighbours
            else:
                if (grid[ownvertex.vertexXAxis][ownvertex.vertexYAxis - 1] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis, ownvertex.vertexYAxis - 1,
                                      grid[ownvertex.vertexXAxis][ownvertex.vertexYAxis - 1],1)
                if (grid[ownvertex.vertexXAxis - 1][ownvertex.vertexYAxis] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis - 1, ownvertex.vertexYAxis,
                                      grid[ownvertex.vertexXAxis - 1][ownvertex.vertexYAxis],1)
                if (grid[ownvertex.vertexXAxis ][ownvertex.vertexYAxis+1] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis , ownvertex.vertexYAxis+1,
                                      grid[ownvertex.vertexXAxis][ownvertex.vertexYAxis+1],1)
                if (grid[ownvertex.vertexXAxis + 1][ownvertex.vertexYAxis] != "Obstacle"):
                    owngraph.add_edge(src_number, ownvertex.vertexXAxis + 1, ownvertex.vertexYAxis,
                                      grid[ownvertex.vertexXAxis + 1][ownvertex.vertexYAxis],1)
        src_number += 1
    return owngraph

def GetStart(graph): #Function to get the start node
    for node in graph.graph:
        if (node.type == "Start"):
            return node

def GetFinish(graph): #Function to get the finish node
    for node in graph.graph:
        if (node.type == "End"):
            return node

def GetNodeIndex(graph, required_node): #Function to get the index of the required node in the graph list
    index = 0
    for node in graph.graph:
        if (node.vertexXAxis == required_node.vertexXAxis and node.vertexYAxis == required_node.vertexYAxis):
            return index
        index += 1

def heuristic(curr_node,child_node):  #Returns the heuristic manhattan cost to the final node from child node
    return abs(curr_node.vertexXAxis-child_node.vertexXAxis) + abs(curr_node.vertexYAxis-child_node.vertexYAxis)

def EdgeGetter(node, graph): #function to get all edges of a required node from graph
    edgeList = []
    for i in graph.graph:
        if (node.vertexXAxis == i.vertexXAxis and node.vertexYAxis == i.vertexYAxis):
            node = i
            break
    while node.next != None:
        edgeList.append(node.next)
        node = node.next
    return edgeList

def is_Two_Node_Equal(node_1,node_2):  #Calculates if given x and y vertex ids are equal to a nodes vertexes
    if(node_1[0]== node_2.vertexXAxis and node_1[1] == node_2.vertexYAxis):
        return True
    return False
def UCS(graph,start):
    start_node = start;
    finish_node = GetFinish(graph);
    que=[];
    que.append([start_node, 0, [(start_node.vertexYAxis, start_node.vertexXAxis)]]) #Add start node to priority queue
    explored = [] #List for explored nodes
    while(que):
        que = sorted(que, key=lambda element: (element[1]))  #convert que list to a priority queue what sorted w.r.t. costs
        #pop item from queue
        curr_node = que[0][0]
        curr_cost = que[0][1]
        curr_path = list(que[0][2])
        del que[0]
        # check if solution is reached
        if(is_Two_Node_Equal((curr_node.vertexXAxis,curr_node.vertexYAxis),finish_node)):
            return curr_path
        explored.append((curr_node.vertexXAxis,curr_node.vertexYAxis))
        for neighbour in EdgeGetter(curr_node,graph):
            if(neighbour.type != "Obstacle" ):
                is_in_explored = False
                is_in_queue = False
                current_que_cost = 0
                #check if child is in the explored list
                if (neighbour.vertexXAxis,neighbour.vertexYAxis) in explored:
                    is_in_explored = True
                neighbour_que_index = 0
                # check if child is in the queue and if child in queue gets its cost and index values
                for elements in que:
                    if(is_Two_Node_Equal((elements[0].vertexXAxis,elements[0].vertexYAxis),neighbour)):
                        current_que_cost = elements[1]
                        is_in_queue = True
                        break
                    neighbour_que_index += 1
                #set neighbours vlues for add it to queue
                new_cost = curr_cost + 1
                curr_path.append((neighbour.vertexYAxis,neighbour.vertexXAxis))
                ekle = list(curr_path) #to prevent changes in curr_path
                del curr_path[-1]
                #if neighbour is not visited yet and not in queue
                if (not is_in_queue) and (not is_in_explored):
                    que.append([neighbour, new_cost, ekle])
                # if neighbour is not visited yet but in queue with a higher cost
                elif current_que_cost > new_cost:
                    que[neighbour_que_index][1] = new_cost
                    que[neighbour_que_index][2] = ekle
    return None


def AStar(graph):
    start_node = GetStart(graph);
    finish_node = GetFinish(graph);
    que = [];
    #que[item][1] = UCS cost to node (h(x)), que[item][2] = heuristic_cost(g(x))
    que.append([start_node, 0, 0,[(start_node.vertexYAxis, start_node.vertexXAxis)]]) #add start node to proitiry queue
    explored = [] #list for visited nodes
    while que:
        # convert que list to a priority queue what sorted w.r.t. total costs (total_cost = h(x)+g(x))
        que = sorted(que, key=lambda element: (element[1]+element[2]))
        #pop item from queue
        curr_node = que[0][0]
        curr_UCS_cost = que[0][1]
        curr_heuristic_cost = que[0][2]
        curr_path = list(que[0][3])
        del que[0]
        if(curr_node.vertexXAxis== 1 and curr_node.vertexYAxis== 1):
            a=5
        # check if solution is reached
        if is_Two_Node_Equal((curr_node.vertexXAxis,curr_node.vertexYAxis),finish_node):
            return curr_path
        explored.append((curr_node.vertexXAxis, curr_node.vertexYAxis)) # add node to visited nodes list
        for neighbour in EdgeGetter(curr_node,graph):
            if (neighbour.type != "Obstacle"):
                is_in_explored = False
                is_in_queue = False
                current_que_total_cost = 0
                # gets the heuristic cost from popped node to its child
                next_heuristic_cost = heuristic(neighbour,finish_node)
                # check if child is in the explored list
                if (neighbour.vertexXAxis, neighbour.vertexYAxis) in explored:
                    is_in_explored = True
                neighbour_que_index = 0
                # check if child is in the queue and if child in queue gets its cost and index values
                for elements in que:
                    if (is_Two_Node_Equal((elements[0].vertexXAxis, elements[0].vertexYAxis), neighbour)):
                        current_que_total_cost = elements[1]+elements[2]
                        is_in_queue = True
                        break
                    neighbour_que_index += 1
                #calculate the new cost to this child with UCS cost and heuristic cost
                if (neighbour.type != "Start"):
                    if (neighbour.type != "End"):

                        new_heuristic_cost = next_heuristic_cost
                        new_UCS_Cost =  curr_UCS_cost + int(neighbour.type)
                    # if child node is end  node heuristic cost to reach child node from popped node is 0 ucs cost is old ucs+1
                    else:
                        new_heuristic_cost = next_heuristic_cost
                        new_UCS_Cost = curr_UCS_cost
                #if child node is start  node ucs cost is old ucs cost
                else :
                    new_heuristic_cost=next_heuristic_cost
                    new_UCS_Cost = curr_UCS_cost
                #set required values
                curr_path.append((neighbour.vertexYAxis, neighbour.vertexXAxis))
                ekle = list(curr_path)
                del curr_path[-1]
                # if node is not in queue and not visited yet add it to que direclty
                if (not is_in_queue) and (not is_in_explored):
                    que.append([neighbour, new_UCS_Cost,new_heuristic_cost, ekle])
                # if node is not queue and total cost in queue is greater than new total cost edit this que element with new cost and path
                elif is_in_queue and current_que_total_cost> (new_UCS_Cost+new_heuristic_cost):
                    que[neighbour_que_index][1] = new_UCS_Cost
                    que[neighbour_que_index][2] = new_heuristic_cost
                    que[neighbour_que_index][3] = ekle



    return None
def InformedSearch ( method_name , problem_file_name ):
    grid=getGrid(problem_file_name)
    graph=GraphCreater(grid)
    if method_name == "UCS":
        result = UCS(graph,GetStart(graph))
        result.reverse()
        return (result)
    elif method_name == "AStar":
        result = AStar(graph)
        result.reverse()
        return (result)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(InformedSearch("UCS", "testcaseUCS1.txt"))


