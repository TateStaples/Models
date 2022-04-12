import math

from matplotlib.widgets import Button, Slider
from Main import EulerApproximation
import matplotlib.pyplot as plt

fig, ax = plt.subplots()


def get_val(label: str):
    if Grapher.active is None or Interface.active is None:
        return
    return Interface.active.get_val(label) if label in Interface.active.labels else Grapher.active.get_val(label)


class Grapher:
    speed = 1
    time = 0
    legend = True
    active = None

    def __init__(self, labels: list):
        Grapher.active = self
        self.labels = labels
        for label in labels:
            setattr(self, label, list())
            setattr(self, label + "_plot", plt.plot([0], [0], label=label)[0])
        self.times = list()

        plt.ylim(0, 10)
        self.max = 10

    def clear(self):
        self.time = 0
        self.times = list()
        for label in self.labels:
            setattr(self, label, list())
        self.max = 10

    def update_graphs(self):
        x = self.times
        for label in self.labels:
            plot = getattr(self, label + "_plot")
            plot.set_xdata(x)
            plot.set_ydata(getattr(self, label))
        plt.xlim(0, self.time)

    def draw(self):
        self.update_graphs()
        if self.legend:
            plt.legend()
        plt.draw()
        plt.pause(.02 / self.speed)

    def add_val(self, label: str, val: float):
        if val > self.max:
            self.max = val
            plt.ylim(0, self.max * 1.1)
        vals = getattr(self, label)
        vals.append(val)

    def get_val(self, label: str):
        val = getattr(self, label)
        # print(label, val)
        return val[-1] if isinstance(val, list) else val

    def add_time(self, t):
        self.times.append(t)
        self.time = t

    @property
    def time_step(self):
        return self.times[-1] - self.times[-2]


class Calculusifier:
    paused = False
    draw = True
    running = True
    verbose = False

    def __init__(self, lines: list, time_step: float = 1.0, end_condition=(lambda: False)):
        self.time_step = time_step
        self.lines = lines
        self.calculators = [EulerApproximation(value=initial_val, derivative_formula=derivative, time_step=time_step)
                            for _, initial_val, derivative in lines]
        self.labels = [line[0] for line in lines]
        self.graph = Grapher(self.labels)
        for label, initial_val, _ in lines:
            self.graph.add_val(label, initial_val)
        self.graph.add_time(0)
        self.end_condition = end_condition

    def run(self):
        while self.running:
            while self.paused or self.end_condition():
                plt.pause(0.2)
            vals = []
            for label, calc in zip(self.labels, self.calculators):
                vals.append((label, calc.step()))
            for label, val in vals:
                self.graph.add_val(label, val)
            if self.verbose:
                print(self.graph.time+self.time_step, [(calc.value, calc.derivative) for calc in self.calculators])
            self.graph.add_time(self.graph.time + self.time_step)
            if self.draw:
                self.graph.draw()

    def reset(self):
        self.graph.clear()
        for calc, (label, initial_val, _) in zip(self.calculators, self.lines):
            self.graph.add_val(label, initial_val)
            calc.value = initial_val
            calc.time = 0
        self.graph.add_time(0)


class Interface:
    active = None

    # fig.canvas.mpl_connect('close_event', quit)  # listen to close event

    def __init__(self, constants: dict, sim: Calculusifier):
        Interface.active = self
        self.sim = sim
        self.constants = constants
        num_constants = len(constants)
        dy = 0.2 + 0.05 * num_constants
        plt.subplots_adjust(bottom=dy)

        # buttons
        self.pause_play = Button(plt.axes([0.15, dy - 0.1, 0.15, 0.03]), "Pause")
        self.reset = Button(plt.axes([0.35, dy - 0.1, 0.15, 0.03]), "Reset")
        self.pause_play.on_clicked(self.go)
        self.reset.on_clicked(self.restart)

        # constant sliders
        self.labels = [key for key in constants]
        # print(self.labels, constants)
        for constant in constants:
            initial_val, _, _ = constants[constant]
            setattr(self, constant, initial_val)
        self.sliders = [
            Slider(ax=plt.axes([0.25, 0.05 * num, 0.5, 0.01]), label=constant, valinit=constants[constant][0],
                   valmin=constants[constant][1], valmax=constants[constant][2])
            for num, constant in enumerate(constants, start=1)
        ]

        for label, slider in zip(self.labels, self.sliders):
            def get_function(name):
                def function(val):
                    setattr(Interface.active, name, val)
                return function
            slider.on_changed(get_function(label))

        plt.sca(ax)

    def get_val(self, label: str):
        # print("Interface getting label: ", label, getattr(self, label))
        return getattr(self, label) if label in self.labels else self.sim.graph.get_val(label)

    def go(self, *args):
        if "Pause" in str(self.pause_play.label):
            self.pause_play.label.set_text("Play")
            self.sim.paused = True
        else:
            self.pause_play.label.set_text("Pause")
            self.sim.paused = False

    def restart(self, *args):
        self.sim.reset()
        # self.sim.run()


infection_end_condition = lambda: get_val("I") < 1
SIR_variable = [
    ("S", 49990, lambda: -get_val("transmission") * get_val("S") * get_val("I")),
    ("I", 10, lambda: get_val("transmission") * get_val("S") * get_val("I") - get_val("recovery") * get_val("I")),
    ("R", 0, lambda: get_val("recovery") * get_val("I")),
]
SIR_constants = {"transmission": (0.000005, 0, 1), "recovery": (1 / 7, 0, 1)}


