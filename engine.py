import random
from deap import base, creator, tools
import numpy
import logging

from util import fitness


class Engine():
    means = None
    stdevs = None
    toolbox = None
    cross_probability = 0.5
    mutation_probability = 0.1
    max_generation = 200
    acceptable_mean = None
    init_generation_size = 300
    pop = None
    fits = None
    def __init__(self, means, stdevs, max_allowed, acceptable_mean, tournament_size=3, mutate_mu=10, mutate_sigma=5):
        self.means = means
        self.stdevs = stdevs
        self.acceptable_mean = acceptable_mean
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        self.toolbox = base.Toolbox()
        self.toolbox.register("attr_val", random.uniform, 0, max([(m+3*s) for m,s in zip(means,stdevs)]))
        self.toolbox.register("individual",tools.initRepeat,creator.Individual,self.toolbox.attr_val,n=len(means))
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", fitness, mean=means, stdev=stdevs, maxAllowed=max_allowed)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutGaussian, mu=mutate_mu, sigma=mutate_sigma, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=tournament_size)

    def _set_fitness(self, population):
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitnesses = map(self.toolbox.evaluate, invalid_ind)
        for individual, fitness in zip(invalid_ind, fitnesses):
            logging.info("fitness %s for individual %s", fitness, individual)
            individual.fitness.values = fitness

    def initialize(self):
        self.pop = self.toolbox.population(n=self.init_generation_size)
        self._set_fitness(self.pop)

    def run(self):
        g = 0
        mean = -500
        while g < self.max_generation and mean < self.acceptable_mean:
            g = g + 1
            logging.info("-- Generation %i --" % g)
            offspring = self.toolbox.select(self.pop, len(self.pop))
            offspring = list(map(self.toolbox.clone, offspring))
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < self.cross_probability:
                    self.toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values
            for mutant in offspring:
                if random.random() < self.mutation_probability:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values
            self._set_fitness(offspring)
            self.pop[:] = offspring
            self.fits = [ind.fitness.values[0] for ind in self.pop]
            length = len(self.pop)
            mean = sum(self.fits) / length
            sum2 = sum(x*x for x in self.fits)
            std = abs(sum2 / length - mean**2)**0.5
            logging.info("  Min %s" % min(self.fits))
            logging.info("  Max %s" % max(self.fits))
            logging.info("  Avg %s" % mean)
            logging.info("  Std %s" % std)

    def fittest(self):
        if self.pop == None or self.fits == None:
            return None
        return self.pop[numpy.argmax(self.fits)]

    def argfittest(self):
        if self.pop == None or self.fits == None:
            return None
        return numpy.argmax(self.fits)
