import reflex as rx
import ply.lex as lex
import ply.yacc as yacc
from anytree import Node, RenderTree
import re
import sys
import io

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

# Definición del analizador sintáctico
def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : simple_statement
                 | compound_statement'''
    p[0] = p[1]

def p_simple_statement(p):
    '''simple_statement : assignment_statement NEWLINE
                        | return_statement NEWLINE
                        | print_statement NEWLINE
                        | expression_statement NEWLINE'''
    p[0] = p[1]

def p_compound_statement(p):
    '''compound_statement : if_statement
                          | while_statement
                          | for_statement
                          | function_def'''
    p[0] = p[1]

def p_assignment_statement(p):
    '''assignment_statement : ID EQUALS expression'''
    p[0] = ('assignment', p[1], p[3])

def p_return_statement(p):
    '''return_statement : RETURN expression'''
    p[0] = ('return', p[2])

def p_print_statement(p):
    '''print_statement : PRINT LPAREN expression_list RPAREN'''
    p[0] = ('print', p[3])

def p_expression_statement(p):
    '''expression_statement : expression'''
    p[0] = ('expression_statement', p[1])

def p_expression_list(p):
    '''expression_list : expression
                       | expression_list COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_if_statement(p):
    '''if_statement : IF expression COLON NEWLINE INDENT statement_list DEDENT
                    | IF expression COLON NEWLINE INDENT statement_list DEDENT ELSE COLON NEWLINE INDENT statement_list DEDENT'''
    if len(p) == 8:
        p[0] = ('if', p[2], p[6])
    else:
        p[0] = ('if-else', p[2], p[6], p[12])

def p_while_statement(p):
    '''while_statement : WHILE expression COLON NEWLINE INDENT statement_list DEDENT'''
    p[0] = ('while', p[2], p[6])

def p_for_statement(p):
    '''for_statement : FOR ID IN expression COLON NEWLINE INDENT statement_list DEDENT'''
    p[0] = ('for', p[2], p[4], p[8])

def p_function_def(p):
    '''function_def : DEF ID LPAREN parameter_list RPAREN COLON NEWLINE INDENT statement_list DEDENT'''
    p[0] = ('function_def', p[2], p[4], p[9])

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

def p_expression(p):
    '''expression : arithmetic_expr
                  | comparison_expr'''
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
              | STRING
              | ID
              | function_call'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_function_call(p):
    '''function_call : ID LPAREN expression_list RPAREN'''
    p[0] = ('function_call', p[1], p[3])

def p_comparison_expr(p):
    '''comparison_expr : arithmetic_expr comparison_op arithmetic_expr'''
    p[0] = (p[2], p[1], p[3])

def p_comparison_op(p):
    '''comparison_op : EQ
                     | NE
                     | LT
                     | LE
                     | GT
                     | GE'''
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}', line {p.lineno}")
    else:
        print("Syntax error at EOF")

# Construir el parser
parser = yacc.yacc()

