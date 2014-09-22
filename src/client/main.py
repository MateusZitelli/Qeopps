from libs.codeGenerator import Generator
from libs.SyncTable import generate_population
from libs.parser import Parser
from libs.fitness import Fitness
from libs.utils import *
from time import sleep
import re


pattern_int_config = r'\s*(.+):(\d+)$'
pattern_float_config = r'\s*(.+):(\d+.\d+)$'
pattern_string_config = r'\s*(.+):(.+)'
class Solution:
    def __init__(self, table):
        self.table = table
        self.fitness = None

class Qeopps:
    """Create the enviroment for the optimizations based on the config file."""
    def __init__(self, aim_program_file_name, config_file_name):
        self.aim_program_file_name = aim_program_file_name
        self.config_file = open(config_file_name, 'r')
        self.get_config()
        self.parser = Parser(self.aim_program_file_name)
        self.population_dir = self.settings["population_programs_dir"]

    def get_config(self):
        """Loads data from the configuration file"""
        self.settings = dict()
        for line in self.config_file.readlines():
            line_match_int_value = re.match(pattern_int_config, line)
            line_match_float_value = re.match(pattern_float_config, line)
            line_match_string_value = re.match(pattern_string_config, line)
            if line_match_int_value:
                setting = line_match_int_value.group(1)
                value = int(line_match_int_value.group(2))
            elif line_match_float_value:
                setting = line_match_float_value.group(1)
                value = float(line_match_float_value.group(2))
            elif line_match_string_value:
                setting = line_match_string_value.group(1)
                value = line_match_string_value.group(2)
            else:
                continue
            self.settings[setting] = value

    def must_stop(self):
        """Returns if the end of the optimization was reached"""
        if "max_generations" in self.settings:
            if self.settings["max_generations"] < self.generation:
                return True

    def add_individual(self, individual):
        """ Add an individual to the population"""
        if(type(individual) is list):
            for i in individual:
                self.population.append(Solution(i))
        else:
            self.population.append(Solution(individual))

    def update_population(self):
        """ Update the popuation, removing the bad solutions and adding new
        individuals after mutations and crossing-over """
        population_size = self.settings["population_size"]
        self.population = sorted(self.population,
                                 key=lambda x: x.fitness)[:population_size]
        for i in xrange(population_size):
          child = None
          # Mutate
          if probability(self.settings["mutation_probability"]):
            solution_index = getLinearDistributedIndex(population_size)
            child = self.population[solution_index].table.get_copy()
            child.mutate()
            self.add_individual(child)
          # Crossover
          if probability(self.settings["crossingover_probability"]):
            # Create a child if there is no child yet
            if child == None:
              solution_index = getLinearDistributedIndex(population_size)
              child = self.population[solution_index].table.get_copy()
            other_index = getLinearDistributedIndex(population_size)
            other_table = self.population[other_index].table
            # The cross_over operation returns 2 solutions
            for c in child.cross_over(other_table):
                self.add_individual(c)

    def run(self):
        """ Run the optimization """
        self.generation = 0
        while True:
            print 'Generation %i' % (self.generation)
            for i, solution in enumerate(self.population):
                file_name = self.population_dir + "Qeopps_son" + str(i) + ".c"
                code_generator = Generator(self.parser.tree, file_name,
                    solution.table)
                code_generator.generate_code()
                compiler_string = self.settings["compiler_string"]
                compiler_flags = self.settings["compiler_flags"]
                server_host = self.settings["server_host"]
                f = Fitness(file_name, compiler_string, compiler_flags, server_host)
                print f.benchmark()
            self.update_population()
            self.generation += 1
            if self.must_stop():
                break

    def start_optimization(self):
        """ Configure the initial scenario and run the optimization """
        self.parser.parse()
        init_pop_size = self.settings["init_population_size"]
        scope_mutations = self.settings["init_population_scope_mutations"]
        type_mutations = self.settings["init_population_type_mutations"]
        table_population = generate_population(self.parser.syncTable,
            init_pop_size, scope_mutations, type_mutations)
        self.population = [Solution(t) for t in table_population]
        self.run()


q = Qeopps("./Programs/nbody.c", "test.cfg")
q.start_optimization()
