import sys
import re
import os
from tabulate import tabulate
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QLabel, QMessageBox
import ply.lex as lex
import ply.yacc as yacc
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QMainWindow, QWidget
from PyQt6.QtCore import Qt

# Definición del analizador léxico
tokens = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
    'ID', 'EQUALS', 'COLON', 'COMMA', 'STRING', 'INDENT', 'DEDENT',
    'IF', 'ELSE', 'WHILE', 'FOR', 'IN', 'DEF', 'RETURN', 'PRINT',
    'GT', 'LT', 'GE', 'LE', 'EQ', 'NE', 'COMMENT', 'NEWLINE'
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
    pass  # Ignorar comentarios

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.lexer.at_line_start = True
    return t

t_ignore = ' \t'

# Manejo mejorado de indentación
def t_INDENT(t):
    r'^[ \t]+'
    if t.lexer.at_line_start:
        depth = len(t.value.replace("\t", " " * 4))
        if depth > t.lexer.indent_stack[-1]:
            t.type = "INDENT"
            t.lexer.indent_stack.append(depth)
        elif depth < t.lexer.indent_stack[-1]:
            t.type = "DEDENT"
            while depth < t.lexer.indent_stack[-1]:
                t.lexer.indent_stack.pop()
                t.lexer.emit('DEDENT', '')
            if depth != t.lexer.indent_stack[-1]:
                raise IndentationError("Indentation error")
        else:
            t.type = "IGNORE"
        return t if t.type != "IGNORE" else None
    t.lexer.at_line_start = False

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Inicialización del lexer
lexer.indent_stack = [0]
lexer.at_line_start = True

# Definición mejorada del analizador sintáctico
def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])
    print(f"Program node created with {len(p[1])} statements")

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]
    print(f"Statement list created with {len(p[0])} statements")

def p_statement(p):
    '''statement : simple_statement
                 | compound_statement'''
    p[0] = p[1]
    print(f"Statement created: {p[0][0]}")

def p_simple_statement(p):
    '''simple_statement : small_statement NEWLINE'''
    p[0] = p[1]
    print(f"Simple statement created: {p[0][0]}")

def p_small_statement(p):
    '''small_statement : expression_statement
                       | assignment_statement
                       | return_statement
                       | print_statement'''
    p[0] = p[1]
    print(f"Small statement created: {p[0][0]}")

def p_expression_statement(p):
    '''expression_statement : expression'''
    p[0] = ('expression_statement', p[1])
    print("Expression statement created")

def p_assignment_statement(p):
    '''assignment_statement : ID EQUALS expression'''
    p[0] = ('assignment', p[1], p[3])
    print(f"Assignment created: {p[1]} = ...")

def p_return_statement(p):
    '''return_statement : RETURN expression'''
    p[0] = ('return', p[2])
    print("Return statement created")

def p_print_statement(p):
    '''print_statement : PRINT LPAREN expression_list RPAREN'''
    p[0] = ('print', p[3])
    print("Print statement created")

def p_compound_statement(p):
    '''compound_statement : if_statement
                          | while_statement
                          | for_statement
                          | function_def'''
    p[0] = p[1]
    print(f"Compound statement created: {p[0][0]}")

def p_function_def(p):
    '''function_def : DEF ID LPAREN parameter_list RPAREN COLON suite'''
    p[0] = ('function_def', p[2], p[4], p[7])
    print(f"Function definition created: {p[2]}")

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
    print(f"Parameter list created with {len(p[0])} parameters")

def p_suite(p):
    '''suite : INDENT statement_list DEDENT
             | simple_statement'''
    if len(p) == 2:
        p[0] = ('suite', [p[1]])
    else:
        p[0] = ('suite', p[2])
    print(f"Suite created with {len(p[0][1])} statements")

