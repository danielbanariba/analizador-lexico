#TODO
# - Hacer que la logica este en distintos componentes
# - mejorar la traduccion de javascript
# - hacer que pueda convertirse de uno a otro
# - Mejorar Analisis sintactico
# - Creacion de arbol, de forma visual

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import ply.lex as lex
import ply.yacc as yacc

# Definición del analizador léxico
tokens = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
    'ID', 'EQUALS', 'COLON', 'COMMA', 'STRING', 'INDENT', 'DEDENT',
    'IF', 'ELSE', 'WHILE', 'FOR', 'IN', 'DEF', 'RETURN', 'PRINT',
    'GT', 'LT', 'GE', 'LE', 'EQ', 'NE', 'COMMENT'
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
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

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remove quotes
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in ['if', 'else', 'while', 'for', 'in', 'def', 'return', 'print']:
        t.type = t.value.upper()
    return t

def t_COMMENT(t):
    r'\#.*'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

# Manejo de indentación
def t_INDENT(t):
    r'^[ \t]+'
    if t.lexer.at_line_start and t.lexer.paren_count == 0:
        t.value = len(t.value.replace("\t", " "*4))
        if t.value > t.lexer.indent_stack[-1]:
            t.type = "INDENT"
            t.lexer.indent_stack.append(t.value)
        elif t.value < t.lexer.indent_stack[-1]:
            t.type = "DEDENT"
            t.lexer.indent_stack.pop()
        else:
            t.type = "IGNORE"
        return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Inicialización del lexer
lexer.indent_stack = [0]
lexer.paren_count = 0
lexer.at_line_start = True

# Definición del analizador sintáctico
def p_program(p):
    '''program : statement_list'''
    p[0] = p[1]

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : simple_statement
                 | compound_statement
                 | COMMENT'''
    p[0] = p[1]

def p_simple_statement(p):
    '''simple_statement : assignment
                        | function_call
                        | return_statement
                        | print_statement'''
    p[0] = p[1]

def p_compound_statement(p):
    '''compound_statement : function_def
                          | if_statement
                          | while_statement
                          | for_statement'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : ID EQUALS expression'''
    p[0] = ('assignment', p[1], p[3])

def p_function_call(p):
    '''function_call : ID LPAREN expression_list RPAREN'''
    p[0] = ('function_call', p[1], p[3])

def p_expression_list(p):
    '''expression_list : expression
                       | expression_list COMMA expression
                       | '''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_return_statement(p):
    '''return_statement : RETURN expression'''
    p[0] = ('return', p[2])

def p_print_statement(p):
    '''print_statement : PRINT LPAREN expression RPAREN'''
    p[0] = ('print', p[3])

def p_function_def(p):
    '''function_def : DEF ID LPAREN parameter_list RPAREN COLON block'''
    p[0] = ('function_def', p[2], p[4], p[7])

def p_parameter_list(p):
    '''parameter_list : ID
                      | parameter_list COMMA ID
                      | '''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_if_statement(p):
    '''if_statement : IF expression COLON block
                    | IF expression COLON block ELSE COLON block'''
    if len(p) == 5:
        p[0] = ('if', p[2], p[4])
    else:
        p[0] = ('if-else', p[2], p[4], p[7])

def p_while_statement(p):
    '''while_statement : WHILE expression COLON block'''
    p[0] = ('while', p[2], p[4])

def p_for_statement(p):
    '''for_statement : FOR ID IN expression COLON block'''
    p[0] = ('for', p[2], p[4], p[6])

def p_block(p):
    '''block : INDENT statement_list DEDENT'''
    p[0] = p[2]

def p_expression(p):
    '''expression : arithmetic_expr
                  | comparison_expr
                  | STRING
                  | NUMBER
                  | ID
                  | function_call'''
    p[0] = p[1]

