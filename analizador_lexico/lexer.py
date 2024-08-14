import ply.lex as lex

# Definición del analizador léxico
tokens = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO', 'LPAREN', 'RPAREN',
    'ID', 'EQUALS', 'COLON', 'COMMA', 'STRING', 'FSTRING', 'INDENT', 'DEDENT',
    'IF', 'ELSE', 'WHILE', 'FOR', 'IN', 'DEF', 'RETURN', 'PRINT', 'CLASS',
    'GT', 'LT', 'GE', 'LE', 'EQ', 'NE', 'COMMENT', 'NEWLINE', 'DOT',
    'LAMBDA', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'DICT_METHOD',
    'AT'
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_COLON = r':'
t_COMMA = r','
t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='
t_EQ = r'=='
t_NE = r'!='
t_DOT = r'\.'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'("([^"\\]|\\.)*")|(\'([^\'\\]|\\.)*\')'
    t.value = t.value[1:-1]  # Remove quotes
    return t

def t_FSTRING(t):
    r'f"[^"]*"|f\'[^\']*\''
    t.value = t.value[2:-1]  # Remove 'f' and quotes
    return t

def t_AT(t):
    r'@'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value == 'lambda':
        t.type = 'LAMBDA'
    elif t.value in ['items', 'keys', 'values']:
        t.type = 'DICT_METHOD'
    elif t.value in ['if', 'else', 'while', 'for', 'in', 'def', 'return', 'print', 'class']:
        t.type = t.value.upper()
    return t

def t_COMMENT(t):
    r'\#.*'
    pass  # Ignorar comentarios

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.lexer.at_line_start = True
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}, position {t.lexpos}")
    t.lexer.skip(1)

# Manejo de indentación
def t_INDENT(t):
    r'^\s+'
    if t.lexer.at_line_start:
        if len(t.value) > len(t.lexer.indent_stack[-1]):
            t.type = "INDENT"
            t.lexer.indent_stack.append(t.value)
            return t
        elif len(t.value) < len(t.lexer.indent_stack[-1]):
            t.type = "DEDENT"
            t.lexer.indent_stack.pop()
            return t
    t.lexer.at_line_start = False
    return None  # Descartar si no es INDENT ni DEDENT

def t_eof(t):
    if len(t.lexer.indent_stack) > 1:
        t.type = "DEDENT"
        t.lexer.indent_stack.pop()
        return t

# Construir el lexer
lexer = lex.lex()

# Inicialización del lexer
def init_lexer():
    lexer = lex.lex()
    lexer.indent_stack = ['']
    lexer.at_line_start = True
    lexer.paren_count = 0
    return lexer