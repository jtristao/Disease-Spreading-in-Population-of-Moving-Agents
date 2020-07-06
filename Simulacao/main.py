from Simulation import *
import matplotlib.pyplot as plt

def main():
	pointA = Point(0, 0.1, 10)
	pointB = Point(0, 0.1, 10)

	n = 10
	movesA = list()
	movesB = list()
	for i in range(n):
		movesA.append(pointA.get_pos())
		pointA.move()
		movesB.append(pointB.get_pos())
		pointB.move()



	xA = [i for (i,j) in movesA]
	yA = [j for (i,j) in movesA]

	xB = [i for (i,j) in movesB]
	yB = [j for (i,j) in movesB]

	plt.plot(xA, yA)
	plt.plot(xB, yB)

	plt.xlim(0, 10)
	plt.ylim(0, 10)

	plt.show()


if __name__ == '__main__':
	main()