import parser

p = parser.Parser("teste.c")
p.parse()
p.tree.print_tree()

