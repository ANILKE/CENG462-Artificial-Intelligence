from queue import PriorityQueue
from traceback import print_tb
from turtle import st

mincustomer = 0
vertice_count = 0


class AdjList:  # Class for keeping adjacency list:
    def __init__(self, xAxis, yAxis, name):
        self.vertexXAxis = xAxis  # X-axis of the adjacent node
        self.vertexYAxis = yAxis  # Y-axis of the adjacent node
        self.type = name
        self.before=None
        self.next = None  # Next node


class Graph:
    def __init__(self, vertices, grid):

        self.V = vertices  # Vertex Number
        self.graph = []
        for i in range(len(grid)):
            for j in range(len(grid)):
                if (grid[i][j] == "Start" or grid[i][j] == "Finish" or grid[i][j] == "Customer"):
                    self.graph.append(AdjList(i, j, grid[i][j]))
        # Adjacency List

    # Function to add an edge in an undirected graph
    def add_edge(self, src_num, destx, desty, dest_type):  # Function to add new edges
        # Adding the dest node to the source node
        node = AdjList(destx, desty, dest_type)
        node.next = None
        oldnode = self.graph[src_num]
        while oldnode != None:
            addhere = oldnode
            oldnode = oldnode.next
        addhere.next = node

    def print_graph(self):
        for i in range(9):

            print("Adjacency list of vertexX {} ".format(i), end="")
            temp = self.graph[i]
            while temp:
                print(" -> {}".format(temp.vertexXAxis), end="")
                print(" + {}".format(temp.vertexYAxis), end="")
                print(" + {}".format(temp.type), end="")
                temp = temp.next
            print(" \n")

graph =Graph(0, [])
def GetGrid(problem_file_name):  # Duzelt
    try:
        global mincustomer
        global vertice_count
        locations = {0: 'Start', 1: 'Finish', 2: 'Customer', 3: 'Empty'}
        file = open(problem_file_name, 'r')
        rawinput = file.read().split("\n")
        digitsplus = rawinput[0].split(":")[1]
        digits = digitsplus.split(",")[0]
        digits = digits[1:]
        mincustomer = int(digits)
        rawinput = rawinput[0].split("'")

        rowcount = 0
        file.close()

        for i in rawinput:
            if i[0] == "." or i[0] == "C" or i[0] == "S" or i[0] == "F":
                rowcount += 1

        grid = [[locations[3]] * rowcount for i in range(rowcount)]

        row = 0
        for inputrows in rawinput:
            if (inputrows[0] == "]"):
                break
            else:
                if inputrows[0] == "." or inputrows[0] == "C" or inputrows[0] == "S" or inputrows[0] == "F":
                    for column in range(0, rowcount):
                        if inputrows[column] == '.':
                            grid[row][column] = locations[3]

                        elif inputrows[column] == 'C':
                            vertice_count += 1
                            grid[row][column] = locations[2]

                        elif inputrows[column] == 'F':
                            vertice_count += 1
                            grid[row][column] = locations[1]

                        elif inputrows[column] == 'S':
                            vertice_count += 1
                            grid[row][column] = locations[0]

                    row += 1

        return grid
    except:
        print("Cannot Open File")


def GraphCreater(grid):
    global vertice_count
    owngraph = Graph(vertice_count, grid)

    src_number = 0

    for ownvertex in owngraph.graph:
        if (ownvertex.type != "Finish"):
            for i in range(0, len(grid)):
                for j in range(0, len(grid)):
                    if (grid[i][j] == "Finish" or grid[i][j] == "Customer"):
                        if i == ownvertex.vertexXAxis and j == ownvertex.vertexYAxis:
                            continue
                        else:
                            owngraph.add_edge(src_number, i, j, grid[i][j])
        src_number += 1
    return owngraph


def GetStart(graph):
    for node in graph.graph:
        if (node.type == "Start"):
            return node


def GetFinish(graph):
    for node in graph.graph:
        if (node.type == "Finish"):
            return node


def GetNodeIndex(graph, required_node):
    index = 0
    for node in graph.graph:
        if (node.vertexXAxis == required_node.vertexXAxis and node.vertexYAxis == required_node.vertexYAxis):
            return index
        index += 1


def EdgeGetter(node):
    edgeList = []
    while node.next != None:
        edgeList.append(node.next)
        node = node.next
    return edgeList


def GetCost(node1, node2):
    return abs(node1.vertexXAxis - node2.vertexXAxis) + abs(node1.vertexYAxis - node2.vertexYAxis)


