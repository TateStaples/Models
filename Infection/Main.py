import matplotlib.pyplot as plt
import random
import copy


class EulerApproximation:
    def __init__(self, **kwargs):
        self.derivative = 0
        self.time = 0
        self.value = 0
        self.derivative_formula = lambda: 1
        self.time_step = 1

        for key in kwargs:
            setattr(self, key, kwargs[key])

        self._times = list()
        self._values = list()

    """
    Take a step along the differential location from current location
    """
    def step(self, dt=None):
        self.derivative = self.derivative_formula()
        if dt is None: dt = self.time_step
        delta_y = dt * self.derivative

        # add current position
        self._times.append(self.time)
        self._values.append(self.value)

        # adjust to new position
        self.time += dt
        self.value += delta_y
        return self.value

    def __call__(self, *args, **kwargs):
        return self.step()


class CalculusModel:
    draw = True
    paused = False

    num_people = 50000
    initial_infected = 10

    transmission_rate = 0.000005  # a
    recovery_rate = 1 / 7  # B
    antibody_loss_rate = 0.00
    death_rate = 0.00
    vaccination_rate = 0

    def __init__(self):
        self.susceptible = self.infected = self.recovered = self.dead = 0  # initialize variables
        self.reset()

        self.dS = lambda: -self.transmission_rate * self.infected * self.susceptible \
                          + self.antibody_loss_rate * self.recovered \
                          - self.vaccination_rate
        self.dI = lambda: self.transmission_rate * self.infected * self.susceptible \
                          - self.recovery_rate * self.infected
        self.dR = lambda: self.recovery_rate * self.infected \
                          - self.antibody_loss_rate * self.recovered \
                          - self.death_rate * self.recovered \
                          + self.vaccination_rate
        self.dD = lambda: self.death_rate * self.recovered

    def reset(self):
        self.infected = self.initial_infected
        self.recovered = 0
        self.susceptible = self.num_people - self.infected
        self.dead = 0

    def run(self):
        ds = []
        susceptible_calculator = EulerApproximation(value=self.susceptible, derivative_formula=self.dS)
        infected_calculator = EulerApproximation(value=self.infected, derivative_formula=self.dI)
        recovered_calculator = EulerApproximation(value=self.recovered, derivative_formula=self.dR)
        dead_calculator = EulerApproximation(value=self.dead, derivative_formula=self.dD)
        while self.susceptible > 1 and self.infected > 1:
            if self.paused:
                plt.pause(0.2)
                continue
            susceptible = susceptible_calculator()
            infected = infected_calculator()
            recovered = recovered_calculator()
            dead = dead_calculator()

            ds.append(infected_calculator.derivative)
            # if graph.time: print(f"I({self.susceptible}) = {i.derivative/s.derivative} @ t={graph.time}, I={infected}")
            graph.susceptible = self.susceptible = susceptible
            graph.infected = self.infected = infected
            graph.recovered = self.recovered = recovered
            graph.dead = self.dead = dead
            # print(self.susceptible, self.infected, self.recovered)

            graph.time += susceptible_calculator.time_step
            if self.draw:
                graph.draw()
        print(f"Highest rate of Infection ({max(ds)}) @ t={ds.index(max(ds)) + 1}")
        print(f"Total Infected = {self.num_people - self.susceptible}")


class Person:
    antibody_length = 90
    infection_length = 5

    def __init__(self):
        self._infected = False
        self.immune = False
        self.antibody_finish = None
        self.infected_finish = None
        self.dead = False

    @property
    def infected(self):
        return self._infected

    @infected.setter
    def infected(self, value):
        if value and not self.immune and not self.infected:
            self.infected_finish = graph.time + self.infection_length
            self._infected = value
        elif self._infected:
            if random.random() < SimulationModel.death_risk:
                self.dead = True
                SimulationModel.people.remove(self)
            self.immune = True
            self._infected = False
            self.antibody_finish = graph.time + self.antibody_length

    def update(self):
        if self.immune and graph.time > self.antibody_finish:
            self.immune = False
        elif self.infected and graph.time > self.infected_finish:
            self.infected = False

    def interact(self, other):
        if self.infected and random.random() < SimulationModel.infection_risk:
            other.infected = self.infected
        elif other.infected and random.random() < SimulationModel.infection_risk:
            self.infected = other.infected

    @property
    def condition(self):
        return "infected" if self.infected else "recovered" if self.immune else "susceptible"

    def vaccinate(self, success_rate=1, effect_length=300):
        if random.random() < success_rate:
            self.immune = True
            self.antibody_finish = graph.time + effect_length

    def __eq__(self, other):
        return other == self.condition


