from Simulation import *
import matplotlib.pyplot as plt

def main():
	test = Simulation(n=10, dim=3, speed=0.1, prob_infection=1, prob_recovery=0.1, initial_infected=0.1, radius=1, prob_point_jump=0)

	print(test.run())
	# print("Points :", test.temp_draw())

if __name__ == '__main__':
	main()