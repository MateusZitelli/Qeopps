from Tree import Tree, TreeNode
class Parser:
    def __init__(self, filename):
        f = open(filename, "rU")
        self.text = f.read()
        self.lines = self.text.split(";")
        f.close()
        self.tree = Tree(TreeNode("program"))

    def parse(self, current_node = None):
        if(current_node == None):
            current_node = self.tree.root
        for i, j in enumerate(self.lines):
            if "}" in j:
                for i in j:
                    if i == "}":
                        current_node = current_node.parent
            if "{" in j:
                if " if " in j:
                    cond = j[j.find("(")+1:j.find(")")]
                    if_node = self.tree.new_node("if("+cond+")",\
                        current_node)
                    current_node = if_node
                elif " switch " in j:
                    cond = j[j.find("(")+1:j.find(")")]
                    switch_node = self.tree.new_node("switch("+cond+")",\
                        current_node)
                    current_node = switch_node
                elif " while " in j:
                    cond = j[j.find("(")+1:j.find(")")]
                    while_node = self.tree.new_node("while("+cond+")",\
                        current_node)
                    current_node = while_node
                elif " for " in j:
                    cond = j[j.find("(")+1:j.find(")")]
                    for_node = self.tree.new_node("for("+cond+")",\
                        current_node)
                    current_node = for_node
                else:
                    function = j.split("(")[0]
                    args = j[j.find("(")+1:j.find(")")]
                    func_node = self.tree.new_node(function.replace("\n", "").lstrip(' ')+"("+args+")",\
                        current_node)
                    current_node = func_node
            else:
                if "#" in j:
                    self.tree.new_node(j.lstrip(' '),\
                        current_node)
                else:
                    self.tree.new_node(j.replace("\n", "").lstrip(' '),\
                        current_node)
