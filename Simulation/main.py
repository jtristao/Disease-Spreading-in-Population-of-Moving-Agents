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

	model = Model(**simulation_parameters)
	print(model)
	n = 100
	prob_agent_jump = [0, 0.01, 0.1, 1]
	# avg = disease_spreading_over_time(model, n, prob_agent_jump)

	model.visualization(0)

	# print(avg.max())


if __name__ == '__main__':
	main()