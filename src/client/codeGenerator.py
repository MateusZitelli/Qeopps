from parser import Parser, NODE_TYPE
from SyncTable import SYNC_TYPE, SYNC_RW, generate_population

IDENTATION_LEVEL = " " * 4

class Generator:
    def __init__(self, tree, output_file, sync_table=None):
        self.tree = tree
        self.sync_table = sync_table
        self.create_sync_dict()
        self.code_file = open(output_file, "w")
        self.defined_functions = list()
        self.transactions_extra_indentation = 0
        self.used_mutex_names = list()
        self.definitions_writed = False

    def create_sync_dict(self):
        self.sync_dict = {}
        for t in self.sync_table.transactions:
            for s in t.syncs:
                if not s.scope in self.sync_dict:
                    self.sync_dict[s.scope] = [s]
                else:
                    self.sync_dict[s.scope].append(s)

    def write_definitions(self):
        if self.definitions_writed:
            return
        self.definitions_writed = True
        for t in self.sync_table.transactions:
            for s in t.syncs:
                if s.rw == 0:
                    rw_text = "read"
                elif s.rw == 1:
                    rw_text = "write"
                mutex_text = "mutex_%s_%s" % (rw_text, s.variable)
                if mutex_text in self.used_mutex_names:
                    n = len([m for m in self.used_mutex_names if m == mutex_text])
                    self.used_mutex_names.append(mutex_text)
                    mutex_text += str(n)
                else:
                    self.used_mutex_names.append(mutex_text)
                mutex_string = "pthread_mutex_t %s = PTHREAD_MUTEX_INITIALIZER;"\
                    % (mutex_text)
                s.text = mutex_text
                self.code_file.write(mutex_string + "\n")

    def write_lines(self, node, last_node=None):
        #For each command in the block
        if node in self.sync_dict:
            for s in self.sync_dict[node]:
                identation = IDENTATION_LEVEL * (node.depth + self.transactions_extra_indentation)
                if s.type == SYNC_TYPE["mutex"]:
                    if s.rw == SYNC_RW["read"]:
                        lock_string = "lock(&"
                    elif s.rw == SYNC_RW["write"]:
                        lock_string = "lock(&"
                    sync_string = "pthread_mutex_" + lock_string + s.text + ");"
                elif s.type == SYNC_TYPE["stm"]:
                    #TODO
                    #sync_string = "__transaction_atomic{"
                    sync_string = "{"
                    self.transactions_extra_indentation += 1
                line_string = identation + sync_string
                self.code_file.write(line_string + "\n")

        for n in node.childs:
            if not "#" in n.data[1]:
                self.write_definitions()
            #if the node contain a function
            if n.data[0] == NODE_TYPE["FUNCTION_NODE"]:
                #if the function is already defined, print the calling and
                #go to the next node
                if n.data[2] in self.defined_functions:
                    comment = " //defined as %s" % n.data[1]
                    self.code_file.write(IDENTATION_LEVEL * (last_node.depth + 1) +
                                         n.data[3] + ";" + comment + "\n")
                    continue
                #else add the function to the defined functions list
                self.defined_functions.append(n.data[2])
            #if the node is a block
            if len(n.childs) > 0:
                self.code_file.write(IDENTATION_LEVEL * (n.depth + self.transactions_extra_indentation - 1) + n.data[1] + "{\n")
                self.write_lines(n, node)
            else:
                if "#" == n.data[1][0]:
                    self.code_file.write(IDENTATION_LEVEL * (n.depth + self.transactions_extra_indentation - 1) + n.data[1] + "\n")
                else:
                    self.code_file.write(IDENTATION_LEVEL * (n.depth + self.transactions_extra_indentation - 1) + n.data[1] + ";\n")
            if len(n.childs) > 0:
                self.code_file.write(IDENTATION_LEVEL * (n.depth + self.transactions_extra_indentation - 1) + "}" + "\n")

        if node in self.sync_dict:
            for s in self.sync_dict[node][::-1]:
                if s.type == SYNC_TYPE["mutex"]:
                    sync_string = "pthread_mutex_unlock(&" + s.text + ");"
                elif s.type == SYNC_TYPE["stm"]:
                    sync_string = "}"
                    self.transactions_extra_indentation -= 1
                identation = IDENTATION_LEVEL * (node.depth + self.transactions_extra_indentation)
                line_string = identation + sync_string
                self.code_file.write(line_string + "\n")

    def generate_code(self):
        # self.write_definitions()
        self.write_lines(self.tree.root)
        self.code_file.close()

if __name__ == "__main__":
    p = Parser("examples/teste2.c")
    p.parse()
    np = generate_population(p.syncTable, 20, 200, 200)
    for i, j in enumerate(np):
        g = Generator(p.tree, "examples/code%i.c" % (i), j)
        g.generate_code()
