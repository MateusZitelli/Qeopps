from libs.codeGenerator import Generator
from libs.SyncTable import generate_population
from libs.parser import Parser
from libs.fitness import Fitness
from libs.utils import *
from time import sleep
import re

class Solution:
    def __init__(self, table):
        self.table = table
        self.fitness = None

class Queopps:
    def __init__(self, aim_program_file_name, config_file_name):
        self.aim_program_file_name = aim_program_file_name
        self.config_file = open(config_file_name, 'r')
        self.get_config()
        self.parser = Parser(self.aim_program_file_name)
        self.population_dir = self.settings["population_programs_dir"]

    def get_config(self):
        self.settings = dict()
        for line in self.config_file.readlines():
            line_match_int_value = re.match(r'\s*(.+):(\d+)$', line)
            if line_match_int_value:
                setting = line_match_int_value.group(1)
                value = int(line_match_int_value.group(2))
                self.settings[setting] = value
                continue
            line_match_float_value = re.match(r'\s*(.+):(\d+.\d+)$', line)
            if line_match_float_value:
                setting = line_match_float_value.group(1)
                value = float(line_match_float_value.group(2))
                self.settings[setting] = value
                continue
            line_match_string_value = re.match(r'\s*(.+):(.+)', line)
            if line_match_string_value:
                setting = line_match_string_value.group(1)
                value = line_match_string_value.group(2)
                self.settings[setting] = value

    def must_stop(self):
        if "max_generations" in self.settings:
            if self.settings["max_generations"] < self.generation:
                return True

    def generate_new_population(self):
      population_size = self.settings["population_size"]
      self.population = sorted(self.population,
                                key=lambda x: x.fitness)[:population_size]
      new_solutions = 0
      for i in xrange(population_size):
        copy = None
        if probability(self.settings["mutation_probability"]):
          solution_index = getLinearDistributedIndex(population_size)
          copy = self.population[solution_index].table.get_copy()
          copy.mutate()
        # if probability(self.settings["crossingover_probability"]):
        #   if copy == None:
        #     solution_index = getLinearDistributedIndex(population_size)
        #     copy = self.population[solution_index].table.get_copy()
        #   other_index = getLinearDistributedIndex(population_size)
        #   other_table = self.population[other_index].table
        #   copy = copy.cross_over(other_table)
        if copy != None:
          new_solutions += 1
          self.population[population_size - new_solutions] = Solution(copy)

    def run(self):
        self.generation = 0
        while True:
            print 'Generation %i' % (self.generation)
            for i, solution in enumerate(self.population):
                file_name = self.population_dir + "Queopps_son" + str(i) + ".c"
                code_generator = Generator(self.parser.tree, file_name,
                    solution.table)
                code_generator.generate_code()
                compiler_string = self.settings["compiler_string"]
                compiler_flags = self.settings["compiler_flags"]
                server_host = self.settings["server_host"]
                print server_host
                f = Fitness(file_name, compiler_string, compiler_flags, server_host)
                print f.benchmark()
            self.generate_new_population()
            self.generation += 1
            if self.must_stop():
                break

    def start_optimization(self):
        self.parser.parse()
        init_pop_size = self.settings["init_population_size"]
        scope_mutations = self.settings["init_population_scope_mutations"]
        type_mutations = self.settings["init_population_type_mutations"]
        table_population = generate_population(self.parser.syncTable,
            init_pop_size, scope_mutations, type_mutations)
        self.population = [Solution(t) for t in table_population]
        self.run()


q = Queopps("./Programs/nbody.c", "test.cfg")
q.start_optimization()
