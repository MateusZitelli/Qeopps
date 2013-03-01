class TreeNode:
    def __init__(self, childs=[], data):
        self.childs = list(childs)
        self.data = data

    def add_child(self, child):
        self.childs.append(child)

class Tree:
    def __init__(self, root=None):
        self.root = root
        if root == None:
            self.size = 0
        else:
            self.size = 1

    def mutate
        