def BFS(graph):
    global mincustomer
    finalList = [(0, 0)] * (mincustomer + 2)
    visited = [False] * (graph.V)
    queue = []

    startNode = GetStart(graph)
    startIndex = GetNodeIndex(graph, startNode)
    finishNode = GetFinish(graph)

    queue.append(startNode)
    visited[startIndex] = True

    finalList[-1] = (finishNode.vertexXAxis, finishNode.vertexYAxis)
    final_list_index = 0
    if (mincustomer > (graph.V - 2)):
        return None
    elif (mincustomer == 0):
        finalList[0] = (startNode.vertexXAxis, startNode.vertexYAxis)
        return finalList
    while queue:
        s = queue.pop(0)
        finalList[final_list_index] = (s.vertexXAxis, s.vertexYAxis)
        final_list_index += 1
        if (final_list_index == mincustomer + 1):
            break

        for i in EdgeGetter(graph.graph[GetNodeIndex(graph, s)]):
            if (i.type != "Finish"):
                iIndex = GetNodeIndex(graph, i)
                if visited[iIndex] == False:
                    queue.append(i)
                    visited[iIndex] = True

    return finalList


def DFSRec(graph, node, visited, finalList, listIndex):
    finalList[listIndex] = (node.vertexXAxis, node.vertexYAxis)
    if (listIndex == (mincustomer)):
        return
    for neighbour in EdgeGetter(graph.graph[GetNodeIndex(graph, node)]):
        if (neighbour.vertexXAxis, neighbour.vertexYAxis) not in visited:
            DFSRec(graph, neighbour, visited, finalList, listIndex + 1)


def DFS(graph):
    finishNode = GetFinish(graph)
    startNode = GetStart(graph)
    finalList = [(0, 0)] * (mincustomer + 2)
    finalList[-1] = (finishNode.vertexXAxis, finishNode.vertexYAxis)
    if (mincustomer > (graph.V - 2)):
        return None
    elif (mincustomer == 0):
        finalList[0] = (startNode.vertexXAxis, startNode.vertexYAxis)
        return finalList
    visited = set()
    startNode = GetStart(graph)
    DFSRec(graph, startNode, visited, finalList, 0)
    return finalList


def UCS():
    global graph
    global mincustomer
    finalList = [(0, 0)] * (mincustomer + 2)
    visited = [[False] * (graph.V) for i in range(graph.V)]
    cost = [9223372036854775807] * (graph.V)
    node = GetStart(graph)
    node_index = GetNodeIndex(graph, node)
    cost[node_index] = 0
    que = [(0, node)]
    if mincustomer > (graph.V - 2):
        return None
    startNode = GetStart(graph)
    finishNode = GetFinish(graph)

    finalList[-1] = (finishNode.vertexXAxis, finishNode.vertexYAxis)
    if (mincustomer == 0):
        finalList[0] = (startNode.vertexXAxis, startNode.vertexYAxis)
        return finalList
    count=0
    while (len(que) > 0):
        que = sorted(que, key=lambda tup: tup[0])
        queue_element=que.pop(0)
        nodescost=queue_element[0]
        node = queue_element[1]
        node_index=GetNodeIndex(graph,node)
        if node.vertexXAxis == finishNode.vertexXAxis and node.vertexYAxis==finishNode.vertexYAxis:
            if cost[GetNodeIndex(graph,node)]>=nodescost and GetBeforeCount(node)==mincustomer+1:
                cost[GetNodeIndex(graph,node)]=nodescost
            else:
                for i in (graph.V):
                    if(graph.graph[i] not in GetBefors(node)):
                        visited[i]=False
            continue

        if (visited[node_index] == False):
            for neighbour in EdgeGetter(graph.graph[GetNodeIndex(graph, node)]):
                newcost=GetCost(node,neighbour)
                graph.graph[GetNodeIndex(graph,neighbour)].before=node
                neighbour.before = node
                que.append((nodescost+newcost,neighbour))
        visited[node_index]=True


    return cost
def GetBefors(node):
    list=[]
    while node:
        list.append(node)
        node=node.before
    return list
def GetBeforeCount(node):
    count=0
    node=node.before
    while node:
        count+=1
        node = node.before
    return count
def UnInformedSearch(method_name, problem_file_name):
    global mincustomer
    global graph
    locations = {0: 'Start', 1: 'Finish', 2: 'Customer', 3: 'Empty'}
    grid = GetGrid(problem_file_name)
    graph = GraphCreater(grid)
    graph.print_graph
    if method_name == "BFS":
        result = BFS(graph)
        return (result)
    elif method_name == "DFS":
        result = DFS(graph)
        return (result)
    elif method_name == "UCS":
        result = UCS()
        return (result)
if __name__ == '__main__':
    print(UnInformedSearch("UCS", "sampleproblem2.txt"))
