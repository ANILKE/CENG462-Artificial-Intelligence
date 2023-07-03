import copy
import random

# Since query2 gives reversed result in gibbs, I wrote the nearest function to check if the result is in the correct form


class Node: #that takes bayesian network variables with their name, table, parents, childeren,
    def __init__(self,variable,values = {},parents = [],childs=[],childs_parents = []):
        self.variable = variable
        self.values = values
        self.parents = parents
        self.childs = childs
        self.childs_parents= childs_parents
class BayesNet: #that takes the variable nodes.In query section query node and evidences
    def __init__(self,query =[]):
        self.variables = []
        self.query = query

    def add_variable(self, name): #after parse varible lines create variable in BayesNet
        variable = Node(name, {},[],[],[])
        self.variables.append(variable)
    def set_parents(self,name,parents): #after parse parents lines create parents in BayesNet
        if(name != -1):
            for i in range(len(parents)):
                self.variables[name].parents.append(parents[i])
    def set_values(self,name,values): #after parse table lines create table in BayesNet
        if (name != -1):

            self.variables[name].values = values

    def get_node_idx(self,node_name): # to fi,nd the given varible name's in bayesnet variable list
        for i in range(len(self.variables)):
            if(self.variables[i].variable==node_name):
                return i
        return -1
    def add_chils(self): #after parse relations lines create child array in BayesNet
        for i in range(len(self.variables)):
            curr_var = self.variables[i].variable
            for j in range(len(self.variables)):
                if(i !=j):
                    if(curr_var in self.variables[j].parents):
                        self.variables[i].childs.append(self.variables[j])
    def convert_parents_to_node(self):
        for i in range(len(self.variables)):
            parents_list = list(self.variables[i].parents)
            self.variables[i].parents = []
            for j in range(len(parents_list)):
                self.variables[i].parents.append(self.variables[self.get_node_idx(parents_list[j])])

    def sort(self): #Topologic sort
        for i in range(len(self.variables)-1):
            for j in range(i+1,len(self.variables)):
                if(self.variables[j] in self.variables[i].parents):
                    get = self.variables[i], self.variables[j]

                    # unpacking those elements
                    self.variables[j], self.variables[i] = get
    def set_childs_parents(self):
        for i in range(len(self.variables)):
            for j in range(len(self.variables[i].childs)):
                for k in range(len(self.variables[i].childs[j].parents)):
                    if(self.variables[i].childs[j].parents[k] != self.variables[i]):
                        self.variables[i].childs_parents.append(self.variables[i].childs[j].parents[k])
def sqr(i): # to find the values number (for example for 1 parent 2 values true and false)
    result = 1
    for j in range(i):
        result *= 2
    return result
def parser(problem_file_name): #parsees the given input txt line by line and constructs the bayesnet
    file = open(problem_file_name, 'r')
    lines = file.read().split("\n")
    bn = BayesNet([])
    value = 1
    bn.variables = []
    for i in range(1,len(lines)): #takes the variable names and create node and bayes net variables.
        if(lines[i] !='[Paths]'):
            bn.add_variable(lines[i])
        else:
            value += 1
            break
        value += 1
    temp_value = value
    parents = []
    for i in range(temp_value,len(lines)): #takes the paths and create path in variable node in bayesnet.
        if(lines[i] != '[ProbabilityTable]'):
            splited = lines[i].split("'")
            for j in range(len(splited)):
                if("A"<=splited[j][0]<="Z"):
                    parents.append(splited[j])
                elif(splited[j][0]== "]"):
                    node_name = lines[i].split("'")[-2]
                    index = bn.get_node_idx(node_name)
                    bn.set_parents(index,parents)
                    parents = []
                    break
        else:
            value +=1
            break
        value +=1
    temp_value =value

    probabilities = {}
    for i in range(temp_value, len(lines)): #takes the prob table and create probtable in variable node in bayesnet.
        if (lines[i] != '[Query]'):
            name = lines[i].split("'")[1]
            index = bn.get_node_idx(name)
            probs = lines[i].split(".")
            for j in range(sqr(len(bn.variables[index].parents))):
                if(probs[-j-2] and probs[-j-2][-1] == '1'):
                    str_prob ="1."
                else:
                    str_prob = "0."
                for k in range(len(probs[-j-1])):
                    if probs[-j-1][k]!="," and probs[-j-1][k]!="}":
                        str_prob +=  probs[-j-1][k]
                    else:
                        break
                if(bn.variables[index].parents == []):
                    probabilities['True'] = float(str_prob)
                else:
                    i=0
                    sonuc = ''
                    while i <len(probs[-j-2]):
                        if(probs[-j-2][i:i+2] =='Tr' or probs[-j-2][i:i+2] =='Fa'):
                            t= i
                            while(probs[-j-2][t] != ":" and probs[-j-2][t] != ")"):
                                sonuc += probs[-j-2][t]
                                t += 1
                            break
                        i += 1
                    probabilities[sonuc] = float(str_prob)
            bn.set_values(index,probabilities)
            probabilities = {}

        else:
            value += 1
            break
        value += 1

    # creates bayesnet's query
    bn.query.append(bn.variables[bn.get_node_idx(lines[-1].split(",")[0][2:-1])])
    bn.query.append({})
    splited_query = lines[-1].split(",")[1:]
    for i in range(len(splited_query)):
        curr_query = str(splited_query[i][2:]).split(":")
        if(i == 0):
            bn.query[1][curr_query[0][1:-1]] = curr_query[1][1:]
        elif(i==len(splited_query)-1):
            bn.query[1][curr_query[0][:-1]] = curr_query[1][1:-2]
        else:
            bn.query[1][curr_query[0][:-1]] = curr_query[1][1:-1]



    return bn

