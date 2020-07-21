from Simulation import *
import matplotlib.pyplot as plt

def simulation_infected_over_time(n, dim, speed, prob_infection, prob_recovery, initial_infected, radius, prob_point_jump):
	test = Simulation(n=n, dim=dim, speed=speed, prob_infection=prob_infection, prob_recovery=prob_recovery,
						 initial_infected=initial_infected, radius=radius, prob_point_jump=prob_point_jump)

	results = list()
	max_dim = 0
	print("Running simulation...")
	for i in range(30):
		if i % 5 == 0:
			print("{}\t".format(i), end="", flush=True)
		
		infected_over_time = test.run()
		results.append(infected_over_time)
		max_dim = max(max_dim, len(infected_over_time))
	print()

	for i in range(len(results)):		
		results[i] = np.pad(results[i], (1, max_dim - len(results[i])), constant_values=0)
	results = np.array(results)

	average = results.mean(0)
	average = average/1000

	return average

def main():
	n = 1000
	dim = 32
	speed = 0.1
	prob_infection = 0.1
	prob_recovery = 0.05
	initial_infected = 0.01
	radius = 1
	prob_point_jump = [0, 0.01, 0.1, 1]

	results = list()
	for value in prob_point_jump:
		print("Jump prob: {}".format(value))
		results.append(simulation_infected_over_time(n, dim, speed, prob_infection, prob_recovery, initial_infected, radius, value))


	colors = ["blue", "red", "green", "gray"]
	for i in range(len(results)):
		plt.plot(results[i], c=colors[i], label="p={}".format(prob_point_jump[i]))
	
	plt.title("Number of infected individuals as a function of time")
	plt.xlabel("t")
	plt.ylabel("N(t)")
	plt.legend()
	plt.show()


if __name__ == '__main__':
	main()