import random, copy
import Tree
class Sync:
    def __init__(self, sync_type, variables, scope):
        self.sync_type = sync_type
        self.variables = list(variables)
        self.scope = scope

    def mutate_type(self):
        self.sync_type = random.randrange(2)

    def mutate_scope(self, move_up = None):
        if(move_up == None):
            move_up = random.randrange(2)
        if(move_up and self.scope.parent != None):
            self.scope = self.scope.parent
        elif(len(self.scope.childs)):
            self.scope = random.choice(self.scope.childs)
            
class Transaction:
    def __init__(self, syncs):
        self.syncs = list(syncs)
        self.size = len(self.syncs)

    def mutate_scope(self):
        move_up = random.randrange(2)
        for s in self.syncs:
            s.mutate_scope(move_up)
        

class SyncTable:
    def __init__(self, transactions):
        self.transactions = list(transacations)
        self.size = len(self.transactions)

    def mutate(self, mutation_type = None):
        if(mutation_type == None):
            mutation_type = random.randrange(3)
        if(mutation_type == 0):
            target_transaction = random.choice(self.transactions)
            target_sync = random.choice(target_transaction.syncs)
            target_sync.mutate_type()
        elif(mutation_type == 1):
            target_transaction = random.choice(self.transactions)
            target_sync = random.choice(target_transaction.syncs)
            target_sync.mutate_scope()
        elif(mutation_type == 2):
            target_transaction = random.choice(self.transactions)
            target_transaction.mutate_scope()

    def cross_over(self, other):
        min_table_size = min(self.size, other.size)
        cut_point = random.randrange(0, min_table_size)
        slices = [self.transactions[0:cut_point],\
            self.transactions[cut_point:],\
            other.transactions[0:cut_point],\
            other.transactions[cut_point:]]
        if(random.randrange(2)):
            new_tables = [SyncTable(slices[0] + slices[2]),\
                SyncTable(slices[1] + slices[3])]
        else:
            new_tables = [SyncTable(slices[2] + slices[0]),\
                SyncTable(slices[3] + slices[1])]
	return new_tables

def generate_population(base_table, population_size,\
    scope_mutations, type_mutations):
    for i in range(population_size):
        population.append(copy.deepcopy(base_table))
    for table in population:
        for i in range(scope_mutations):
            table.mutate(random.randint(1,2))
        for i in range(type_mutations):
            table.mutate(0)
    return population


    
