from Model import *
import progressbar

def disease_spreading_over_time(model, n_simulations, prob_agent_jump, folder=None):
	print("Running Simulation")

	average = list()
	for prob in prob_agent_jump:
		print("Agent Jump probability: %f" % prob)

		results = list()
		max_dim = 0

		bar = progressbar.ProgressBar(maxval=n_simulations, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
		bar.start()

		for i in range(n_simulations):
			results.append(model.run(prob))
			max_dim = max(max_dim, len(results[i]))
			
			bar.update(i+1)

		bar.finish()

		for i in range(len(results)):		
			results[i] = np.pad(results[i], (1, max_dim - len(results[i])), constant_values=0)

		results = np.array(results)
		results = results.mean(0)
		results /= 1000

		average.append(results)

	colors = ["blue", "red", "green", "gray"]
	for i in range(len(average)):
		plt.plot(average[i], c=colors[i], label="p={}".format(prob_agent_jump[i]))
	
	plt.title("Number of infected individuals as a function of time")
	plt.xlabel("t")
	plt.ylabel("N(t)")
	plt.legend()
	plt.show()

	return average

def distance_and_clustering_average(model):
	prob_agent_jump = np.logspace(-6, 0, num=20)
	distance_average = list()
	clustering_average = list()

	print("Distance and clustering analysis")
	for prob in prob_agent_jump:
		print("Agent Jump probability: %f" % prob)

		distance = 0
		clustering = 0

		bar = progressbar.ProgressBar(maxval=10, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
		bar.start()

		for i in range(10):
			results = model.distance_simulation(prob)
			distance += results[0]
			clustering += results[1]

			bar.update(i+1)

		bar.finish()

		distance_average.append(distance/10)
		clustering_average.append(clustering/10)

	print(distance_average)
	print(clustering_average)