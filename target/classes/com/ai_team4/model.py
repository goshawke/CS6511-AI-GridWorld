import numpy as np
import Requests
import movement_viz as v
from matplotlib import pyplot

def init_q_table():
    '''
    init q table (initilizations are all [0])
    defines grid as 40x40, 4 possible actions (N, S, E, W)
    access grid as row, col, action
    ex of indexing: q-tab[0][0][0] grid 0:0, action 'N'
    '''

    return (np.zeros((40, 40, 4)))

def num_to_move(num):
    '''
    translates the index returned from np.argmax()
    when accessing our representation of the q-table
    structure into the expexted value that the API 
    can understand
    '''
    if num == 0:
        return 'N'
    elif num == 1:
        return 'S'
    elif num == 2:
        return 'E'
    elif num == 3:
        return 'W'

    return 'ERROR!'

def update_q_table(location, q_table, reward, gamma, new_loc, learning_rate, move_num):
    '''
    bellman eq: NEW Q(s,a) = Q(s,a) + learning_rate * [R(s,a) + gamma * maxQ'(s',a') - Q(s,a)]
    '''

    #collecting the current understanding of the best q value based upon our new location, weight it by gamma and add reward
    right_side = reward + gamma * q_table[new_loc[0], new_loc[1], :].max() - q_table[location[0], location[1], move_num]

    #use the previous location to 
    new_q = q_table[location[0], location[1], move_num] + learning_rate * right_side

    #update q_table with new value
    q_table[location[0], location[1], move_num] = new_q


def learn(q_table, worldId=0, mode='train', learning_rate=0.001, gamma=0.9, epsilon=0.9, good_term_states=[], bad_term_states=[], epoch=0, obstacles=[], run_num=0, verbose=True):
    '''
    ~MAIN LEARNING FUNCTION~
    takes in:
    -the Q-table data structure (numpy 3-dimensional array)
    -worldId (for api and plotting)
    -mode (train or exploit)
    -learning rate (affects q-table calculation)
    -gamma (weighting of the rewards)
    -epsilon (determines the amount of random exploration the agent does)
    -good_term_states
    -bad_term_states
    -eposh
    -run number
    -verbosity

    returns: q_table [NumPy Array], good_term_states [list], bad_term_states [list], obstacles [list]
    '''

    #create the api instance
    a = Requests.Requests(worldId=worldId)
    a.enter_world()

    #init terminal state reached
    terminal_state = False

    #create a var to track the type of terminal state
    good = False

    #accumulate the rewards so far for plotting reward over step
    rewards_acquired = []

    #find out where we are
    loc_world, loc_state = a.get_location()

    #create a list of everywhere we've been for the viz
    visited = []

    # if verbose: print("loc_response",loc_response)
    
    # convert JSON into a tuple (x,y)
    location = int(loc_state.split(':')[0]), int(loc_state.split(':')[1]) #location is a tuple (x, y)
    
    # SET UP FIGURE FOR VISUALIZATION.
    pyplot.figure(1, figsize=(10,10))
    curr_board = [[float('-inf')] * 40 for temp in range(40)]
    
    #keep track of where we've been for the visualization
    visited.append(location)
    while True:
        curr_board[location[1]][location[0]] = 1
        for i in range (len(curr_board)):
            for j in range(len(curr_board)):
                if (curr_board[i][j] != 0):
                    curr_board[i][j] -= .1
        for obstacle in obstacles:
            if obstacle in visited:
                obstacles.remove(obstacle)
        v.update_grid(curr_board, good_term_states, bad_term_states, obstacles, run_num, epoch, worldId, location, verbose)

        #in q-table, get index of best option for movement based on our current state in the world
        if mode == 'train':
            #use an episolon greedy approach to randomly explore or exploit
            if np.random.uniform() < epsilon:
                unexplored = np.where(q_table[location[0]][location[1]].astype(int) == 0)[0]
                explored = np.where(q_table[location[0]][location[1]].astype(int) != 0)[0]

                if unexplored.size != 0:
                    move_num = int(np.random.choice(unexplored))
                else:
                    move_num = int(np.random.choice(explored))
            else:
                move_num = np.argmax(q_table[location[0]][location[1]])

        else:
            #mode is exploit -we'll use what we already have in the q-table to decide on our moves
            move_num = np.argmax(q_table[location[0]][location[1]])

        #make the move - transition into a new state
        move_response = a.make_move(move=num_to_move(move_num), worldId=str(worldId)) 

        if verbose: print("move_response", move_response)
        

        if move_response["code"] != "OK":
            #handel the unexpected
            print(f"something broke on make_move call \nresponse lookes like: {move_response}")

            move_failed = True
            while move_failed:
                move_response = a.make_move(move=num_to_move(move_num), worldId=str(worldId))

                print("\n\ntrying move again!!\n\n")

                if move_response["code"] == 'OK':
                    move_failed = False
        
        # check that we're not in a terminal state, and if not convert new location JSON into tuple
        if move_response["newState"] is not None:
            new_loc = int(move_response["newState"]["x"]), int(move_response["newState"]["y"]) #tuple (x,y)
            
            # keep track of if we hit any obstacles
            expected_loc = list(location)
            recent_move = num_to_move(move_num)
      
            if recent_move == "N":
                expected_loc[1]+=1
            elif recent_move == "S":
                expected_loc[1]-=1
            elif recent_move == "E":
                expected_loc[0]+=1
            elif recent_move == "W":
                expected_loc[0]-=1

            expected_loc = tuple(expected_loc)

            if verbose: print(f"New Loc: {new_loc} (where we actually are now):")
            if verbose: print(f"Expected Loc: {expected_loc} (where we thought we were going to be):")

            if (mode == "train"):
                obstacles.append(expected_loc)

            #continue to track where we have been
            visited.append(new_loc)

            #if we placed an obstacle there in the vis, remove it
            for obstacle in obstacles:
                if obstacle in visited:
                    obstacles.remove(obstacle)
            
        else:
            #we hit a terminal state
            terminal_state = True
            print("\n\n--------------------------\nTERMINAL STATE ENCOUNTERED\n--------------------------\n\n")
       
        #get the reward for the most recent move we made
        reward = float(move_response["reward"])


        #add reward to plot
        rewards_acquired.append(reward) 

        #if we are training the model then update the q-table for the state we were in before
        #using the bellman-human algorithim
        if mode == "train":
            update_q_table(location, q_table, reward, gamma, new_loc, learning_rate, move_num)
        
        #update our current location variable to our now current location
        location = new_loc


        #if we are in a terminal state then we need to collect the information for our visualization
        #and we need to end our current training epoch
        if terminal_state:
            print(f"Terminal State REWARD: {reward}")

            if reward > 0:
                #we hit a positive reward so keep track of it as a good reward terminal-state
                good = True
            if not(location in good_term_states) and not(location in bad_term_states):
                #update our accounting of good and bad terminal states for the visualization
                if good:
                    good_term_states.append(location)
                else:
                    bad_term_states.append(location)

            #update our visualization a last time before moving onto the next epoch
            v.update_grid(curr_board, good_term_states, bad_term_states, obstacles, run_num, epoch, worldId, location, verbose)
            break

    return q_table, good_term_states, bad_term_states, obstacles