def enumeration_ask(bn):
    #creates evidence set
    evidence = {}
    for i in range(len(bn.query[1])):
        evidence[list(bn.query[1].keys())[i]] = list(bn.query[1].values())[i]
    # ccalculates for true and false values of query variable
    for x_i in range(2):
        if(x_i ==0):
            deep_copied_ev = copy.deepcopy(evidence)
            deep_copied_ev[bn.query[0].variable] ="True"
            true_val = (enumerete_all(bn, bn.variables, deep_copied_ev))
        else:
            deep_copied_ev = copy.deepcopy(evidence)
            deep_copied_ev[bn.query[0].variable] = "False"
            false_val = (enumerete_all(bn, bn.variables, deep_copied_ev))
            if(true_val == 0 and false_val == 0):
                false_val = 1.0
    #normalize result
    total = true_val + false_val
    true_val /= total
    false_val /= total
    return (round(true_val,3),round(false_val,3))

def enumerete_all(bn,vars,e):
    #if no vars return directly 1
    if(len(vars) == 0 or vars[0].values == {}):
        return 1
    curr_node = vars[0]
    #if current node is  in evidences
    if(curr_node.variable in list(e.keys())):
        # if node has no parent return directly its value
        if(len(curr_node.parents) == 0):
            #if value in evidences is true return prob value
            if(e[curr_node.variable] == 'True'):
                result_1 = curr_node.values['True']
            # if value in evidences is false return 1 - prob value
            else:
                result_1 = round(1 - curr_node.values['True'],3)
        # if node has no parents
        else:
            #calculate conditions of its parents in evidence set (true or false in order)
            parensts_bools = ''
            for i in range(len(curr_node.parents)):
                temp = e[curr_node.parents[i].variable]
                if (i != 0):
                    parensts_bools += ','
                if (i == len(curr_node.parents) - 1 and len(curr_node.parents) != 1 ):
                    parensts_bools += ' '
                if (temp == 'True'):
                    parensts_bools += 'True'
                else:
                    parensts_bools += 'False'
            #return probability value directly from parents sequance
            result_1 = curr_node.values[parensts_bools]
        return result_1 * enumerete_all(bn,vars[1:],e)
    # if current node is not in evidences
    else:
        #creat bot true and false conditions and calculate both in same manner with upper calculations
        result = 0
        e_new1 = copy.deepcopy(e)
        e_new1[curr_node.variable] = 'True'
        e_new2 = copy.deepcopy(e)
        e_new2[curr_node.variable] = 'False'
        if (len(curr_node.parents) == 0):
            try:
                result1 = curr_node.values['True']
            except:
                result1 = 0
        else:
            parensts_bools = ''
            for i in range(len(curr_node.parents)):
                temp = e[curr_node.parents[i].variable]
                if (i != 0):
                    parensts_bools += ','
                if (i == len(curr_node.parents) - 1 and len(curr_node.parents) != 1 ):
                    parensts_bools += ' '
                if (temp == 'True'):
                    parensts_bools += 'True'
                else:
                    parensts_bools += 'False'
            result1 = curr_node.values[parensts_bools]
        result+= result1 * enumerete_all(bn,vars[1:],e_new1)
        if (len(curr_node.parents) == 0):
            try:
                result1 = round(1-curr_node.values['True'],3)
            except:
                result1 = 1
        else:
            parensts_bools = ''
            for i in range(len(curr_node.parents)):
                temp =e.get(curr_node.parents[i].variable)
                if (i != 0):
                    parensts_bools += ','
                if (i == len(curr_node.parents) - 1 and len(curr_node.parents) != 1 ):
                    parensts_bools += ' '
                if(temp=='True'):
                    parensts_bools += 'True'
                else:
                    parensts_bools += 'False'
            result1 = round(1 - curr_node.values[parensts_bools],3)
        result += result1 * enumerete_all(bn,vars[1:],e_new2)
        return result


