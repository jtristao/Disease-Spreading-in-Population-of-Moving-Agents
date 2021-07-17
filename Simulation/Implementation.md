# Implementation

A brief description of the implemented classes, their main attributes and how to use them.

## Simulation
	
The main class of the project. It handles the simulation attributes and simulates the disease spreading, returning different results.

### Attributes

* n: Total number of agents in the simulation.
* dim: The length of the cell (dim * dim)
* prob\_agent\_jump:
* speed:
* prob_infection:
* prob_recovery:
* initial_infected:
* radius:

### Functions

#### Number of infected individuals as a function of time

* usage: disease\_spreading\_over\_time(n_simulations, prob_agent_jump, folder=None)
* arguments:
   * n_simulations : number of times the simulation will run
   * p : list of probabilities for an agent to move
   * folder : if not none, the place where the plot will be saved

Run the simulation changing the agent probability of jump, keeping track of the number of infected individuals at every instant. The simulation runs n times and results are averaged.

[8.878856595551898, 9.353307907907908, 8.863455213672582, 9.304705505505504, 9.35078098098098, 9.288024824824825, 8.718921721721722, 8.052224824824824, 6.804604007614829, 6.449184584584584, 5.541211611611612, 4.348852925069357, 3.8552860860860863, 3.2667633633633635, 2.7931033033033033, 2.456632232232232, 2.0797757757757758, 1.9191051051051047, 1.8657387387387387, 1.8278484484484483]

[0.5814967879479698, 0.6168774906439537, 0.6325200186363376, 0.6158913891056992, 0.6111496234671618, 0.6219727984279606, 0.615826410404072, 0.6152039612191254, 0.5716682198392027, 0.6074908331583485, 0.5981824774439954, 0.5521078302624531, 0.5665803732951857, 0.5180115369267904, 0.42972911402042013, 0.3200956511427345, 0.2148094413008915, 0.16681843964817478, 0.17115924820322848, 0.19264788854885376]
