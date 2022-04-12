import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
fig, ax = plt.subplots()
fig.canvas.mpl_connect('close_event', quit) # listen to close event

from Main import *


sim = SimulationModel()


def reset(val):
    sim.reset()
    graph.clear()
    graph.draw()
    sim.run()


def pause_play(val):
    if "Pause" in str(go.label):
        go.label.set_text("Play")
        sim.paused = True
    else:
        go.label.set_text("Pause")
        sim.paused = False


plt.subplots_adjust(bottom=0.5)

# x, y, w, h
pos1 = plt.axes([0.15, 0.35, 0.15, 0.03])
go = Button(pos1, "Pause")
pos2 = plt.axes([0.35, 0.35, 0.15, 0.03])
restart = Button(pos2, "Reset")
axis0 = plt.axes([0.25, 0.3, 0.5, 0.01])
sim_speed = Slider(ax=axis0, label='Speed', valmin=0.00001, valmax=1, valinit=1)
axis1 = plt.axes([0.25, 0.25, 0.5, 0.01])
infection_risk = Slider(ax=axis1, label='Infection Rate', valmin=0.0, valmax=1, valinit=sim.infection_risk)
axis2 = plt.axes([0.25, 0.2, 0.5, 0.01])
num_interaction = Slider(ax=axis2, label='Interaction Count', valmin=0.0, valmax=20000, valinit=sim.num_interaction)
axis3 = plt.axes([0.25, 0.15, 0.5, 0.01])
infection_length = Slider(ax=axis3, label='Infection Length', valmin=0.0, valmax=100, valinit=Person.infection_length)
axis4 = plt.axes([0.25, 0.1, 0.5, 0.01])
antibody_length = Slider(ax=axis4, label='Antibody Length', valmin=0.0, valmax=656, valinit=Person.antibody_length)
axis5 = plt.axes([0.25, 0.05, 0.5, 0.01])
death_risk = Slider(ax=axis5, label='Death Risk', valmin=0.0, valmax=1, valinit=sim.death_risk)

go.on_clicked(pause_play)
restart.on_clicked(reset)

sim_speed.on_changed(lambda x: setattr(graph, "speed", x))
infection_risk.on_changed(lambda x: setattr(sim, "infection_risk", x))
num_interaction.on_changed(lambda x: setattr(sim, "num_interaction", int(x)))
infection_length.on_changed(lambda x: setattr(Person, "infection_length", x))
antibody_length.on_changed(lambda x: setattr(Person, "antibody_length", x))
death_risk.on_changed(lambda x: setattr(sim, "death_risk", x))

plt.sca(ax)
plt.ylim(0, sim.num_people)
sim.run()
plt.ioff()
plt.show()
