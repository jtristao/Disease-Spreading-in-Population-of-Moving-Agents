import random as rd
import numpy as np

def random_coordinates(dim):
	return [rd.uniform(0, dim), rd.uniform(0, dim)]


class Point:
	def __init__(self, prob_jump, speed, dim):
		self.pos = random_coordinates(dim)
		self.prob_jump = prob_jump
		self.speed = speed
		self.dim = dim
		
	def move(self):
		prob = rd.uniform(0, 1)

		# Realiza um salto para um local aleatorio
		if prob < self.prob_jump:
			print("JUMP")
			self.pos = random_coordinates(self.dim)
		else:
			print("MOVE")
			angle = rd.uniform(0, 2*np.pi)
			# print(self.pos)
			self.pos[0] += self.speed * np.cos(angle)
			self.pos[1] += self.speed * np.sin(angle)
			# print(self.pos)

	def get_pos(self):
		return self.pos.copy()

	def __str__(self):
		info = ""
		info += "Coordenadas : ({}, {})\n".format(self.pos[0], self.pos[1])
		info += "Velocidade: {}".format(self.speed)

		return info
