# Jan 15, 2020
from random import *
from math import *
import pygame

pygame.init()

window_height = 500
window_width = 500
window = pygame.display.set_mode((window_width, window_height))

Black = (0, 0, 0)
White = (255, 255, 255)
Gray = (128, 128, 128)
RED = (255, 0, 0)
Aqua = (0, 128, 208)
Blue = (0, 0, 128)
Green = (0, 255, 0)
Orange = (255, 165, 0)
Yellow = (255, 255, 0)


class Person:
    vaccinated_color = Yellow
    infected_color = RED
    unvaccinated_color = Gray
    immune_color = Green
    radius = 10
    meet_dis = 25
    speed = 5
    all_people = []

    def __init__(self):
        self.infected = False
        self.vaccinated = vaccination_rate > random()
        self.effective_vaccination = vaccination_efficacy > random() and self.vaccinated
        self.immune = False
        self.x = randint(0, window_width)
        self.y = randint(0, window_height)
        self.color = self.vaccinated_color if self.vaccinated else self.unvaccinated_color
        self.time_left_infected = None
        self.met_partner = False
        self.partner = None
        self.all_people.append(self)

    def infect(self, endurance):
        self.infected = True
        self.time_left_infected = endurance
        self.color = self.infected_color

    def check_met(self):
        met = sqrt((self.x - self.partner.x) ** 2 + (self.y - self.partner.y) ** 2) < self.meet_dis
        self.met_partner = met
        return met

    def goto_partner(self):
        self.goto(self.partner.x, self.partner.y)

    def goto(self, x, y):
        dx = x - self.x
        dy = y - self.y
        if sqrt(dx**2 + dy**2) < self.meet_dis:
            return
        angle = atan(dx / dy) if dy != 0 else radians(90) if dx > 0 else radians(270)
        angle += pi if dy < 0 else 0
        self.x += sin(angle) * self.speed
        self.y += cos(angle) * self.speed

    def interact(self, other):
        if other.infected:
            if not (self.effective_vaccination or self.immune or self.infected):
                self.infect(people_encountered)
                return True
        return False

    def update(self):
        if self.infected:
            self.time_left_infected -= 1
            if self.time_left_infected <= 0:
                self.infected = False
                self.immune = True
                self.color = self.immune_color
        self.partner = None

    def draw(self):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius)
        if self.partner is not None:
            pygame.draw.line(window, Green, (int(self.x), int(self.y)), (int(self.partner.x), int(self.partner.y)))

    def __repr__(self):
        try:
            return f"Person #{self.all_people.index(self) + 1}"
        except ValueError:
            return "impossible person"


class Sim:
    background_color = Aqua

    def __init__(self, population_size, intial_infect, endurance):
        self.pop = []
        self.amount_vaccinated = 0
        self.amount_unvaccinated = 0
        for i in range(population_size):
            new = Person()
            if i < intial_infect:
                new.infect(endurance)
            elif new.vaccinated:
                self.amount_vaccinated += 1
            else:
                self.amount_unvaccinated += 1
            self.pop.append(new)
        self.unvaccinated_infection_amount = 0
        self.vaccinated_infection_amount = 0
        self.turns = 0
        # print(Person.all_people)

    def run_visual_sim(self):
        while True in [person.infected for person in self.pop]:
            self.turns += 1
            self.tick()
            self.draw()
        self.print_summary()
        while True:
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    print("bye")
                    quit()

    # sim without the drawing
    def run_virtual_sim(self):
        while True in [person.infected for person in self.pop]:
            self.turns += 1
            self.virtual_tick()
        self.print_summary()

    def virtual_tick(self):
        pairs = self.get_pairs()
        self.interact(pairs)
        for p in self.pop:
            p.update()

    def tick(self):
        pairs = self.get_pairs()
        self.move_together()
        self.interact(pairs)
        self.draw()
        for p in self.pop:
            p.update()
        self.seperate()

    def interact(self, pairs):
        for p1, p2 in pairs:
            i1 = p1.interact(p2)
            i2 = p2.interact(p1)
            if i1 and p1.vaccinated:
                self.vaccinated_infection_amount += 1
            elif i1 and not p1.vaccinated:
                self.unvaccinated_infection_amount += 1
            if i2 and p2.vaccinated:
                self.vaccinated_infection_amount += 1
            elif i2 and not p2.vaccinated:
                self.unvaccinated_infection_amount += 1

    def get_pairs(self):
        nums = [i for i in range(len(self.pop))]
        pairs = []
        shuffle(nums)
        while len(nums) > 1:
            person1 = self.pop[nums.pop(1)]
            person2 = self.pop[nums.pop(0)]
            person1.partner = person2
            person2.partner = person1
            # print(pop)
            pairs.append((person1, person2))
        if len(nums) == 1:
            self.pop[nums[0]].partner = self.pop[nums[0]]
        return pairs

    def move_together(self):
        have_updated = True
        while have_updated:
            have_updated = False
            for person in self.pop:
                if not person.check_met():
                    have_updated = True
                    person.goto_partner()
            self.draw()

    def seperate(self):
        seperation_amount = 50
        random_cords = [(randint(0, window_width), randint(0, window_height)) for i in range(len(self.pop))]
        for i in range(seperation_amount):
            for target, p in zip(random_cords, self.pop):
                x, y = target
                p.goto(x, y)
            self.draw()

    def draw(self):
        for event in pygame.event.get():
            if event == pygame.QUIT:
                print("quitting")
                quit()
        window.fill(self.background_color)
        for person in self.pop:
            person.draw()
            # print(person.x, person.y)
        pygame.display.update()

    def print_summary(self):
        print(f"There were {self.turns} amount of days until the infection went away")
        print(f"{self.vaccinated_infection_amount} out of {self.amount_vaccinated} vaccinated people were infected")
        print(f"{self.unvaccinated_infection_amount} out of {self.amount_unvaccinated} unvaccinated people were infected")

if __name__ == '__main__':
    vaccination_rate = .8
    vaccination_efficacy = 0.67
    people_encountered = 5
    intial_amount_of_infected = 1
    population_size = 100
    sim = Sim(population_size, intial_amount_of_infected, people_encountered)
    sim.run_virtual_sim()