def p_arithmetic_expr(p):
    '''arithmetic_expr : term
                       | arithmetic_expr PLUS term
                       | arithmetic_expr MINUS term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_term(p):
    '''term : factor
            | term TIMES factor
            | term DIVIDE factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_factor(p):
    '''factor : LPAREN expression RPAREN
              | NUMBER
              | ID'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_comparison_expr(p):
    '''comparison_expr : arithmetic_expr GT arithmetic_expr
                       | arithmetic_expr LT arithmetic_expr
                       | arithmetic_expr GE arithmetic_expr
                       | arithmetic_expr LE arithmetic_expr
                       | arithmetic_expr EQ arithmetic_expr
                       | arithmetic_expr NE arithmetic_expr'''
    p[0] = (p[2], p[1], p[3])

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}', line {p.lineno}")
    else:
        print("Syntax error at EOF")

# Construir el parser
parser = yacc.yacc()

class CodeAnalyzerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Analizador y Traductor de Código')
        self.setGeometry(100, 100, 1000, 800)

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Área de texto para mostrar el código
        self.code_edit = QTextEdit()
        main_layout.addWidget(QLabel('Código Python:'))
        main_layout.addWidget(self.code_edit)

        # Botones
        button_layout = QHBoxLayout()
        self.load_button = QPushButton('Cargar Archivo')
        self.load_button.clicked.connect(self.load_file)
        self.analyze_button = QPushButton('Analizar')
        self.analyze_button.clicked.connect(self.analyze_code)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.analyze_button)
        main_layout.addLayout(button_layout)

        # Área de texto para mostrar el análisis léxico
        self.lexical_output = QTextEdit()
        self.lexical_output.setReadOnly(True)
        main_layout.addWidget(QLabel('Análisis Léxico:'))
        main_layout.addWidget(self.lexical_output)

        # Área de texto para mostrar el análisis sintáctico
        self.syntax_output = QTextEdit()
        self.syntax_output.setReadOnly(True)
        main_layout.addWidget(QLabel('Análisis Sintáctico:'))
        main_layout.addWidget(self.syntax_output)

        # Área de texto para mostrar la traducción a JavaScript
        self.js_output = QTextEdit()
        self.js_output.setReadOnly(True)
        main_layout.addWidget(QLabel('Traducción a JavaScript:'))
        main_layout.addWidget(self.js_output)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Abrir archivo', '', 'Archivos de texto (*.txt)')
        if file_name:
            with open(file_name, 'r') as file:
                self.code_edit.setPlainText(file.read())

    def analyze_code(self):
        code = self.code_edit.toPlainText()
        
        # Análisis léxico
        lexer.input(code)
        lex_output = "Línea | Tipo de Token | Valor\n" + "-" * 40 + "\n"
        for tok in lexer:
            lex_output += f"{tok.lineno:5d} | {tok.type:13s} | {tok.value}\n"
        self.lexical_output.setPlainText(lex_output)

        # Análisis sintáctico
        try:
            result = parser.parse(code, lexer=lexer)
            self.syntax_output.setPlainText(str(result))
        except Exception as e:
            self.syntax_output.setPlainText(f"Error en el análisis sintáctico: {str(e)}")

        # Traducción a JavaScript
        js_code = self.translate_to_js(code)
        self.js_output.setPlainText(js_code)

    def translate_to_js(self, python_code):
        js_code = ""
        lines = python_code.split('\n')
        indent_level = 0
        
        for line in lines:
            stripped_line = line.strip()
            
            # Ignorar líneas vacías y comentarios
            if not stripped_line or stripped_line.startswith('#'):
                js_code += line + '\n'
                continue
            
            # Manejar indentación
            if stripped_line.startswith(('if', 'else', 'for', 'while', 'def')):
                js_code += '  ' * indent_level + self.translate_line(stripped_line) + ' {\n'
                indent_level += 1
            elif stripped_line.startswith(('return', 'print')):
                js_code += '  ' * indent_level + self.translate_line(stripped_line) + ';\n'
            else:
                js_code += '  ' * indent_level + self.translate_line(stripped_line) + ';\n'
            
            # Reducir indentación después de bloques
            if indent_level > 0 and len(line) - len(line.lstrip()) < 4 * indent_level:
                indent_level -= 1
                js_code += '  ' * indent_level + '}\n'
        
        return js_code

    def translate_line(self, line):
        # Traducir palabras clave de Python a JavaScript
        line = line.replace('def ', 'function ')
        line = line.replace('elif ', 'else if ')
        line = line.replace(':', '')
        line = line.replace('print(', 'console.log(')
        
        # Traducir operadores de comparación
        line = line.replace(' == ', ' === ')
        line = line.replace(' != ', ' !== ')
        
        return line

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CodeAnalyzerGUI()
    ex.show()
    sys.exit(app.exec())