class State(rx.State):
    python_code: str = """
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

result = factorial(5)
print("El factorial de 5 es:", result)
"""
    lexical_output: str = ""
    syntax_output: str = ""
    js_output: str = ""
    tree_image: str = ""
    debug_output: str = ""

    def analyze_code(self):
        self.debug_output = "Iniciando análisis...\n"

        # Capturar la salida estándar y de error
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()

        try:
            # Análisis léxico
            lexer.input(self.python_code)
            self.lexical_output = "Línea | Tipo de Token | Valor\n" + "-" * 40 + "\n"
            tokens = []
            for tok in lexer:
                self.lexical_output += f"{tok.lineno:5d} | {tok.type:13s} | {tok.value}\n"
                tokens.append(tok)
            self.debug_output += f"Análisis léxico completado. Tokens encontrados: {len(tokens)}\n"

            # Análisis sintáctico
            lexer.input(self.python_code)
            result = parser.parse(self.python_code, debug=True)
            
            if result is not None:
                self.syntax_output = self.pretty_print_ast(result)
                self.debug_output += "AST generado con éxito.\n"
                
                # Generar árbol visual
                root = self.build_tree(result)
                self.generate_tree_image(root)
            else:
                self.syntax_output = "Error: No se pudo generar el AST."
                self.debug_output += "El parser retornó None. Revisando los tokens:\n"
                for tok in tokens:
                    self.debug_output += f"  {tok.type}: {tok.value}\n"
                self.tree_image = "No se pudo generar el árbol sintáctico."

            # Traducción a JavaScript
            self.js_output = self.translate_to_js(self.python_code)

        except Exception as e:
            import traceback
            self.syntax_output = f"Error en el análisis: {str(e)}\n\n"
            self.syntax_output += traceback.format_exc()
            self.debug_output += f"Excepción capturada: {str(e)}\n"
            self.tree_image = "Error al generar el árbol sintáctico."

        finally:
            # Restaurar la salida estándar y de error, y capturar sus contenidos
            sys.stdout.seek(0)
            sys.stderr.seek(0)
            self.debug_output += "Salida estándar:\n" + sys.stdout.read() + "\n"
            self.debug_output += "Salida de error:\n" + sys.stderr.read()
            sys.stdout = old_stdout
            sys.stderr = old_stderr

    def build_tree(self, ast, parent=None):
        if ast is None:
            return Node("None", parent=parent)
        
        if isinstance(ast, (str, int, float)):
            return Node(str(ast), parent=parent)
        
        if isinstance(ast, tuple):
            node = Node(str(ast[0]), parent=parent)
            for child in ast[1:]:
                self.build_tree(child, node)
            return node
        
        if isinstance(ast, list):
            node = Node("program" if parent is None else "block", parent=parent)
            for item in ast:
                self.build_tree(item, node)
            return node
        
        return Node(str(ast), parent=parent)

    def generate_tree_image(self, root):
        tree_str = ""
        for pre, _, node in RenderTree(root):
            tree_str += f"{pre}{node.name}\n"
        self.tree_image = tree_str

    def pretty_print_ast(self, ast, indent=0):
        if isinstance(ast, tuple):
            return "  " * indent + f"{ast[0]}:\n" + "\n".join(self.pretty_print_ast(x, indent + 1) for x in ast[1:])
        elif isinstance(ast, list):
            return "\n".join(self.pretty_print_ast(x, indent) for x in ast)
        else:
            return "  " * indent + str(ast)

    def translate_to_js(self, python_code):
        js_code = ""
        lines = python_code.split('\n')
        indent_level = 0
        indent_size = 4
        in_function = False
        
        for line in lines:
            stripped_line = line.strip()
            
            if not stripped_line or stripped_line.startswith('#'):
                js_code += '//' + line[1:] + '\n' if stripped_line.startswith('#') else '\n'
                continue
            
            current_indent_level = (len(line) - len(line.lstrip())) // indent_size
            
            while indent_level > current_indent_level:
                indent_level -= 1
                js_code += '  ' * indent_level + '}\n'
            
            translated_line = self.translate_line_to_js(stripped_line)
            js_code += '  ' * indent_level + translated_line
            
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
        
        while indent_level > 0:
            indent_level -= 1
            js_code += '  ' * indent_level + '}\n'
        
        return js_code

    def translate_line_to_js(self, line):
        # Traducir palabras clave de Python a JavaScript
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

def index():
    return rx.container(
        rx.vstack(
            rx.heading("Analizador y Traductor de Código Python a JavaScript"),
            rx.text_area(
                value=State.python_code,
                placeholder="Ingrese su código Python aquí",
                on_change=State.set_python_code,
                height="200px",
                width="100%",
            ),
            rx.button("Analizar y Traducir", on_click=State.analyze_code),
            rx.divider(),
            rx.heading("Análisis Léxico", size="md"),
            rx.text_area(value=State.lexical_output, is_read_only=True, height="200px", width="100%"),
            rx.heading("Análisis Sintáctico", size="md"),
            rx.text_area(value=State.syntax_output, is_read_only=True, height="200px", width="100%"),
            rx.heading("Árbol Sintáctico", size="md"),
            rx.text(State.tree_image, font_family="monospace", white_space="pre-wrap"),
            rx.heading("Código JavaScript", size="md"),
            rx.text_area(value=State.js_output, is_read_only=True, height="200px", width="100%"),
            rx.heading("Información de Depuración", size="md"),
            rx.text_area(value=State.debug_output, is_read_only=True, height="300px", width="100%"),
            width="100%",
            max_width="800px",
            spacing="4",
        )
    )

app = rx.App()
app.add_page(index)