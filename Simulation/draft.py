import random as rd
import numpy as np
import matplotlib.pyplot as plt

def random_coordinate(dim):
	return [rd.uniform(0, dim), rd.uniform(0, dim)]

def point_distance(point_a, point_b):
	xa, ya = point_a.get_pos()
	xb, yb = point_b.get_pos()

	return ((xa - xb)**2 + (ya - yb)**2)**0.5

def coordinate_floor(coordinate):
	return (int(coordinate[0]), int(coordinate[1]))

def is_inside(position, dim):
	if position[0] >= 0 and position[0] < dim and position[1] >= 0 and position[1] < dim:
		return True

	return False

class Simulation:
	def __init__(self, n, dim, prob_agent_jump, speed=1, prob_infection=0.1, prob_recovery=0.05, 
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

		for i in range(n):
			coordinate = random_coordinate(dim)
			discrete_coordinate = coordinate_floor(coordinate)

			self.agent_to_coordinate[i] = coordinate
			if discrete_coordinate in self.coordinate_to_agent: 
				self.coordinate_to_agent[discrete_coordinate].append(i)
			else:
				self.coordinate_to_agent[discrete_coordinate] = [i]

		self.infected = set(rd.sample(range(n), int(initial_infected*n)))
		
		self.recovered = list()

	def run(self):
		while len(self.infected) > 0:
			# print(self.coordinate_to_agent)
			# print(self.agent_to_coordinate, end="\n\n")
			self.__move()
			print(self.infected)
			self.__infect()
			self.__recover()

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

			moves = [[-1,-1], [0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0]]

			for move in moves:
				position = tuple([discrete_coordinate[0] + move[0], discrete_coordinate[1] + move[1]])

				if is_inside(position, self.dimension) and position in self.coordinate_to_agent:
					for neighbor in self.coordinate_to_agent[position]:
						if rd.uniform(0,1) < self.prob_infection and neighbor not in self.recovered:
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
		if prob < self.prob_agent_jump:
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
		return "Simulation"

def main():
	t = Simulation(n=10, dim=3, prob_agent_jump=0, initial_infected=0.1)
	t.run()

if __name__ == '__main__':
	main()