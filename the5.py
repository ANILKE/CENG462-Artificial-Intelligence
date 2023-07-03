import copy
import random

class GameTable: #that includes current board, current player symbol, starting player symbol as starter, possible actions indexes in board and possible action number
    def __init__(self,starter,player):
        self.table = '---------'
        self.starter = starter
        self.actions = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
        self.number_of_poss_actions = 9
        self.player = player

    def get_reward(self):
        # calculates if the x wins the game or not and returns corresponding  reward values
        if (self.player == 'X'):
            opponent = 'O'
        else:
            opponent = 'X'

        if ( self.table[0] == self.player and  self.table[1] == self.player and  self.table[2] == self.player) or \
                ( self.table[3] == self.player and  self.table[4] == self.player and  self.table[5] == self.player) or \
                ( self.table[6] == self.player and  self.table[7] == self.player and  self.table[8] == self.player) or \
                ( self.table[0] == self.player and  self.table[3] == self.player and  self.table[6] == self.player) or \
                ( self.table[1] == self.player and  self.table[4] == self.player and  self.table[7] == self.player) or \
                ( self.table[2] == self.player and  self.table[5] == self.player and  self.table[8] == self.player) or \
                ( self.table[0] == self.player and  self.table[4] == self.player and  self.table[8] == self.player) or \
                ( self.table[2] == self.player and  self.table[4] == self.player and  self.table[6] == self.player):
            return 1

        elif ( self.table[0] == opponent and  self.table[1] == opponent and  self.table[2] == opponent) or \
                ( self.table[3] == opponent and  self.table[4] == opponent and  self.table[5] == opponent) or \
                ( self.table[6] == opponent and  self.table[7] == opponent and  self.table[8] == opponent) or \
                ( self.table[0] == opponent and  self.table[3] == opponent and  self.table[6] == opponent) or \
                ( self.table[1] == opponent and  self.table[4] == opponent and  self.table[7] == opponent) or \
                ( self.table[2] == opponent and  self.table[5] == opponent and  self.table[8] == opponent) or \
                ( self.table[0] == opponent and  self.table[4] == opponent and  self.table[8] == opponent) or \
                ( self.table[2] == opponent and  self.table[4] == opponent and  self.table[6] == opponent):
            return -1
        elif('-' in self.table):
            return 15
        else:
            return 0
    def remove_action(self,index):
        #removes the taken actions from array
        self.actions.remove(index)
        self.number_of_poss_actions -=1


def parser(problem_file_name):
    #get the inputs and convert to a dict
    result = {}
    file = open(problem_file_name, 'r')
    lines = file.read().split("\n")
    result['alpha'] = float(lines[1])
    result['gamma'] = float(lines[3])
    result['epsilon'] = float(lines[5])
    result['episode_count'] = int(lines[7])
    return result

def is_in_the_table(condition):
    #check if game is finished or not finished
    if (condition[0] == 'X' and condition[1] == 'X' and condition[2] == 'X') or \
            (condition[3] == 'X' and condition[4] == 'X' and condition[5] == 'X') or \
            (condition[6] == 'X' and condition[7] == 'X' and condition[8] == 'X') or \
            (condition[0] == 'X' and condition[3] == 'X' and condition[6] == 'X') or \
            (condition[1] == 'X' and condition[4] == 'X' and condition[7] == 'X') or \
            (condition[2] == 'X' and condition[5] == 'X' and condition[8] == 'X') or \
            (condition[0] == 'X' and condition[4] == 'X' and condition[8] == 'X') or \
            (condition[2] == 'X' and condition[4] == 'X' and condition[6] == 'X'):
        return False

    elif (condition[0] == 'O' and condition[1] == 'O' and condition[2] == 'O') or \
            (condition[3] == 'O' and condition[4] == 'O' and condition[5] == 'O') or \
            (condition[6] == 'O' and condition[7] == 'O' and condition[8] == 'O') or \
            (condition[0] == 'O' and condition[3] == 'O' and condition[6] == 'O') or \
            (condition[1] == 'O' and condition[4] == 'O' and condition[7] == 'O') or \
            (condition[2] == 'O' and condition[5] == 'O' and condition[8] == 'O') or \
            (condition[0] == 'O' and condition[4] == 'O' and condition[8] == 'O') or \
            (condition[2] == 'O' and condition[4] == 'O' and condition[6] == 'O'):
        return False
    elif ('-' in condition):
        return True
    else:
        return False