def p_if_statement(p):
    '''if_statement : IF expression COLON suite
                    | IF expression COLON suite ELSE COLON suite'''
    if len(p) == 5:
        p[0] = ('if', p[2], p[4])
    else:
        p[0] = ('if-else', p[2], p[4], p[7])
    print("If statement created")

def p_while_statement(p):
    '''while_statement : WHILE expression COLON suite'''
    p[0] = ('while', p[2], p[4])
    print("While statement created")

def p_for_statement(p):
    '''for_statement : FOR ID IN expression COLON suite'''
    p[0] = ('for', p[2], p[4], p[6])
    print("For statement created")

def p_expression(p):
    '''expression : arithmetic_expr
                  | comparison_expr'''
    p[0] = p[1]
    print("Expression created")

def p_arithmetic_expr(p):
    '''arithmetic_expr : term
                       | arithmetic_expr PLUS term
                       | arithmetic_expr MINUS term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])
    print("Arithmetic expression created")

def p_term(p):
    '''term : factor
            | term TIMES factor
            | term DIVIDE factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])
    print("Term created")

def p_factor(p):
    '''factor : LPAREN expression RPAREN
              | NUMBER
              | STRING
              | ID
              | function_call'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]
    print("Factor created")

def p_function_call(p):
    '''function_call : ID LPAREN expression_list RPAREN'''
    p[0] = ('function_call', p[1], p[3])
    print(f"Function call created: {p[1]}")

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
    print(f"Expression list created with {len(p[0])} expressions")

def p_comparison_expr(p):
    '''comparison_expr : arithmetic_expr comparison_op arithmetic_expr'''
    p[0] = (p[2], p[1], p[3])
    print("Comparison expression created")

def p_comparison_op(p):
    '''comparison_op : EQ
                     | NE
                     | LT
                     | LE
                     | GT
                     | GE'''
    p[0] = p[1]
    print(f"Comparison operator: {p[1]}")

def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}, position {p.lexpos}: Unexpected token '{p.value}' of type '{p.type}'")
    else:
        print("Syntax error at EOF")

# Construir el parser
try:
    parser = yacc.yacc(debug=True)
except Exception as e:
    print(f"Error al construir el parser: {str(e)}")
    sys.exit(1)

class CodeAnalyzerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Analizador y Traductor de Código')
        self.setGeometry(100, 100, 1200, 800)

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
        self.visualize_button = QPushButton('Visualizar Árbol')
        self.visualize_button.clicked.connect(self.visualize_tree)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.analyze_button)
        button_layout.addWidget(self.visualize_button)
        main_layout.addLayout(button_layout)

        # Tabla para mostrar el análisis léxico
        self.lexical_output = QTableWidget()
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

        # Etiqueta para mostrar la imagen del árbol
        self.tree_image = QLabel()
        self.tree_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.tree_image)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Abrir archivo', '', 'Archivos de texto (*.txt)')
        if file_name:
            with open(file_name, 'r') as file:
                self.code_edit.setPlainText(file.read())

    def ast_to_string(self, node, level=0):
        if isinstance(node, tuple):
            result = "  " * level + f"({node[0]})\n"
            for child in node[1:]:
                result += self.ast_to_string(child, level + 1)
            return result
        elif isinstance(node, list):
            result = "  " * level + "[\n"
            for item in node:
                result += self.ast_to_string(item, level + 1)
            result += "  " * level + "]\n"
            return result
        else:
            return "  " * level + f"{node}\n"
    def analyze_code(self):
        code = self.code_edit.toPlainText()
        
        # Asegurarse de que el código termine con una nueva línea
        if not code.endswith('\n'):
            code += '\n'
        # Reinicializar el lexer
        lexer.lineno = 1
        lexer.indent_stack = [0]
        lexer.at_line_start = True
        lexer.input(code)
        
        # Configurar la tabla
        self.lexical_output.clear()  # Limpiar cualquier contenido anterior
        self.lexical_output.setRowCount(0)
        self.lexical_output.setColumnCount(3)
        self.lexical_output.setHorizontalHeaderLabels(["Línea", "Tipo de Token", "Valor"])

        # Análisis léxico
        lex_errors = []
        tokens = []
        row = 0
        for tok in lexer:
            tokens.append(tok)
            if tok.type == 'error':
                lex_errors.append(f"Error léxico en la línea {tok.lineno}: Carácter ilegal '{tok.value[0]}'")
            else:
                self.lexical_output.insertRow(row)
                self.lexical_output.setItem(row, 0, QTableWidgetItem(str(tok.lineno)))
                self.lexical_output.setItem(row, 1, QTableWidgetItem(tok.type))
                self.lexical_output.setItem(row, 2, QTableWidgetItem(str(tok.value)))
                row += 1
        
        if lex_errors:
            for error in lex_errors:
                self.lexical_output.insertRow(row)
                self.lexical_output.setItem(row, 0, QTableWidgetItem(""))
                self.lexical_output.setItem(row, 1, QTableWidgetItem("Error"))
                self.lexical_output.setItem(row, 2, QTableWidgetItem(error))
                row += 1

        # Ajustar columnas al contenido
        self.lexical_output.resizeColumnsToContents()

        # Análisis sintáctico
        try:
            print("Comenzando análisis sintáctico...")
            self.ast = parser.parse(input=code, lexer=lexer, debug=True)
            print(f"AST generado: {self.ast}")
            if self.ast is None:
                raise Exception("El analizador sintáctico no generó un AST válido.")
            ast_str = self.ast_to_string(self.ast)
            print("Representación del AST:")
            print(ast_str)
            self.syntax_output.setPlainText(ast_str)
        except Exception as e:
            error_msg = f"Error en el análisis sintáctico: {str(e)}\n"
            error_msg += f"Tokens generados: {tokens}\n"
            print(error_msg)  # Imprimir en la consola para debugging
            self.syntax_output.setPlainText(error_msg)
            self.ast = None

        # Traducción a JavaScript
        js_code = self.translate_to_js(code)
        self.js_output.setPlainText(js_code)

    def ast_to_string(self, node, level=0):
        if isinstance(node, tuple):
            result = "  " * level + f"({node[0]})\n"
            for child in node[1:]:
                result += self.ast_to_string(child, level + 1)
            return result
        elif isinstance(node, list):
            result = "  " * level + "[\n"
            for item in node:
                result += self.ast_to_string(item, level + 1)
            result += "  " * level + "]\n"
            return result
        elif isinstance(node, str):
            return "  " * level + f"STRING: '{node}'\n"
        elif isinstance(node, int):
            return "  " * level + f"NUMBER: {node}\n"
        else:
            return "  " * level + f"UNKNOWN: {node}\n"

    def visualize_tree(self):
        if not hasattr(self, 'ast') or self.ast is None:
            QMessageBox.warning(self, "Advertencia", "Primero analiza el código para generar el árbol")
            return

        try:
            # Generar el árbol utilizando anytree
            root = self.build_anytree(self.ast)
            print(f"Root node: {root.name}")  # Depuración
            
            # Renderizar el árbol como texto
            tree_str = ""
            for pre, _, node in RenderTree(root):
                tree_str += f"{pre}{node.name}\n"
                print(f"Nodo: {node.name}")  # Depuración

            # Mostrar el árbol en un QTextEdit
            self.syntax_output.setPlainText(tree_str)  # Mostramos solo esta parte
            
        except Exception as e:
            print(f"Error: {str(e)}")  # Depuración
            QMessageBox.warning(self, "Error", f"Ocurrió un error al generar el árbol: {str(e)}")

    def build_anytree(self, node, parent=None):
        if isinstance(node, tuple):
            any_node = Node(node[0], parent=parent)
            print(f"Creando nodo tuple: {node[0]}")  # Depuración
            for child in node[1:]:
                self.build_anytree(child, parent=any_node)
            return any_node
        elif isinstance(node, list):
            any_node = None
            for item in node:
                any_node = self.build_anytree(item, parent=parent)
            return any_node
        else:
            print(f"Creando nodo simple: {node}")  # Depuración
            return Node(str(node), parent=parent)

    def translate_to_js(self, python_code):
        js_code = ""
        lines = python_code.split('\n')
        indent_level = 0
        indent_size = 4  # Assuming 4 spaces per indent level
        in_function = False
        
        for line in lines:
            stripped_line = line.strip()
            
            # Ignorar líneas vacías y comentarios
            if not stripped_line or stripped_line.startswith('#'):
                js_code += line + '\n'
                continue
            
            current_indent_level = (len(line) - len(line.lstrip())) // indent_size
            
            # Adjust indent level in JS based on Python code
            while indent_level > current_indent_level:
                indent_level -= 1
                js_code += '  ' * indent_level + '}\n'
            
            translated_line = self.translate_line(stripped_line)
            js_code += '  ' * indent_level + translated_line
            
            # Si la línea es una apertura de bloque, incrementamos el nivel de indentación
            if stripped_line.endswith(':'):
                if not translated_line.endswith('{'):
                    js_code += ' {'
                js_code += '\n'
                indent_level += 1
                if stripped_line.startswith('def '):
                    in_function = True
            elif in_function and stripped_line.startswith('return '):
                js_code += ';\n'
                in_function = False
            elif not translated_line.endswith('{') and not translated_line.endswith('}'):
                js_code += ';\n'
            else:
                js_code += '\n'
        
        # Cerrar todos los bloques restantes
        while indent_level > 0:
            indent_level -= 1
            js_code += '  ' * indent_level + '}\n'
        
        return js_code

    def translate_line(self, line):
        # Traducir palabras clave de Python a JavaScript
        if line.startswith('def '):
            line = line.replace('def ', 'function ')
        line = line.replace('elif ', 'else if ')
        line = line.replace(':', '')
        line = line.replace('print(', 'console.log(')
        line = line.replace('True', 'true')
        line = line.replace('False', 'false')
        line = line.replace(' and ', ' && ')
        line = line.replace(' or ', ' || ')
        line = line.replace(' not ', ' !')
        
        # Traducción de operadores de comparación
        line = line.replace(' == ', ' === ')
        line = line.replace(' != ', ' !== ')
        line = line.replace(' // ', ' / ')  # Integer division in JS
        
        # Manejo de bucles for
        if line.startswith('for ') and 'range' in line:
            match = re.search(r'for (\w+) in range\(([^)]+)\)', line)
            if match:
                var, range_args = match.groups()
                range_parts = range_args.split(',')
                if len(range_parts) == 1:
                    start, end = '0', range_parts[0].strip()
                elif len(range_parts) == 2:
                    start, end = [p.strip() for p in range_parts]
                else:
                    start, end, step = [p.strip() for p in range_parts]
                    return f"for (let {var} = {start}; {var} < {end}; {var} += {step})"
                return f"for (let {var} = {start}; {var} < {end}; {var}++)"
        
        # Manejo de asignaciones
        if '=' in line and not line.startswith('if') and not line.startswith('for'):
            parts = line.split('=')
            if len(parts) == 2:
                var, value = parts[0].strip(), parts[1].strip()
                if '*=' in line:
                    return f"{var} *= {value.replace('*=', '').strip()}"
                elif '/=' in line:
                    return f"{var} /= {value.replace('/=', '').strip()}"
                else:
                    return f"let {var} = {value}"
        
        # Manejo de declaraciones if
        if line.startswith('if ') or line.startswith('elif ') or line.startswith('else'):
            line = line.rstrip(':')
            if 'if ' in line or 'elif ' in line:
                condition = line.split('if ')[-1].split('elif ')[-1].strip()
                return f"if ({condition})"
            else:
                return "else"
        
        return line

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CodeAnalyzerGUI()
    ex.show()
    sys.exit(app.exec())