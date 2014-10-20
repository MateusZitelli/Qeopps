import random, copy
import Tree

SYNC_TYPE = {"mutex":0, "stm":1}
SYNC_RW = {"read":0, "write":1, "read_vector":0, "write_vector":1}
MUTATION_TYPES = {"TYPE":0, "SINGLE_SYNC_SCOPE":1, "TRANSACTION_SCOPE":2}

class Sync:
    def __init__(self, sync_type, variable, scope, sync_rw):
        """sync_type -> 0 - Mutex, 1 - STM
        variables -> List of variables
        scope -> Scope of the sync
        sync_rw -> 0 - read, 1 - write"""
        self.type = sync_type
        self.variable = variable
        self.scope = scope
        self.init_depth = scope.depth
        self.rw = sync_rw
        self.text = None

    def mutate_type(self):
        #TODO
        return
        self.type = random.randrange(2)

    def mutate_scope(self, move_up = None):
        childs_quant = len(self.scope.childs)
        if(move_up == None):
            move_up = random.randrange(2)
        if(move_up and self.scope.depth > 1):
            self.scope = self.scope.parent
        elif(childs_quant and self.init_depth > self.scope.depth):
            self.scope = random.choice(self.scope.childs)

    def get_copy(self):
        new_sync = Sync(self.type, self.variable, self.scope, self.rw)
        return new_sync

class Transaction:
    def __init__(self, syncs = None):
        if syncs == None:
            self.syncs = list()
        else:
            self.syncs = list(syncs)
        self.size = len(self.syncs)

    def mutate_scope(self):
        move_up = random.randrange(2)
        for s in self.syncs:
            s.mutate_scope(move_up)

    def get_copy(self):
        new_transaction = Transaction()
        for s in self.syncs:
            new_transaction.syncs.append(s.get_copy())
        return new_transaction


class SyncTable:
    def __init__(self, transactions=None):
        if transactions is not None:
            self.transactions = list(transactions)
        else:
            self.transactions = list()
        self.size = len(self.transactions)

    def mutate(self, mutation_type=None):
        if self.size == 0:
            return
        if mutation_type is None:
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
        cut_point = 0
        if min_table_size > 0:
            cut_point = random.randrange(0, min_table_size)
        slices = [self.transactions[0:cut_point],
            self.transactions[cut_point:],
            other.transactions[0:cut_point],
            other.transactions[cut_point:]]
        if(random.randrange(2)):
            new_tables = [SyncTable(slices[0] + slices[2]),
                SyncTable(slices[1] + slices[3])]
        else:
            new_tables = [SyncTable(slices[2] + slices[0]),
                SyncTable(slices[3] + slices[1])]
        return new_tables

    def viable(self):
        for t in self.transactions:
            if not t.viable():
                return False
        return True

    def addTransaction(self, transaction):
        self.transactions.append(transaction)
        self.size += 1

    def get_copy(self):
        new_table = SyncTable()
        for t in self.transactions:
            new_table.addTransaction(t.get_copy())
        return new_table

def generate_population(base_table, population_size,\
    scope_mutations, type_mutations):
    if len(base_table.transactions) == 0:
        return []
    population = list()
    for i in range(population_size):
        population.append(base_table.get_copy())
    for table in population:
        for i in range(scope_mutations):
            table.mutate(random.randint(MUTATION_TYPES["SINGLE_SYNC_SCOPE"],
                                        MUTATION_TYPES["TRANSACTION_SCOPE"]))
        for i in range(type_mutations):
            table.mutate(MUTATION_TYPES["TYPE"])
    return population
