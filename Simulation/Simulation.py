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

		# Simualtion data
		self.total_time	= 0
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

	# Repro
	def run(self):
		infected_by_time = list()


		while len(self.infected) > 0:
				self.temp_draw()

				# Move
				self.__move_points()

				# Infect
				self.__infect()

				
				
				# Cure
				

	def __move_points(self):
		for point in self.population:
			point.move()

	def __infect(self):
		infected = list(self.infected)
		susceptible = list(self.susceptible)
		for infected_point in infected:
			print(len(self.infected))
			for susceptible_point in susceptible:
				if point_distance(infected_point, susceptible_point) <= self.radius:
					if rd.uniform(0,1) < self.prob_infection:
						self.infected.append(susceptible_point)
						self.susceptible.remove(susceptible_point)

	def temp_draw(self):
		sus = list()
		for point in self.susceptible:
			sus.append(point.get_pos())

		inf = list()
		for point in self.infected:
			inf.append(point.get_pos())

		x_sus = [i for i,j in sus]
		y_sus = [j for i,j in sus]

		x_inf = [i for i,j in inf]
		y_inf = [j for i,j in inf]

		plt.scatter(x_sus, y_sus)
		plt.scatter(x_inf, y_inf, c='r')

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

def main():
	test = Simulation(n=10, dim=3, speed=0.1, prob_infection=1, prob_recovery=0.1, initial_infected=0.1, radius=1, prob_point_jump=0)

	print(test.run())
	# print("Points :", test.temp_draw())

if __name__ == '__main__':
	main()