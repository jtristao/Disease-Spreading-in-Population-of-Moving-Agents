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