def appropiritate_x_o(curr):
    # calculates if X's and O's are balanced in the game board(game continues normally w,th appropriate moves)
    o_count = 0
    x_count = 0
    for i in range(9):
        if(curr[i]=='X'):
            x_count += 1
        if (curr[i] == 'O'):
            o_count += 1
    if(o_count == x_count or o_count == (x_count-1) or (o_count == x_count+1)):
        return True
    else:
        return False
def init_q_table(starter,player):
    result = {}
    #create the dict key values
    for i in range(3):
        for j in range(3):
            result[(i, j)] = {}

    symbols = ['-','X','O']
    curr_symbol = ['-','-','-','-','-','-','-','-','-']
    cur_condition = ['-','-','-','-','-','-','-','-','-']
    #loop through all board indexes and set each one to - X or O and continue
    for i in result:
        i_index_value = i[0] * 3 + i[1]
        curr_symbol[0] = '-'
        for var_0 in range(3):
            curr_symbol[1] = symbols[var_0]
            for var_1 in range(3):
                curr_symbol[2] = symbols[var_1]
                for var_2 in range(3):
                    curr_symbol[3] = symbols[var_2]
                    for var_3 in range(3):
                        curr_symbol[4] = symbols[var_3]
                        for var_4 in range(3):
                            curr_symbol[5] = symbols[var_4]
                            for var_5 in range(3):
                                curr_symbol[6] = symbols[var_5]
                                for var_6 in range(3):
                                    curr_symbol[7] = symbols[var_6]
                                    for var_7 in range(3):
                                        curr_symbol[8] = symbols[var_7]
                                        for j in range(i_index_value,i_index_value+9):
                                            cur_condition[ j%9 ] = curr_symbol[j-i_index_value]

                                        # if current board state is game done or board includes unbalanced X's and O's do not add this state to q_table

                                        if(is_in_the_table(cur_condition) and appropiritate_x_o(cur_condition)):
                                            new_str = ''
                                            for kel in range(9):
                                                new_str += cur_condition[kel]
                                            result[i][new_str] = 0.0

    return result

def select_action(game_board,epsilon,q_table,seed_val,flag):
    # Epsilon-Greedy Strategy.
    if random.random() <= epsilon:
        #if more than 1 possible actions select randomly
        if( len(game_board.actions) - 1 >0):
            action = random.randint(0, len(game_board.actions) - 1)
            selected_action = game_board.actions[action]
            # check if it is sars's next action if it is do not remove the action otherwise remove the action from possible actions array
            if(flag == 1):
                game_board.remove_action(selected_action)
        #if only 1 action left select it
        else:
            action = 0
            selected_action = game_board.actions[action]
            # check if it is sars's next action if it is do not remove the action otherwise remove the action from possible actions array
            if (flag == 1):
                game_board.remove_action(selected_action)
    # Actual Q learning algorithm.
    # Find the best action.
    else:
        value_max = -10000
        next_act = (0,0)
        #loop through all the possible
        for act in game_board.actions:
            # next_table = game_board.table
            # next_table = next_table[:(act[0]*3+act[1])] + game_board.player + next_table[(act[0]*3+act[1])+1:]

            #if q_table value of boards in this action is bigger set it
            if(q_table[act][game_board.table]> value_max):
                value_max = q_table[act][game_board.table]
                next_act = act
        selected_action = next_act
        #check if it is sars's next action if it is do not remove the action otherwise remove the action from possible actions array
        if (flag == 1):
            game_board.remove_action(next_act)
    return selected_action

def take_action( game, a ):
    #set the game board according to taken action
    s = game.table
    player = game.player
    # Place the player's symbol on the board at the chosen position
    s = s[:(a[0] * 3 + a[1])] + player + s[(a[0] * 3 + a[1]) + 1:]
    game.table = s
    # Determine the reward for the action
    old_player = game.player
    game.player = 'X'
    reward = game.get_reward()
    game.player = old_player
    # Return the reward and the next state
    return reward, s

def find_a_max(q,s,a):
    #find the max valued action from q_table
    result =(0,0)
    max_val = -10000
    #check if board is in action in q_table
    try:
        for act in q:
            if(q[act][s] > max_val):
                max_val = q[act][s]
                result = act
    # if board is not in action in q_table simply pass
    except:
        pass
    if max_val == -10000:
        max_val = 0
    if(max_val != 0):
        asda =6
    return result, max_val


def get_action_value(board, a, q_table):
    s = board.table

    return q_table[a][s]
