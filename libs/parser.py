import Tree
from SyncTable import *
import re

NODE_TYPE = {"NORMAL_NODE":0, "FUNCTION_NODE": 1}
VERBOSE = 0
class Tag:
    def __init__(self, read_vars, write_vars):
        self.rvars = read_vars
        self.wvars = write_vars

class Parser:
    def __init__(self, filename):
        f = open(filename, "rU")
        self.text = re.sub(r"([\{\}])", r"\1;", f.read()).replace("*/", "*/;")
        self.commands = self.text.split(";")
        f.close()
        self.tree = Tree.Tree(Tree.TreeNode("program"))
        self.tags = list()
        self.syncTable = SyncTable()
        self.functions = dict()

    def parse(self, current_node = None):
        if(current_node == None):
            current_node = self.tree.root
        next_commands_already_parseds = 0
        for i, j in enumerate(self.commands):
            if next_commands_already_parseds > 0:
                next_commands_already_parseds -= 1
                continue
            #Parse end of a period
            match_end_period = re.match(r'\s*}', j)
            if match_end_period:
                current_node = current_node.parent
                continue

            #Parse multiline if/switch/while
            operation_match = re.match(r'\s*(if|switch|while)\s*\(\s*(.*)\s*\)[\s\n]*{', j)
            if operation_match:
                operation_string = "%s(%s)" % (operation_match.group(1), operation_match.group(2))
                if VERBOSE: print current_node.depth * " ", operation_string
                new_node = self.tree.new_node((NODE_TYPE["NORMAL_NODE"], operation_string), current_node)
                current_node = new_node
                continue

            #Parse Queopps optimization tag
            match_Queopps_tag = re.match(r'\s*/\*\s*Queopps-TAG\s*(read|write)\s*\((.*?)\)\s*(read|write)\s*\((.*?)\)\s*\*/', j)
            if match_Queopps_tag:
                syncs = list()
                for i, j in enumerate(match_Queopps_tag.groups()[::2]):
                    varibles = match_Queopps_tag.groups()[i * 2 + 1].split(",")
                    for var in varibles:
                        var = var.strip(" ")
                        if var == "":
                            continue
                        if VERBOSE: print current_node.depth * " ", "Queopps_tag ->",var, "<->", j
                        s = Sync(SYNC_TYPE["mutex"], var, current_node, SYNC_RW[j])
                        syncs.append(s)
                t = Transaction(syncs)
                self.syncTable.transactions.append(t)
                continue
            #Parse inline while and if
            match_while_inline = re.match(r'\s*(if|while)\(\s*(.*)\)\s*(.*)', j)
            if match_while_inline:
                inline_string = "%s(%s) %s" % (match_while_inline.group(1),match_while_inline.group(2), match_while_inline.group(3))
                if VERBOSE: print current_node.depth * " ", inline_string
                self.tree.new_node((NODE_TYPE["NORMAL_NODE"],inline_string), current_node)
                continue

            #Parse inline and multiline for loops
            match_for = re.match(r'\s*for\((.*)', j)
            if match_for:
                #Get the nexts args of the for in the nexts commands
                for_arg_quant = 1
                match_last_for_inline_arg = None
                match_last_for_arg = None
                args = [match_for.group(1)]
                while not match_last_for_inline_arg and not match_last_for_arg:
                    args.append(self.commands[i + for_arg_quant])
                    for_arg_quant += 1
                    arg_line = self.commands[i + for_arg_quant]
                    match_last_for_inline_arg = re.match(r'(.*?)\)\s*(.*)', arg_line)
                    match_last_for_arg = re.match(r'(.*?)\)[\s\n]*{', arg_line)
                    next_commands_already_parseds += 1
                next_commands_already_parseds += 1
                if match_last_for_arg:
                    args.append(match_last_for_arg.group(1))
                    args_string = ";".join(args)
                    for_string = "for(%s)" % (args_string)
                    if VERBOSE: print current_node.depth * " ", for_string
                    for_node = self.tree.new_node((NODE_TYPE["NORMAL_NODE"],for_string), current_node)
                    current_node = for_node

                elif match_last_for_inline_arg:
                    args.append(match_last_for_inline_arg.group(1))
                    args_string = ";".join(args)
                    for_inline_string = "for(%s) %s" % (args_string, match_last_for_inline_arg.group(2))
                    if VERBOSE: print current_node.depth * " ", for_inline_string
                    self.tree.new_node((NODE_TYPE["NORMAL_NODE"],for_inline_string), current_node)
                continue

            #Parse functions definitions
            match_functions = re.match(r'\s*(.+)\s+(.*)\((.*)\)[\s\n]*{', j)
            if match_functions:
                return_type = match_functions.group(1)
                function_name = match_functions.group(2)
                args = match_functions.group(3)
                func_string = "%s %s(%s)" % (return_type, function_name, args)
                func_node = self.tree.new_node([NODE_TYPE["FUNCTION_NODE"],func_string, function_name], current_node)
                if VERBOSE: print current_node.depth * " ", func_string
                current_node = func_node
                self.functions[function_name] = func_node
                continue

            #Parse fuctions calls
            match_function_call = re.match(r'\s*(.+)\((.*)\)', j)
            if match_function_call and match_function_call.group(1) in self.functions:
                function_name = match_function_call.group(1)
                args = match_function_call.group(2)
                function_node = self.functions[function_name]
                function_string = "%s(%s)" % (function_name, args)
                function_node.data.append(function_string)
                current_node.childs.append(function_node)
                continue
            #Parse command lines
            command_match = re.match(r'\s*(.+)', j)
            if command_match:
                command_node = self.tree.new_node((NODE_TYPE["NORMAL_NODE"],command_match.group(1)), current_node)
                if VERBOSE: print current_node.depth * " ",command_match.group(1)
        #self.tree.print_tree()

if __name__ == "__main__":
    Parser("examples/teste2.c").parse()
