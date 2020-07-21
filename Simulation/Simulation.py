import random as rd
import numpy as np
import matplotlib.pyplot as plt

def random_coordinates(dim):
	return [rd.uniform(0, dim), rd.uniform(0, dim)]

def point_distance(point_a, point_b):
	xa, ya = point_a.get_pos()
	xb, yb = point_b.get_pos()

	return ((xa - xb)**2 + (ya - yb)**2)**0.5

# Remover self.population

class Simulation:
	def __init__(self, n, dim, speed, prob_infection, prob_recovery, initial_infected, radius, prob_point_jump):
		# Simulation parameters
		self.n = n
		self.dim = dim
		self.speed = speed 
		self.prob_infection = prob_infection
		self.prob_recovery = prob_recovery
		self.initial_infected = initial_infected
		self.radius = radius
		self.prob_point_jump = prob_point_jump

		# Simualtion data
		self.population = list()

		self.infected = list() 
		self.n_initial_infected = int(n*initial_infected)
		for i in range(self.n_initial_infected):
			point = Point(prob_point_jump, speed, dim)
			self.infected.append(point)
			self.population.append(point)

		self.susceptible = list()
		for i in range(n - self.n_initial_infected):
			point = Point(prob_point_jump, speed, dim)
			self.susceptible.append(point)
			self.population.append(point)

		self.recovered = list()

		self.__update_adj_matrix = np.zeros((n, n))

	# Run a simulation based on predefined parameters
	def run(self, adjacency=False):
		infected_by_time = list()
		avg_distance_by_time = list()

		while len(self.infected) > 0:
				infected_by_time.append(len(self.infected))

				if adjacency == True:
					self.__update_adj_matrix()

				# Move
				self.__move_points()

				# Infect
				self.__infect()

				# Cure
				self.__cure()

		self.__reset()
				
		return infected_by_time

	def __move_points(self):
		for point in self.population:
			point.move()

	def __infect(self):
		infected = list(self.infected)
		for infected_point in infected:
			for susceptible_point in self.susceptible:
				if point_distance(infected_point, susceptible_point) <= self.radius:
					if rd.uniform(0,1) < self.prob_infection:
						self.infected.append(susceptible_point)
						self.susceptible.remove(susceptible_point)

	def __cure(self):
		for infected_point in self.infected:
			if rd.uniform(0,1) < self.prob_recovery:
				self.recovered.append(infected_point)
				self.infected.remove(infected_point)

	def __reset(self):
		self.population = list()

		self.infected = list() 
		self.n_initial_infected = int(self.n*self.initial_infected)
		for i in range(self.n_initial_infected):
			point = Point(self.prob_point_jump, self.speed, self.dim)
			self.infected.append(point)
			self.population.append(point)

		self.susceptible = list()
		for i in range(self.n - self.n_initial_infected):
			point = Point(self.prob_point_jump, self.speed, self.dim)
			self.susceptible.append(point)
			self.population.append(point)

		self.recovered = list()


	def temp_draw(self):
		sus = list()
		for point in self.susceptible:
			sus.append(point.get_pos())

		inf = list()
		for point in self.infected:
			inf.append(point.get_pos())

		rec = list()
		for point in self.recovered:
			rec.append(point.get_pos())

		x_sus = [i for i,j in sus]
		y_sus = [j for i,j in sus]

		x_inf = [i for i,j in inf]
		y_inf = [j for i,j in inf]

		x_rec = [i for i,j in rec]
		y_rec = [j for i,j in rec]

		plt.scatter(x_sus, y_sus)
		plt.scatter(x_inf, y_inf, c='r')
		plt.scatter(x_rec, y_rec, c='g')

		plt.show()


	# def draw(self):

class Point:
	def __init__(self, prob_jump, speed, dim):
		self.pos = random_coordinates(dim)
		self.prob_jump = prob_jump
		self.speed = speed
		self.dim = dim

	# Moves a point
	def move(self):
		prob = rd.uniform(0, 1)

		# Performs a jump to a random position
		if prob < self.prob_jump:
			self.pos = random_coordinates(self.dim)

		else:
			angle = rd.uniform(0, 2*np.pi)
			
			self.pos[0] += self.speed * np.cos(angle)
			self.pos[1] += self.speed * np.sin(angle)
			
			# Out of perimeter point
			if self.pos[0] >= self.dim:
				self.pos[0] -= 2*(self.pos[0] - self.dim)
			if self.pos[1] >= self.dim:
				self.pos[1] -= 2*(self.pos[1] - self.dim)

			if self.pos[0] < 0:
				self.pos[0] -= 2*(self.pos[0])
			if self.pos[1] < 0:
				self.pos[1] -= 2*(self.pos[1])

	# Get the point coordinate
	def get_pos(self):
		return self.pos.copy()

	def __repr__(self):
		info = ""
		info += "[Coordenadas : ({}, {})]".format(self.pos[0], self.pos[1])

		return info