def calculate_P_for_main_node(curr_node,x):
    #if value at x is true
    if(x[curr_node.variable] == 'True'):
        # if node has no parent return directly its value
        if (len(curr_node.parents) == 0 ):
            try:
                result1 = round(curr_node.values['True'], 3)
            except:
                result1 = 0
        # if node has no parents
        else:
            # calculate conditions of its parents in evidence set (true or false in order)
            parensts_bools = ''
            for i in range(len(curr_node.parents)):
                temp = x.get(curr_node.parents[i].variable)
                if (i != 0):
                    parensts_bools += ','
                if (i == len(curr_node.parents) - 1 and len(curr_node.parents) != 1 ):
                    parensts_bools += ' '
                if (temp == 'True'):
                    parensts_bools += 'True'
                else:
                    parensts_bools += 'False'
            # return probability value directly from parents sequance
            result1 = round(curr_node.values[parensts_bools], 3)
    # if value at x is false return 1- value in prob table
    else:
        if (len(curr_node.parents) == 0):
            try:
                result1 = round(1 - curr_node.values['True'], 3)
            except:
                result1 = 1
        else:
            parensts_bools = ''
            for i in range(len(curr_node.parents)):
                temp = x.get(curr_node.parents[i].variable)
                if (i != 0):
                    parensts_bools += ','
                if (i == len(curr_node.parents) - 1 and len(curr_node.parents) != 1 ):
                    parensts_bools += ' '
                if (temp == 'True'):
                    parensts_bools += 'True'
                else:
                    parensts_bools += 'False'
            result1 = round(1- curr_node.values[parensts_bools], 3)
    return result1
def calculate_P_for_childs_of_nodes(childs,x):
    #for all chils of current node calculate prob directly
    result = 1
    for i in range(len(childs)):
        result *= calculate_P_for_main_node(childs[i],x)
    return result
def calculate_markov_blanket(x_prime_i,x):
    #crete chils of current node and call calculation functions
    childs = x_prime_i.childs
    result = calculate_P_for_main_node(x_prime_i,x) * calculate_P_for_childs_of_nodes(childs,x)
    return result
def gibbs_ask(query_var,bn, evidence, N, num_iteration):
    #create nonevidence set
    Z= []
    for i in range(len(bn.variables)):
        if (bn.variables[i].variable not in evidence.keys()):
            Z.append(bn.variables[i].variable)
    # create x
    x={}
    random.seed(10)
    # for nonevidence nodes random values assign to x set
    for element in Z:
        x[element] = str(random.choice([True,False]))
    #for evidence certain values append to x
    for elements in evidence.keys():
        x[elements] = evidence[elements]

    # through iteretion number
    for i in range(num_iteration):
        # for each nonevidence variable
        for z_i in Z:
            #take variable as a node
            x_prime_i = bn.variables[bn.get_node_idx(z_i)]
            #calculate z_i markov blanket for current boolean value in x
            markov_old = calculate_markov_blanket(x_prime_i,x)
            x_copy = copy.copy(x)
            if (x[z_i] == 'True'):
                x_copy[z_i] = 'False'
            else:
                x_copy[z_i] = 'True'

            # calculate z_i markov blanket for opposite boolean value in x
            markov_new = calculate_markov_blanket(x_prime_i,x_copy)
            markov_normalizer = markov_old + markov_new
            #normalize markov blanket values
            markov_old /= markov_normalizer
            markov_new /= markov_normalizer
            #select true one
            if(x[z_i] == 'True'):
                final_markov = markov_old
            else:
                final_markov = markov_new
            #assing z_i boolean value accordin to random.random value
            if(final_markov > random.random()):
               x[z_i] = 'True'
            else:
               x[z_i] = 'False'
            #assign query variables boolean value to result
            if (x[query_var.variable] == 'True'):
                N[0] += 1
            elif(x[query_var.variable] == 'False'):
                N[1] += 1
    #normalize result
    total = N[0] + N[1]
    if(total != 0):
        N[0] /= total
        N[1] /= total

    return (N[0],N[1])

def nearest(a,b):
    #function to rearrange result if it is reverse
    diff1 = abs(a[0] - b[0])
    diff2 = abs(a[0] - b[1])
    if(diff2<diff1):
        return (a[1],a[0])
    return a

def DoInference(methode_name, problem_file_name ,num_iteration):
    #parse the given input and create according bayesnet and assign nodes values to proper nodes.
    bn = None
    bn = parser(problem_file_name)
    bn.add_chils()
    bn.convert_parents_to_node()
    bn.sort()
    bn.set_childs_parents()
    #call proper functions
    if(methode_name == "ENUMERATION"):
        result = enumeration_ask(bn)
        return result
    # call proper functions
    if (methode_name == "GIBBS"):
        #create evidence set from bayesnets query variable
        evidence = {}
        for i in range(len(bn.query[1])):
            evidence[list(bn.query[1].keys())[i]] = list(bn.query[1].values())[i]
        query_var=bn.query[0]
        # create result array with 0 initial values
        N = [0,0]
        result1 = gibbs_ask(query_var,bn,evidence,N,num_iteration)
        result2 = enumeration_ask(bn)

        #to aviod reverse results compare results and arrange required result
        result = nearest(result1,result2)
        return result

if __name__ == '__main__':
    print(DoInference("GIBBS","query1.txt",200))