class SimulationModel:
    draw = True
    paused = False

    infection_risk = 0.5
    death_risk = 0.01
    num_people = 10000
    num_interaction = 5000
    vaccination_rate = 0
    start_infected = 10

    people = []

    def __init__(self):
        self.reset()

    def run(self):
        global graph
        vaccines_available = 0
        while "susceptible" in self.people and "infected" in self.people:
            if self.paused:
                plt.pause(0.2)
                continue
            vaccines_available += self.vaccination_rate
            for person in self.people:
                person.update()
            for interaction in range(self.num_interaction):
                alive = len(self.people)
                r1 = random.randint(0, alive - 1)
                r2 = random.randint(0, alive - 1)
                self.people[r1].interact(self.people[r2])
            while vaccines_available > 1:
                p = self.people[self.people.index("susceptible")]
                p.vaccinate(effect_length=Person.antibody_length)
                vaccines_available -= 1

            graph.time += 1
            graph.susceptible = self.people.count("susceptible")
            graph.infected = self.people.count("infected")
            graph.recovered = self.people.count("recovered")
            graph.dead = self.num_people - len(self.people)

            if self.draw:
                graph.draw()

    def reset(self):
        SimulationModel.people = [Person() for _ in range(self.num_people)]
        # first infection
        for infected_index in range(self.start_infected):
            self.people[infected_index].infected = True


class Grapher:
    speed = 1
    plt.ylim(0, CalculusModel.num_people)

    def __init__(self):
        self.time = 0
        self.s_plot, = plt.plot([0], [0], label="Susceptible")
        self.s = list()

        self.i_plot, = plt.plot([0], [0], label="Infected")
        self.i = list()

        self.r_plot, = plt.plot([0], [0], label="Immune")
        self.r = list()

        self.d_plot, = plt.plot([0], [0], label="Dead")
        self.d = list()

    def clear(self):
        self.s = list()
        self.i = list()
        self.r = list()
        self.d = list()
        self.time = 0

    def update_graphs(self):
        x = list(range(self.time))
        self.s_plot.set_xdata(x)
        self.i_plot.set_xdata(x)
        self.r_plot.set_xdata(x)
        self.d_plot.set_xdata(x)
        self.s_plot.set_ydata(self.s)
        self.i_plot.set_ydata(self.i)
        self.r_plot.set_ydata(self.r)
        self.d_plot.set_ydata(self.d)
        plt.xlim(0, self.time)

    def draw(self):
        self.update_graphs()
        plt.legend()
        plt.draw()
        plt.pause(.02 / self.speed)

    @property
    def susceptible(self):
        return self.s[-1]

    @susceptible.setter
    def susceptible(self, value):
        self.s.append(value)

    @property
    def infected(self):
        return self.i[-1]

    @infected.setter
    def infected(self, value):
        self.i.append(value)

    @property
    def recovered(self):
        return self.r[-1]

    @recovered.setter
    def recovered(self, value):
        self.r.append(value)

    @property
    def dead(self):
        return self.d[-1]

    @dead.setter
    def dead(self, value):
        self.d.append(value)


graph = Grapher()
if __name__ == '__main__':
    sim = CalculusModel()
    sim.run()
    plt.ioff()
    print(f"Total Deaths: {graph.dead}")
    print(f"Max Infections: {max(graph.i)}")
    for index, (s, i, r) in enumerate(zip(graph.s, graph.i, graph.r)):
        print(f"{index + 1}: {s, i, r}")
    plt.show()


class DifferentialEquation:
    def __init__(self, equations, variables):
        self.equations = equations
        self.variables = variables

    @classmethod
    def parse(cls, *equations: str, **variables: float):
        parsed = list()
        for equation in equations:
            terms, eq = equation.split('=')

            # manage the left side of the equation - in dy/dx, dy = response & dx = respective
            response, respective = terms.split('/')

            parsed.append([response.strip(), respective.strip(), eq])
        return cls(parsed, variables)

    def step(self, dt):
        new_variables = copy.copy(self.variables)
        for response, respective, equation in self.equations:
            # figure out the respective variables
            delta = dt if respective == "dt" else self.variables[respective[1:]]
            v = response[1:]

            # substitute
            formula = equation
            for variable in self.variables:
                formula = formula.replace(variable, str(self.variables[variable]))

            # calculate
            derivative = eval(formula)

            # apply
            value = self.variables[v]
            value += derivative * delta

            # store
            new_variables[v] = value
        # save for the next step
        self.variables = new_variables



if __name__ == '__main__':
    DifferentialEquation.parse()