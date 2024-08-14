from analizador_lexico.python_analyzer.lexer import init_lexer, parser
from anytree import Node, RenderTree
from typing import List, Dict
import reflex as rx
import re
import sys
import io

class State(rx.State):
    python_code: str = """
class Persona:
    def __init__(self, nombre):
        self.nombre = nombre
    def saludar(self):
        print(f"Hola, soy {self.nombre}")
p = Persona("Juan")
p.saludar()
"""
    lexical_output: List[Dict[str, str]] = []
    syntax_output: str = ""
    js_output: str = ""
    tree_image: str = ""
    debug_output: str = ""

    def clear_all(self):
        self.python_code = ""
        self.lexical_output = []
        self.syntax_output = ""
        self.js_output = ""
        self.tree_image = ""
        self.debug_output = ""

    def analyze_code(self):
        self.debug_output = "Iniciando análisis...\n"

        # Reiniciar el lexer
        lexer = init_lexer()

        # Capturar la salida estándar y de error
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()

        try:
            # Análisis léxico
            lexer.input(self.python_code)
            self.lexical_output = []
            while True:
                tok = lexer.token()
                if not tok:
                    break
                self.lexical_output.append({
                    "linea": str(tok.lineno),
                    "tipo": str(tok.type),
                    "valor": str(tok.value)
                })
            
            self.debug_output += f"Análisis léxico completado. Tokens encontrados: {len(self.lexical_output)}\n"
            self.debug_output += "Tokens:\n" + "\n".join(str(tok) for tok in self.lexical_output) + "\n"

            # Análisis sintáctico
            parser.error = 0  # Reiniciar contador de errores
            result = parser.parse(self.python_code, lexer=lexer, debug=True)  # Activar modo de depuración
            if result is not None:
                self.syntax_output = self.pretty_print_ast(result)
                self.debug_output += "AST generado con éxito.\n"
                
                # Generar árbol visual
                root = self.build_tree(result)
                self.generate_tree_image(root)
            else:
                self.syntax_output = "Error: No se pudo generar el AST."
                self.tree_image = "No se pudo generar el árbol sintáctico."
                self.debug_output += f"Error en el análisis sintáctico. Número de errores: {parser.error}\n"

            # Imprimir el AST para depuración
            self.debug_output += "AST generado:\n"
            self.debug_output += str(result) + "\n"

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
            node = Node("block", parent=parent)
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
            if ast[0] == 'fstring':
                result = "  " * indent + "fstring:\n"
                for component in ast[1]:
                    result += "  " * (indent + 1) + f"{component[0]}: {component[1]}\n"
                return result
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
        in_class = False
        
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
            
            if stripped_line.startswith('class '):
                in_class = True
                js_code += '  ' * indent_level + translated_line + ' {\n'
                indent_level += 1
            elif in_class and stripped_line.startswith('def '):
                if '__init__' in stripped_line:
                    translated_line = translated_line.replace('function __init__', 'constructor')
                else:
                    translated_line = translated_line.replace('function ', '')
                js_code += '  ' * indent_level + translated_line + ' {\n'
                indent_level += 1
            else:
                js_code += '  ' * indent_level + translated_line
            
            if stripped_line.endswith(':') and not stripped_line.startswith('class '):
                if not translated_line.endswith('{'):
                    js_code += ' {'
                js_code += '\n'
                indent_level += 1
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
        line = line.replace('class ', 'class ')
        line = line.replace('__init__', 'constructor')
        line = line.replace('elif ', 'else if ')
        line = line.replace(':', '')
        line = line.replace('True', 'true')
        line = line.replace('False', 'false')
        line = line.replace(' and ', ' && ')
        line = line.replace(' or ', ' || ')
        line = line.replace(' not ', ' !')
        line = line.replace('self.', 'this.')
        
        # Traducción de operadores de comparación
        line = line.replace(' == ', ' === ')
        line = line.replace(' != ', ' !== ')
        line = line.replace(' // ', ' / ')  # Integer division in JS
        
        # Modificar la traducción de print
        if line.strip().startswith('print('):
            content = line.strip()[6:-1]  # Eliminar 'print(' y ')'
            return f"console.log({content})"
        
        # Manejo de f-strings
        if 'f"' in line or "f'" in line:
            line = self.translate_fstring(line)
        
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
        
        return line

    def translate_fstring(self, line):
        # Eliminar 'f' del principio de la cadena
        line = line.replace('f"', '"').replace("f'", "'")
        
        # Reemplazar expresiones {} con ${}
        line = re.sub(r'{([^}]+)}', r'${\\1}', line)
        
        # Cambiar comillas simples por comillas invertidas (backticks)
        if line.startswith("'") and line.endswith("'"):
            line = f"`{line[1:-1]}`"
        
        return line