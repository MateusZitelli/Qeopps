from Tree import *
#from SyncTable import *

def get_cond(text):
    depth = 0
    start = None
    for i, j in enumerate(text):
        if j == "(":
            if depth == 0:
                start = i
            depth += 1
        elif j == ")":
            depth -= 1
        if depth == 0 and start != None:
            return (start + 1, i)

class Parser:
    def __init__(self, filename):
        f = open(filename, "rU")
        self.text = f.read()
        self.lines = self.text.split(";")
        f.close()
        self.tree = Tree(TreeNode("program"))
        #self.syncTable = SyncTable()

    def parse(self, current_node = None):
        if(current_node == None):
            current_node = self.tree.root
        for i, j in enumerate(self.lines):
            if "}" in j:
                for k, l in enumerate(j):
                    if l == "}":
                        current_node = current_node.parent
            if "{" in j:
                if " if " in j or " switch " in j or " while " in j or\
                    " for " in j:
                    cut_points = get_cond(j)
                    node = self.tree.new_node(j[:cut_points[1] + 1].lstrip(' ')\
                        ,current_node)
                else:
                    function = j.split("(")[0]
                    args = j[j.find("(")+1:j.find(")")]
                    func_node = self.tree.new_node(\
                        function.replace("\n", "").replace("}", "").lstrip(' ')\
                        +"("+args+")", current_node)
                    current_node = func_node
            else:
                 self.tree.new_node(j.replace("\n", "")\
                    .replace("}", "").lstrip(' '),current_node)
