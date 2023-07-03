

visited_node_count: int=0
terminal_Condition =[]
node_count =0

class Parsed_Input:  # Class for keeping input as an array and a type max or min
    def __init__(self, array, type):
        self.game_arr = array
        self.type = type

class Node: #This class is the node class for tree nodes. It takes the parsed input and keeps the node's data, depth, childs as a array, minmax value as state
    def __init__(self, data,depth = 0):
        self.data = data
        self.next = []
        self.depth = depth
        self.state = 0
        self.processed = 0
class my_Tree: #Tree class to keep the game tree
    def __int__(self, data):
        self.node = Node(data)

    def initiate_tree(self,game,depth = 0):
        global node_count

        finish = True  # to decide continue or stop. It is false if all array elements are 0
        for i in range(0, len(game.game_arr)): #checks if it is an terminal node or not
            if(game.game_arr[i]!=0):
                finish = False
                break
        if(finish): #if terminal nodes return it
            node = Node(game.game_arr,depth)
            return node
        node = Node(game.game_arr,depth)
        node_count += 1
        node.next = []
        # generate the first order child
        for i in range(0, len(game.game_arr)): #loop through array length
            for j in range(0, game.game_arr[i]): # loop 0 to arrays element
                new_data= list(game.game_arr)
                old_data = new_data[i] # to keep the other elements unchanged store it.
                new_data[i] = j
                child_node = Node(new_data,depth+1)
                node.next.append(child_node)  # append the newly created node to tree
                game.game_arr[i] = old_data
        # loop through all the 1st generation childs and make iterative calls to them to create their childs.
        for i in range(len(node.next)):
            new_game = Parsed_Input(node.next[i].data,game.type)
            child = self.initiate_tree(new_game,depth+1)
            if(child):
                for j in range(len(child.next)):
                    node.next[i].next.append(child.next[j])

        return node
def parser(problem_file_name, type):
    try:
        # To parse the given input this function reads the given text file and takes the integer values and append them to game array.
        file = open(problem_file_name, 'r')
        rawinput = file.read().split("\n")
        game=Parsed_Input([],type)
        for index in range(1,len(rawinput[0])-1):
            if(rawinput[0][index] != ","):
                game.game_arr.append(int(rawinput[0][index]))
        return game
    except:
        print("Cannot open the file.")

def Minimax(game,node):
    if(game.type == "MAX"):
        temp= Max_Value(node,game) # temp is an array that contains the root node and roots max value
        result = ([temp[0].data,temp[0].processed])
    else:
        temp =Min_Value(node,game)  # temp is an array that contains the root node and roots min value
        result = ([temp[0].data, temp[0].processed])

    return result

def AlphaBeta(game, node):
    if (game.type == "MAX"):
        alpha = -10000
        beta = 10000
        temp = Max_Value_for_Alpha(node,alpha,beta,game) # temp is an array that contains the root node and roots max value
        result = ([temp[0].data, temp[0].processed])
    else:
        temp = Min_Value(node, game) # temp is an array that contains the root node and roots min value
    result = ([temp[0].data, temp[0].processed])
    return result


def Max_Value(node, game):
    global visited_node_count
    if(terminal_Condition == node.data): # if node is terminal node([0*game arrays length] array)
        if(node.depth % 2 == 0):  # if opponents turn assign 1 to node
            node.state = 1
            return [node, 1]
        else:                     # if our turn assign -1 to node
            node.state = -1
            return [node, -1]
    
        
    v = -10000
    visited_node_count += 1
    next_node = None
    for i in range(len(node.next)): #for all the childs of node
        temp_tuple =Min_Value(node.next[i],game)   # Call Min value function with child  since it will be opponents turn
        old_v = v
        v = max(v,temp_tuple[1])
        node.processed += (1+node.next[i].processed)
        if(next_node):     # if it is not the first child that has a winning opportunity
            if (v >= old_v and (next_node.processed > temp_tuple[0].processed or next_node.state<temp_tuple[0].state)):  # if  max value of child is bigger than older and childs proccess count is lower than older one
                next_node= node.next[i] #assign the cild node to find the winning state
        elif(v >= old_v ): # if it is the first child that has a winning opportunity
            next_node = node.next[i]
        if (node.depth == 0 and next_node.state == 1): # if a winnable state is found return
            node.state = v
            return [next_node, node.state]
    node.state = v


    return [next_node, node.state]
    
def Min_Value(node, game):

    # work exacly as opposit of the Max_Value() function
    global visited_node_count
    if (terminal_Condition == node.data):
        if (node.depth % 2 == 0):
            node.state = 1
            return [node,node.state]
        else:
            node.state = -1
            return [node,node.state]
    v = 10000
    for i in range(len(node.next)):
        temp_tupe= Max_Value(node.next[i], game)
        old_v = v
        v = min(v,temp_tupe[1])
        node.processed += (1+node.next[i].processed)
    node.state = v

    return [node,node.state]

def Max_Value_for_Alpha(node, alpha, beta, game):
    #works as Max_Value() function but with beta value it does not calculate unneccessary child.
    if (terminal_Condition == node.data):
        if (node.depth % 2 == 0):
            node.state = 1
            return [node, 1]
        else:
            node.state = -1
            return [node, -1]
    v = -10000
    next_node = None
    for i in range(len(node.next)):
        temp_tuple = Min_Value_for_Beta(node.next[i], alpha, beta, game)
        old_v = v
        v = max(v, temp_tuple[1])
        if (v >= beta):
            next_node = node.next[i]
            node.state = v
            node.processed += (1 + node.next[i].processed)
            return [next_node,node.state]
        if (next_node):
            if (v >= old_v and (
                    next_node.processed > temp_tuple[0].processed or next_node.state < temp_tuple[0].state)):
                next_node = node.next[i]
        elif (v >= old_v):
            next_node = node.next[i]
        alpha = max(alpha, v)
        node.processed += (1 + node.next[i].processed)
        if (node.depth == 0 and next_node.state == 1):
            node.state = v
            return [next_node, node.state]
    node.state = v

    return [next_node, node.state]
def Min_Value_for_Beta(node, alpha, beta, game):
    # works as opposite of Max_Value_for_Alpha() function but it eleminates unneccessary child with help of alpha.
    if node.data == [1,3,2]:
        a=5
    if (terminal_Condition == node.data):
        if (node.depth % 2 == 0):
            node.state = 1
            return [node, 1]
        else:
            node.state = -1
            return [node, -1]
    v = 10000
    for i in range(len(node.next)):
        temp_tuple = Max_Value_for_Alpha(node.next[i], alpha, beta, game)
        v = min(v, temp_tuple[1])
        if (v <= alpha):
            node.state= v
            node.processed += (1 + node.next[i].processed)
            return [node,node.state]
        beta = min(beta, v)
        node.processed += (1 + node.next[i].processed)
    node.state = v

    return [node, node.state]
def SolveGame ( method_name , problem_file_name , player_type ):
    game = parser(problem_file_name,player_type) #parse input and take game array
    #create game tree
    tree = my_Tree()
    tree = tree.initiate_tree(game)
    global terminal_Condition
    #calculate terminal condition to use functions
    terminal_Condition = [0]* len(game.game_arr)

    #call the rigth methode which is required in input
    if method_name == "Minimax":
        result = Minimax(game, tree)
        return result

    elif method_name == "AlphaBeta":
        result = AlphaBeta(game , tree)
        return result
