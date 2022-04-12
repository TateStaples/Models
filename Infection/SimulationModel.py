from Main import *
import matplotlib.pyplot as plt

Person.infection_length = 7  # how long they remain infected
Person.antibody_length = 20  # how long people remain immune

SimulationModel.num_people = 10000  # the size of the population
SimulationModel.num_interaction = 5000  # how many interactions per time step
SimulationModel.infection_risk = 0.5  # odds of infection each time
SimulationModel.death_risk = 0.00  # how likely the infection is to kill
SimulationModel.start_infected = 10  # initial amount of infected

SimulationModel.vaccination_rate = 0  # how many people vaccinated per time step
SimulationModel.vaccination_effectiveness = 0.95  # what percent of vaccinated people become immune


if __name__ == '__main__':
    plt.ylim(0, SimulationModel.num_people)
    sim = SimulationModel()
    sim.draw = True
    sim.run()
    plt.ioff()
    print(f"Total Deaths: {graph.dead}")
    print(f"Max Infections: {max(graph.i)}")
    plt.show()