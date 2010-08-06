#    This file is part of EAP.
#
#    EAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    EAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with EAP. If not, see <http://www.gnu.org/licenses/>.

import sys
import random
import copy

sys.path.append("..")

from eap import base
from eap import creator
from eap import toolbox

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
creator.create("Population", list)

tools = toolbox.Toolbox()

# Attribute generator
tools.register("attr_bool", random.randint, 0, 1)

# Structure initializers
tools.register("individual", creator.Individual, content_init=tools.attr_bool, size_init=100)
tools.register("pop", creator.Population, content_init=tools.individual, size_init=300)

def evalOneMax(individual):
    return sum(individual),

tools.register("evaluate", evalOneMax)
tools.register("mate", toolbox.cxTwoPoints)
tools.register("mutate", toolbox.mutFlipBit, indpb=0.05)
tools.register("select", toolbox.selTournament, tournsize=3)

if __name__ == "__main__":
    random.seed(64)
    
    pop = tools.pop()
    CXPB, MUTPB, NGEN = 0.5, 0.2, 40
    
    # Evaluate the entire pop
    for ind in pop:
        ind.fitness.values = tools.evaluate(ind)
    
    # Begin the evolution
    for g in range(NGEN):
        print "-- Generation %i --" % g
    
        # Select the next generation individuals
        offsprings = tools.select(pop, n=len(pop))
        # Clone the selected individuals
        offsprings = [copy.deepcopy(ind) for ind in offsprings]    
    
        # Apply crossover and mutation
        for ind1, ind2 in zip(offsprings[::2], offsprings[1::2]):
            if random.random() < CXPB:
                tools.mate(ind1, ind2)
                del ind1.fitness.values
                del ind2.fitness.values
    
        for ind in offsprings:
            if random.random() < MUTPB:
                tools.mutate(ind)
                del ind.fitness.values
    
        # Evaluate the individuals with an invalid fitness
        for ind in offsprings:
            if not ind.fitness.valid:
                ind.fitness.values = tools.evaluate(ind)
        
        # The pop is entirely replaced by the offsprings
        pop = offsprings
        
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(map(lambda x: x**2, fits))
        std_dev = abs(sum2 / length - mean**2)**0.5
        
        print "  Min %s" % min(fits)
        print "  Max %s" % max(fits)
        print "  Avg %s" % mean
        print "  Std %s" % std_dev
    
    print "-- End of (successful) evolution --"
    
    best_ind = toolbox.selBest(pop, 1)[0]
    print "Best individual is %s, %s" % (best_ind, best_ind.fitness.values)
