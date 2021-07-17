from Simulation import *
from Model import *

def main():
	simulation_parameters = {
		'n':1000,
		'dim' : 31,
		'speed' : 0.1,
		'prob_infection' : 0.1,
		'prob_recovery' : 0.05,
		'initial_infected' : 0.01,
	}

	# simulation_parameters = {
	# 	'n':10,
	# 	'dim' : 3,
	# 	'speed' : 0.1,
	# 	'prob_infection' : 0.1,
	# 	'prob_recovery' : 0.05,
	# 	'initial_infected' : 0.01,
	# }

	model = Model(**simulation_parameters)
	print(model)
	# n = 100
	# prob_agent_jump = [0, 0.01, 0.1, 1]
	# avg = disease_spreading_over_time(model, n, prob_agent_jump)

	# distance_and_clustering_average(model)
	# print(avg.max())
	model.visualization(0)


if __name__ == '__main__':
	main()