import model
import numpy as np
import os

def main():

	mode = str(input("\noption 't' is train (default)\noption 'e' is exploit\n\nENTER OPTION: ") or "t")

	if mode == "t":

		world = int(input("\nwhich World [0-10] would you like to train on? (default is World 0)\nWORLD: ") or "0")

		epochs = int(input(f"\nhow many epochs would you like to train the agent on World {world} for? (default is 1 epoch)\nEPOCHS: ") or "1")


		print(f"\ntraining from scratch for {epochs} on world {world}! \n(visualizations will be saved to './runs/world_{world}/')\n(Q-tables will be saved to './runs/Q-table_world_{world}'")

		verbose = str(input(f"\nWould you like detailed outputs? (default is yes)\n([y]/n)? ") or "y")
		if verbose == "y":
			v = True
		else:
			v = False

		epsilon = 0.9
		q_table = model.init_q_table()

		if not (os.path.exists(f"./runs/world_{world}/")):
			os.makedirs(f"./runs/world_{world}/")

		run_num = len([i for i in os.listdir(f"runs/world_{world}")])
		file_path = f"./runs/Q-table_world_{world}"

		good_term_states = []
		bad_term_states = []
		obstacles = []

		for epoch in range(epochs):
			print("EPOCH #"+str(epoch)+":\n\n")
			q_table, good_term_states, bad_term_states, obstacles = model.learn(
				q_table, worldId=world, mode='train', learning_rate=0.0001, gamma=0.9, epsilon=epsilon, good_term_states=good_term_states, bad_term_states=bad_term_states,
				epoch=epoch, obstacles=obstacles, run_num=run_num, verbose=v)

			epsilon = epsilon_decay(epsilon, epoch, epochs)

			np.save(file_path, q_table)
		np.save(f"./runs/obstacles_world_{world}", obstacles)
		np.save(f"./runs/good_term_states_world_{world}", good_term_states)
		np.save(f"./runs/bad_term_states_world_{world}", bad_term_states)

	elif mode == "e":
		
		world = int(input("\nwhich World [0-10] would you like the agent to exploit? (default is World 0)\nWORLD: ") or "0")
		epochs = int(input(f"\nhow many times would you like the agent to run on World {world} for? (default is 1 time)\nEPOCHS: ") or "1")

		verbose = str(input(f"\nverbosity? (default is yes)\n([y]/n)? ") or "y")
		if verbose == "y":
			v = True
		else:
			v = False

		print(f"\nExploiting world {world} for {epochs} iterations! \n(visualizations will be saved to './runs/world_{world}/')")

		file_path = f"./runs/Q-table_world_{world}"
		q_table = np.load(file_path+".npy")

		obstacles = np.load(f"./runs/obstacles_world_{world}"+".npy")
		good_term_states = np.load(f"./runs/good_term_states_world_{world}"+".npy")
		bad_term_states = np.load(f"./runs/bad_term_states_world_{world}"+".npy")

		obstacles = obstacles.tolist()
		good_term_states = good_term_states.tolist()
		bad_term_states = bad_term_states.tolist()

		epsilon = 0.9
		run_num = len([i for i in os.listdir(f"runs/world_{world}")])

		for epoch in range(epochs):
			print("EPOCH #"+str(epoch)+":\n\n")
			q_table, good_term_states, bad_term_states, obstacles = model.learn(
				q_table, worldId=world, mode='expl', learning_rate=0.0001, gamma=0.9, epsilon=epsilon, good_term_states=good_term_states, bad_term_states=bad_term_states,
				epoch=epoch, obstacles=obstacles, run_num=run_num, verbose=v)
	
	else:
		print("Sorry that is not an option! Bye Bye")
		exit()

def epsilon_decay(epsilon, epoch, epochs):
    '''
    function to exponentially decrease the episilon value 
    acroccs the total number of epochs we train on
    this leads us to explore less as we progress through epochs 
    '''
    epsilon = epsilon*np.exp(-.01*epoch)
    print(f"\nNEW EPSILON: {epsilon}\n")
    return epsilon

if __name__ == "__main__":
    main()