import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
fig, ax = plt.subplots()
fig.canvas.mpl_connect('close_event', quit)  # listen to close event

from Main import *


sim = CalculusModel()


def reset(val):
    sim.reset()
    graph.clear()
    graph.draw()
    sim.run()


def pause_play(val):
    print(val)
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
trans = Slider(ax=axis1, label='Transmission Rate (a)', valmin=0.0, valmax=0.00001, valinit=sim.transmission_rate)
axis2 = plt.axes([0.25, 0.2, 0.5, 0.01])
recovery = Slider(ax=axis2, label='Recovery Rate (B)', valmin=0.0, valmax=0.5, valinit=sim.recovery_rate)
axis3 = plt.axes([0.25, 0.15, 0.5, 0.01])
death = Slider(ax=axis3, label='Death Rate', valmin=0.0, valmax=0.1, valinit=sim.death_rate)
axis4 = plt.axes([0.25, 0.1, 0.5, 0.01])
antibodies = Slider(ax=axis4, label='Antibody Loss Rate', valmin=0.0, valmax=0.5, valinit=sim.antibody_loss_rate)
axis5 = plt.axes([0.25, 0.05, 0.5, 0.01])
vaccination = Slider(ax=axis5, label='Vaccination Rate', valmin=0.0, valmax=1000, valinit=sim.vaccination_rate)

go.on_clicked(pause_play)
restart.on_clicked(reset)

sim_speed.on_changed(lambda x: setattr(graph, "speed", x))
trans.on_changed(lambda x: setattr(sim, "transmission_rate", x))
recovery.on_changed(lambda x: setattr(sim, "recovery_rate", x))
death.on_changed(lambda x: setattr(sim, "death_rate", x))
antibodies.on_changed(lambda x: setattr(sim, "antibody_loss_rate", x))
vaccination.on_changed(lambda x: setattr(sim, "vaccination_rate", x))

plt.sca(ax)
sim.run()
plt.ioff()
plt.show()
