from Main import *

CalculusModel.num_people = 50000
CalculusModel.initial_infected = 10

CalculusModel.transmission_rate = 0.000005
CalculusModel.recovery_rate = 1/7
CalculusModel.death_rate = 0
CalculusModel.antibody_loss_rate = 0.01
CalculusModel.vaccination_rate = 0.001


if __name__ == '__main__':
    plt.ylim(0, CalculusModel.num_people)
    sim = CalculusModel()
    sim.draw = True
    sim.run()
    plt.ioff()
    print(f"Total Deaths: {graph.dead}")
    print(f"Max Infections: {max(graph.i)}")
    plt.show()