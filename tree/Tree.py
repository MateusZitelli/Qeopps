class TreeNode:
    def __init__(self, data, index=None, childs=[], parent=None):
        self.childs = list(childs)
        self.data = data
        self.index = index
        self.parent = parent

    def add_child(self, child):
        self.childs.append(child)
        child.parent = self

class Tree:
    def __init__(self, root=None):
        self.root = root
        if root == None:
            self.size = 0
            self.nodes = []
        else:
            self.size = 1
            self.nodes = [root]

    def new_node(self, data, parent=None):
        self.nodes.append(TreeNode(data, self.size))
        if(parent == None and self.root == None):
            self.root = self.nodes[-1]
        elif(parent == None):
            raise RuntimeError ("The tree alredy have a root.")
        elif(parent in self.nodes):
            parent.add_child(self.nodes[-1])
        else:
            raise RuntimeError ("The parent node isn't in this tree.")
        self.size += 1
        return self.nodes[-1]
