from pycparser import CParser, preprocess_file,parse_file
def parse(filename):
    ast = parse_file("teste.c", use_cpp=True,
                     cpp_path='cpp', 
                     cpp_args=[r'-D__attribute__(x)=',
                               r'-D__asm__(x)=',
                               r'-D__builtin_va_list=int',
                               r'-D__const=',
                               r'-D__restrict=',
                               r'-D__extension__=',
                               r'-D__inline__='])
    print ast.show()

parse("teste.c")
