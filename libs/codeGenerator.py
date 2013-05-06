from parser import Parser, NODE_TYPE
from SyncTable import SYNC_TYPE, SYNC_RW
class Generator:
    def __init__(self, tree, output_file, sync_table = None):
        self.tree = tree
        self.sync_table = sync_table
        self.create_sync_dict()
        self.code_file = open(output_file, "w")
        self.defined_functions = list()

    def create_sync_dict(self):
        self.sync_dict = {}
        for t in self.sync_table.transactions:
            for s in t.syncs:
                if not s.scope in self.sync_dict:
                    self.sync_dict[s.scope] = [s]
                else:
                    self.sync_dict[s.scope].append(s)

    def write_lines(self, node, last_node = None):
        #For each command in the block
        if node in self.sync_dict:
            for s in self.sync_dict[node]:
                identation = "    " * (node.depth)
                if s.type == SYNC_TYPE["mutex"]:
                    if s.rw == SYNC_RW["read"]:
                        lock_string = "rlock("
                    elif s.rw == SYNC_RW["write"]:
                        lock_string = "wlock("
                    sync_string = "mutex_" + lock_string + s.variable + ")"
                line_string = identation + sync_string
                self.code_file.write(line_string + ";\n")
        for n in node.childs:
            #if the node contain a function
            if n.data[0] == NODE_TYPE["FUNCTION_NODE"]:
                #if the function is already defined, print the calling and
                #go to the next node
                if n.data[2] in self.defined_functions:
                    comment = " //defined as %s" % n.data[1]
                    self.code_file.write("    " * (last_node.depth + 1) +\
                                         n.data[3] + ";" + comment + "\n")
                    continue
                #else add the function to the defined functions list and
                #print all the function definition
                self.defined_functions.append(n.data[2])
            #if the node is a block
            if len(n.childs) > 0:
                self.code_file.write("    "* (n.depth - 1) + n.data[1] + "{\n")
            else:
                self.code_file.write("    "* (n.depth - 1) + n.data[1] + ";\n")
            self.write_lines(n, node)
            if len(n.childs) > 0:
                self.code_file.write("    " * (n.depth - 1) + "}" + "\n")
        if node in self.sync_dict:
            for s in self.sync_dict[node]:
                identation = "    " * (node.depth)
                sync_string = "mutex_unlock(" + s.variable + ")"
                line_string = identation + sync_string
                self.code_file.write(line_string + ";\n")

    def generate_code(self):
        self.write_lines(self.tree.root)
        self.code_file.close()

if __name__ == "__main__":
    p = Parser("examples/teste2.c")
    p.parse()
    g = Generator(p.tree, "examples/code.c", p.syncTable)
    g.generate_code()
