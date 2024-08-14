import ply.lex as lex

# Construir el lexer
lexer = lex.lex()

# Inicialización del lexer
def init_lexer():
    lexer = lex.lex()
    lexer.indent_stack = ['']
    lexer.at_line_start = True
    lexer.paren_count = 0
    return lexer