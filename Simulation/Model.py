import random as rd
import numpy as np
import matplotlib.pyplot as plt
import os
import networkx as nx

def random_coordinate(dim):
	return [rd.uniform(0, dim), rd.uniform(0, dim)]

def agent_distance(agent_a, agent_b):
	xa, ya = agent_a[0], agent_a[1] 
	xb, yb = agent_b[0], agent_b[1]

	return ((xa - xb)**2 + (ya - yb)**2)**0.5

def coordinate_floor(coordinate):
	return (int(coordinate[0]), int(coordinate[1]))

def is_inside(position, dim):
	if position[0] >= 0 and position[0] < dim and position[1] >= 0 and position[1] < dim:
		return True

	return False

class Model:
	def __init__(self, n, dim, prob_agent_jump=1, speed=0.1, prob_infection=0.1, prob_recovery=0.05, 
					initial_infected=0.01, radius=1):
		self.n = n
		self.dimension = dim
		self.prob_agent_jump = prob_agent_jump
		self.speed = speed
		self.prob_infection = prob_infection
		self.prob_recovery = prob_recovery
		self.initial_infected = initial_infected
		self.radius = radius

		self.agent_to_coordinate = dict()
		self.coordinate_to_agent = dict()

		# rd.seed(25)

		for i in range(self.n):
			coordinate = random_coordinate(self.dimension)
			discrete_coordinate = coordinate_floor(coordinate)

			self.agent_to_coordinate[i] = coordinate
			if discrete_coordinate in self.coordinate_to_agent: 
				self.coordinate_to_agent[discrete_coordinate].append(i)
			else:
				self.coordinate_to_agent[discrete_coordinate] = [i]

		self.infected = set(rd.sample(range(self.n), int(self.initial_infected * self.n)))
		
		self.recovered = list()

	def run(self, prob_agent_jump):
		self.prob_agent_jump = prob_agent_jump
		infected_over_time = list()

		while len(self.infected) > 0:
			infected_over_time.append(len(self.infected))
			self.__infect()
			self.__recover()
			self.__move()

		self.__reset()

		return infected_over_time

	def visualization(self, prob_agent_jump):
		self.prob_agent_jump = prob_agent_jump
		
		if not os.path.isdir("./animation"):
			os.mkdir("animation")
		path = os.getcwd() + "/animation/"
		img_cnt = 0

		while len(self.infected) > 0:
			self.__draw(path + "{:03d}.png".format(img_cnt))
			img_cnt += 1

			self.__infect()
			self.__recover()
			self.__move()

		os.system("ffmpeg -f image2 -r 10 -i animation/%03d.png -vcodec mpeg4 -vb 40M -y ./disease_spreading.mp4")
		os.system("rm -r animation")


	def distance_simulation(self, prob_agent_jump):
		self.prob_agent_jump = prob_agent_jump

		duration = int(1/self.prob_recovery)

		adjacency_matrix = np.zeros((self.n, self.n))
		self.__update_adjacency_matrix(adjacency_matrix)

		for i in range(duration):
			self.__move()
			self.__update_adjacency_matrix(adjacency_matrix)

		graph = nx.Graph(adjacency_matrix)
		number_components = nx.number_connected_components(graph)

		distance = 0
		clustering = 0
		for comp in nx.connected_components(graph):
			temp = graph.subgraph(comp)
			distance += nx.average_shortest_path_length(temp)
			clustering += nx.average_clustering(temp)

		distance /= number_components
		clustering /= number_components

		return distance, clustering

	def __update_adjacency_matrix(self, adjacency_matrix):
		adj_cells = [[-1,-1], [0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0], [0, 0]]

		for i in range(self.dimension):
			for j in range(self.dimension):
				if (i,j) in self.coordinate_to_agent:
					cel_agents = self.coordinate_to_agent[(i,j)]

					for agent in cel_agents:
						for neighbors in adj_cells: 
							neighbor_pos = (i+neighbors[0], j+neighbors[1])
							if is_inside(neighbor_pos, self.dimension) and neighbor_pos in self.coordinate_to_agent: 
								neighbors_in_adj_cell = self.coordinate_to_agent[neighbor_pos]

								for neighbor in neighbors_in_adj_cell:
									adjacency_matrix[agent][neighbor] = 1

		return adjacency_matrix

	def __draw(self, filename):
		infected = list()
		recovered = list()
		susceptible = list()

		for agent, coord in self.agent_to_coordinate.items():
			if agent in self.infected:
				infected.append(coord)
			elif agent in self.recovered:
				recovered.append(coord)
			else:
				susceptible.append(coord)

		x_sus = [i for i,j in susceptible]
		y_sus = [j for i,j in susceptible]

		x_inf = [i for i,j in infected]
		y_inf = [j for i,j in infected]

		x_rec = [i for i,j in recovered]
		y_rec = [j for i,j in recovered]

		sus = plt.scatter(x_sus, y_sus, c='b', s=5, label ="susceptible")
		inf = plt.scatter(x_inf, y_inf, c='r', s=5, label="infected")
		rec = plt.scatter(x_rec, y_rec, c='g', s=5, label="recovered")

		plt.title("Disease spreading")
		plt.legend(bbox_to_anchor=(0.8, 1), loc='upper left', ncol=1)

		plt.axis('off')

		if filename:
			plt.savefig(filename)
		else:
			plt.show()

		plt.close()

	def __reset(self):
		self.agent_to_coordinate = dict()
		self.coordinate_to_agent = dict()

		for i in range(self.n):
			coordinate = random_coordinate(self.dimension)
			discrete_coordinate = coordinate_floor(coordinate)

			self.agent_to_coordinate[i] = coordinate
			if discrete_coordinate in self.coordinate_to_agent: 
				self.coordinate_to_agent[discrete_coordinate].append(i)
			else:
				self.coordinate_to_agent[discrete_coordinate] = [i]

		self.infected = set(rd.sample(range(self.n), int(self.initial_infected * self.n)))
		self.recovered = list()
		

	def __recover(self):
		infected = list(self.infected)
		for agent in infected:
			if rd.uniform(0,1) < self.prob_recovery:
				self.recovered.append(agent)
				self.infected.remove(agent)

	def __infect(self):
		infected = list(self.infected)
		
		for agent in infected:
			coordinate = self.agent_to_coordinate[agent]
			discrete_coordinate = coordinate_floor(coordinate)

			moves = [[-1,-1], [0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0], [0, 0]]

			for move in moves:
				position = tuple([discrete_coordinate[0] + move[0], discrete_coordinate[1] + move[1]])

				if is_inside(position, self.dimension) and position in self.coordinate_to_agent:
					for neighbor in self.coordinate_to_agent[position]:
						neighbor_pos = self.agent_to_coordinate[neighbor]
						if rd.uniform(0,1) <= self.prob_infection and neighbor not in self.recovered:
							if agent_distance(coordinate, neighbor_pos) <= self.radius:
								self.infected.add(neighbor)


	def __move(self):
		for agent, agent_pos in self.agent_to_coordinate.items():
			discrete_old_pos = coordinate_floor(agent_pos)

			new_pos = self.__make_move(agent_pos)
			discrete_new_pos = coordinate_floor(new_pos) 

			self.agent_to_coordinate[agent] = new_pos
			if discrete_old_pos != discrete_new_pos:
				# print("Changed:", agent, new_pos, discrete_new_pos, discrete_old_pos)
				self.coordinate_to_agent[discrete_old_pos].remove(agent)

				if discrete_new_pos in self.coordinate_to_agent:
					self.coordinate_to_agent[discrete_new_pos].append(agent)
				else:
					self.coordinate_to_agent[discrete_new_pos] = [agent]


	def __make_move(self, pos):
		prob = rd.uniform(0, 1)

		# Performs a jump to a random position
		if prob <= self.prob_agent_jump:
			pos = random_coordinate(self.dimension)

		else:
			angle = rd.uniform(0, 2*np.pi)
			
			pos[0] += self.speed * np.cos(angle)
			pos[1] += self.speed * np.sin(angle)
			
			# Point out of perimeter
			if pos[0] >= self.dimension:
				pos[0] -= 2*(pos[0] - self.dimension)
			if pos[1] >= self.dimension:
				pos[1] -= 2*(pos[1] - self.dimension)

			if pos[0] < 0:
				pos[0] -= 2*(pos[0])
			if pos[1] < 0:
				pos[1] -= 2*(pos[1])

		return pos


	def __repr__(self):
		data = "Model: \n"
		data += "\tNumber of agents : %i \n" % self.n 
		data += "\tDimension : %i \n" % self.dimension
		# data += "\tProbability of agent jump : %.2f \n" % self.prob_agent_jump 
		data += "\tSpeed : %.3f \n" % self.speed
		data += "\tProbability of infection: %.3f \n" % self.prob_infection 
		data += "\tProbability of recovery : %.3f \n" % self.prob_recovery
		data += "\tPercentage of initial infection  : %.3f \n" % self.initial_infected 
		data += "\tRadius : %.3f\n" % self.radius

		return data