import random
import Tree
class Sync:
    def __init__(self, sync_type, variables, scope):
        self.sync_type = sync_type
        self.variables = list(variables)
        self.scope = scope

    def mutate_type(self):
        self.sync_type = random.randrange(2)

    def mutate_scope(self):
        if(random.randrange(2) and self.scope.parent != None):
            self.scope = self.scope.parent
        elif(len(self.scope.childs)):
            self.scope = random.choice(self.scope.childs)
            
class Transaction:
    def __init__(self, syncs):
        self.syncs = list(syncs)
        self.size = len(self.syncs)

class SyncTable:
    def __init__(self, transactions):
        self.transactions = list(transacations)
        self.size = len(self.transactions)

    def mutate(self):
        mutation_type = random.randrange(3)
        if(mutation_type == 0):
            target_transaction = random.choice(self.transactions)
            target_sync = random.choice(target_transaction.syncs)
            target_sync.mutate_type()
        if(mutation_type == 1):
            target_transaction = random.choice(self.transactions)
            target_sync = random.choice(target_transaction.syncs)
            target_sync.mutate_scope()