enhanced_infection_variables = [
    ("S", 49990, lambda: -get_val("transmission") * get_val("S") * get_val("I")
                        + get_val("antibody_loss") * get_val("R")
                        - get_val("vaccination")),
    ("I", 10, lambda: get_val("transmission") * get_val("S") * get_val("I")
                    - get_val("recovery") * get_val("I")
                    - get_val("death_rate") * get_val("I")),
    ("R", 0, lambda: get_val("recovery") * get_val("I")
                     + get_val("vaccination")
                     - get_val("antibody_loss") * get_val("R")),
    ("D", 0, lambda: get_val("I") * get_val("death_rate"))
]
enhanced_infection_constants = {
    "transmission": (0.000005, 0, 1), "recovery": (1/7, 0, 1), "death_rate": (0, 0, 0.1),
    "antibody_loss": (0, 0.5), "vaccination": (0, 0, 10000)
}

quarantine_variables = [
    ("S", 49990, lambda: -get_val("transmission") * get_val("S") * (1-(1-(get_val("transmission")/(get_val("S") + get_val("R")))) ** (get_val("quarantine_rate") * get_val("I"))) * get_val("I") - get_val('transmission') * get_val("S") * (1-get_val("quarantine_rate"))*get_val("I")),
    ("I", 10, lambda: get_val("transmission") * get_val("S") * (1-(1-(get_val("transmission")/(get_val("S") + get_val("R")))) ** (get_val("quarantine_rate") * get_val("I"))) * get_val("I") + get_val('transmission') * get_val("S") * (1-get_val("quarantine_rate"))*get_val("I") - get_val("recovery") * get_val("I")),
    ("R", 0, lambda: (1-get_val('death_rate')) * get_val('recovery') * get_val('I')),
    ("D", 0, lambda: get_val("I") * get_val('death_rate') * get_val('recovery'))
]
quarantine_constants = {
    'quarantine_rate': (0, 0, 1), 'death_rate': (0.005, 0, .1), 'transmission': (0.000005, 0, 0.00001), 'recovery': (1/7, 0, 1/2)
}

battle_variables = [
    ("Army1", 100, lambda: -get_val("Army2") * get_val("Army2_Strength")),
    ("Army2", 200, lambda: -get_val("Army1") * get_val("Army1_Strength")),
]
battle_constants = {"Army1_Strength": (0.04, 0, 0.2), "Army2_Strength": (0.02, 0, 0.2)}

guerrilla_variables = [
    ("ConventionalArmy", 100, lambda: -get_val("GuerrillaArmy") * get_val("GuerrillaArmyStrength")),
    ("GuerrillaArmy", 100,
     lambda: -get_val("ConventionalArmy") * get_val("GuerrillaArmy") * get_val("ConventionalArmyStrength")),
]
guerrilla_constants = {"ConventionalArmyStrength": (0.00002, 0, 0.001), "GuerrillaArmyStrength": (0.01, 0, 0.1)}

baseballCard_variables = [("Value", 2500,
                           lambda: get_val("growth_rate") / (2 * math.sqrt(get_val("time") + 1)) * math.exp(
                               get_val("growth_rate") * math.sqrt(get_val("time") + 1)))]
baseballCard_constants = {"growth_rate": (0.5, 0, 5)}

drug_variables = [("Dosage", 300, lambda: -1 * get_val("decay_rate") * get_val("Dosage") if get_val("Dosage") > get_val("Effective_Amount") else get_val("Dosage_Size") / get_val("time_step")),
                  ("Min_Dosage", 100, lambda: get_val("Effective_Amount") - get_val("Min_Dosage")),
                  ("Max_Dosage", 500, lambda: get_val("Safe_Amount") - get_val("Max_Dosage"))
                  ]
drug_constants = {"decay_rate": (1 - math.pow(0.88, 1 / 60), 0, 0.01),
                  "Dosage_Size": (300, 0, 1000),
                  "Safe_Amount": (500, 0, 1000),
                  "Effective_Amount": (100, 0, 1000)}

predator_variable = [
    ("Predators", 40, lambda: get_val("hunt_rate") * get_val("Predators") * get_val("Prey") - get_val("pred_starvation_rate") * get_val("Predators")),
    ("Prey", 200, lambda: get_val("prey_fecundity") * get_val("Prey") * (1-get_val("Prey")/get_val("capacity"))
                          - get_val("deaths_per_pred") * get_val("Predators") * get_val("Prey")),
]
predator_constants = {"prey_fecundity": (0.05, 0, 0.1), "capacity": (5000, 0, 10000),
                      "deaths_per_pred": (0.001, 0, 0.01),
                      "hunt_rate": (0.0002, 0, 0.001), "pred_starvation_rate": (0.03, 0, .1)}

if __name__ == '__main__':
    sim = Calculusifier(
        quarantine_variables,
        time_step=1, end_condition=infection_end_condition
    )
    sim.verbose = False
    interface = Interface(
        quarantine_constants
        , sim)
    sim.run()
    plt.ioff()
    plt.show()
    # while True: plt.pause(0.1)