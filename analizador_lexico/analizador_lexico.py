import reflex as rx
import ply.lex as lex
import ply.yacc as yacc
from anytree import Node, RenderTree

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
                 | compound_statement
                 | COMMENT'''
    p[0] = p[1]

def p_simple_statement(p):
    '''simple_statement : assignment
                        | function_call
                        | return_statement
                        | print_statement
                        | expression'''
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

class State(rx.State):
    python_code: str = ""
    lexical_output: str = ""
    syntax_output: str = ""
    cpp_output: str = ""
    tree_image: str = ""
    
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Manejar la carga de archivo(s)."""
        if not files:
            return
        file = files[0]
        content = await file.read()
        self.python_code = content.decode("utf-8")
        self.analyze_code()

    def analyze_code(self):
        # Análisis léxico
        lexer.input(self.python_code)
        self.lexical_output = "Línea | Tipo de Token | Valor\n" + "-" * 40 + "\n"
        for tok in lexer:
            self.lexical_output += f"{tok.lineno:5d} | {tok.type:13s} | {tok.value}\n"

        # Análisis sintáctico
        try:
            result = parser.parse(self.python_code, lexer=lexer)
            self.syntax_output = self.pretty_print_ast(result)
            
            # Generar árbol visual
            root = self.build_tree(result)
            self.generate_tree_image(root)
        except Exception as e:
            import traceback
            self.syntax_output = f"Error en el análisis sintáctico: {str(e)}\n\n"
            self.syntax_output += traceback.format_exc()
            self.tree_image = ""

        # Traducción a C++
        self.cpp_output = self.translate_to_cpp(self.python_code)

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
        
        # Para cualquier otro tipo de objeto, convertimos a string
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

    def translate_to_cpp(self, python_code):
        cpp_code = "#include <iostream>\n#include <string>\n\nusing namespace std;\n\n"
        lines = python_code.split('\n')
        indent_level = 0
        in_function = False
        
        for line in lines:
            stripped_line = line.strip()
            
            # Ignorar líneas vacías y comentarios
            if not stripped_line or stripped_line.startswith('#'):
                cpp_code += '//' + line[1:] + '\n' if stripped_line.startswith('#') else '\n'
                continue
            
            # Manejar indentación
            if stripped_line.startswith(('if', 'else', 'for', 'while', 'def')):
                cpp_code += '  ' * indent_level + self.translate_line(stripped_line) + ' {\n'
                indent_level += 1
                if stripped_line.startswith('def'):
                    in_function = True
            elif stripped_line.startswith(('return', 'print')):
                cpp_code += '  ' * indent_level + self.translate_line(stripped_line) + ';\n'
            else:
                cpp_code += '  ' * indent_level + self.translate_line(stripped_line) + ';\n'
            
            # Reducir indentación después de bloques
            if indent_level > 0 and len(line) - len(line.lstrip()) < 4 * indent_level:
                indent_level -= 1
                cpp_code += '  ' * indent_level + '}\n'
                if in_function and indent_level == 0:
                    in_function = False
                    cpp_code += '\n'
        
        # Agregar la función main() si no está presente
        if 'int main()' not in cpp_code:
            cpp_code += '\nint main() {\n    // Coloca aquí el código principal\n    return 0;\n}\n'
        
        return cpp_code

    def translate_line(self, line):
        # Traducir palabras clave de Python a C++
        line = line.replace('def ', 'auto ')
        line = line.replace('elif ', 'else if ')
        line = line.replace(':', '')
        line = line.replace('print(', 'cout << ')
        line = line.replace('True', 'true')
        line = line.replace('False', 'false')
        line = line.replace('None', 'nullptr')
        
        # Ajustar la función print
        if 'cout <<' in line:
            line = line.replace(')', ' << endl')
        
        # Traducir operadores de comparación
        line = line.replace(' and ', ' && ')
        line = line.replace(' or ', ' || ')
        line = line.replace('not ', '!')
        
        # Ajustar declaraciones de variables
        if '=' in line and 'if' not in line and 'while' not in line:
            parts = line.split('=')
            if len(parts) == 2 and '=' not in parts[1]:
                line = 'auto ' + line
        
        return line


def index():
    return rx.container(
        rx.vstack(
            rx.heading("Analizador y Traductor de Código Python a C++"),
            rx.upload(
                rx.vstack(
                    rx.text("Arrastre y suelte el archivo aquí o haga clic para seleccionar"),
                ),
                id="code_upload",
                accept={".py": ["text/x-python"]},
                max_files=1,
                on_upload=State.handle_upload,
                border="1px dotted rgb(107,99,246)",
                padding="2em",
                margin_bottom="1em",
            ),
            rx.button(
                "Seleccionar archivo",
                on_click=rx.upload_files(upload_id="code_upload"),
                color="rgb(107,99,246)",
                bg="white",
                border="1px solid rgb(107,99,246)",
            ),
            rx.text_area(
                value=State.python_code,
                placeholder="El contenido del archivo se mostrará aquí",
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
            rx.heading("Código C++", size="md"),
            rx.text_area(value=State.cpp_output, is_read_only=True, height="200px", width="100%"),
            width="100%",
            max_width="800px",
            spacing="4",
        )
    )

app = rx.App()
app.add_page(index)

app = rx.App()
app.add_page(index)