def sarsa(inputs, random_seed, q_table, game_board):
    # select the action
    a = select_action(game_board, inputs['epsilon'], q_table, random_seed,1)
    #calculate reward and next board
    reward, next_s = take_action(copy.copy(game_board), a)
    #if game continues set reward to 0
    if (reward == 15):
        reward = 0
    # if game is finished do not take the next actions value and set the q_table values and board state and return
    else:
        q_table[a][game_board.table] += inputs['alpha'] * (reward - q_table[a][game_board.table])
        game_board.table = next_s
        return
    #if game continues take the next states action value
    table_old =game_board.table
    game_board.table = next_s
    a_prime = select_action(game_board, inputs['epsilon'], q_table, random_seed,0)
    a_prime_value = get_action_value(game_board,a_prime,q_table)
    game_board.table = table_old
    # set the q_table vlues
    q_table[a][game_board.table] += inputs['alpha'] * (
                reward + (inputs['gamma'] * a_prime_value) - q_table[a][game_board.table])

    # update board
    game_board.table = next_s

def q_learning(inputs, random_seed, q_table,game_board):
    # select action
    a = select_action(game_board,inputs['epsilon'],q_table,random_seed,1)
    #get reward and next board
    reward, next_s = take_action(copy.copy(game_board), a)
    # if game continues set reward to 0
    if(reward == 15):
        reward = 0
    # take the best action and q table value
    a_max, a_max_value = find_a_max(q_table,next_s,a)
    if(a_max_value != 0 ):
        dsada=5
    #update the q_table value of board in action
    q_table[a][game_board.table] += inputs['alpha'] * ( reward + (inputs['gamma'] * a_max_value) - q_table[a][game_board.table])
    if q_table[a][game_board.table] != 0:
        dsada=5
    # update the board
    game_board.table = next_s


def game(inputs, random_seed,method_name):
    # set the seed value which is given as an input
    random.seed(random_seed)
    player = 'X'
    #selectwho to start game as  a  X or O symbol
    starter = random.choice([0, 1])
    if (starter == 0):
        starter = 'X'
    else:
        starter = 'O'
    # init q table
    q_table = init_q_table(starter, player)

    # select corresponding X or O symbols wrt input function
    if(method_name == "SARSA"):
        #loop through episodes
       for i in range(inputs['episode_count']):
           #init game board for each episode as '---------'
           game_board = GameTable(starter, player)
           # while a game is not finished play the game
           while True:
               # according to starter symbol adjust the corresponding function
               if(starter == 'X'):
                   game_board.player = ('X')
                   sarsa(inputs, random_seed, q_table,game_board)
                   if(game_board.get_reward() != 15):
                       break
                   game_board.player = ('O')
                   q_learning(inputs, random_seed, q_table,game_board)
                   if (game_board.get_reward() != 15):
                       break
               else:
                   game_board.player = ('O')
                   q_learning(inputs, random_seed, q_table,game_board)
                   if (game_board.get_reward() != 15):
                       break
                   game_board.player = ('X')
                   sarsa(inputs, random_seed, q_table,game_board)
                   if (game_board.get_reward() != 15):
                       break

    else:
        # This has exact same explanations as upper part just the order of functions are changed
        for i in range(inputs['episode_count']):
            game_board = GameTable(starter, player)
            while True:
                if (starter == 'X'):
                    game_board.player = ('X')
                    q_learning(inputs, random_seed, q_table,game_board)
                    if (game_board.get_reward() != 15):
                        break
                    game_board.player = ('O')
                    sarsa(inputs, random_seed, q_table,game_board)
                    if (game_board.get_reward() != 15):
                        break
                else:
                    game_board.player = ('O')
                    sarsa(inputs, random_seed, q_table,game_board)
                    if (game_board.get_reward() != 15):
                        break
                    game_board.player = ('X')
                    q_learning(inputs, random_seed, q_table,game_board)
                    if (game_board.get_reward() != 15):
                        break

    return q_table

def SolveMDP ( method_name , problem_file_name , random_seed ) :
    #parse the given inputs and take as a dict
    inputs = parser(problem_file_name)
    #start the game and take the return value as q_table dict
    q_table = game(inputs, random_seed, method_name)

   #convert the result dict to expected output form
    result = {}
    #for each item of dict take act and its dictionary as element of act
    for action, elemets_of_act in q_table.items():
        # create an empty list to this key
        result[action] = []
        # take the board and corresponding q_table_value of this bord
        for board, q_value in elemets_of_act.items():
            #append them to dict value as a tupple
            result[action].append((board,q_value))
    #print the result
    print(result)




if __name__ == '__main__':
    SolveMDP("Q-learning", "mdp1.txt", 462)
    a=5