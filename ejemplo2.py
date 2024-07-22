import re
from enum import Enum, auto
from lark import Lark, Token as LarkToken

class TipoToken(Enum):
    """Enumeración de los tipos de tokens soportados."""
    NUMERO = auto()
    IDENTIFICADOR = auto()
    OPERADOR_ARITMETICO = auto()
    OPERADOR_LOGICO = auto()
    OPERADOR_COMPARACION = auto()
    OPERADOR_ASIGNACION = auto()
    PARENTESIS_IZQ = auto()
    PARENTESIS_DER = auto()
    LLAVE_IZQ = auto()
    LLAVE_DER = auto()
    PALABRA_CLAVE = auto()
    CADENA = auto()
    COMENTARIO = auto()
    FIN_DE_LINEA = auto()
    ESPACIO = auto()
    COMA = auto()
    PUNTO_Y_COMA = auto()
    DOS_PUNTOS = auto()

class Token:
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna

    def __str__(self):
        return f'Token({self.tipo.name}, {self.valor!r}, linea:{self.linea}, columna:{self.columna})'

class ErrorLexico(Exception):
    pass

class AnalizadorLexico:
    def __init__(self, codigo_fuente):
        self.codigo_fuente = codigo_fuente
        self.tokens = []
        self.linea_actual = 1
        self.columna_actual = 1
        self.contexto = []
        
        # Configuración de Lark
        self.lark_parser = Lark(r"""
            start: (_NEWLINE | stmt)*

            stmt: simple_stmt | compound_stmt
            simple_stmt: small_stmt _NEWLINE
            small_stmt: expr | assign | return_stmt | COMMENT
            compound_stmt: func_def | if_stmt

            func_def: "def" NAME "(" [NAME ("," NAME)*] "):" suite
            if_stmt: "if" expr ":" suite

            suite: _NEWLINE _INDENT stmt+ _DEDENT | simple_stmt

            assign: NAME "=" expr
            return_stmt: "return" expr

            ?expr: NAME | NUMBER | STRING | func_call | expr OP expr | "(" expr ")"
            func_call: NAME "(" [expr ("," expr)*] ")"

            OP: "+" | "-" | "*" | "/" | ">" | "<" | ">=" | "<=" | "==" | "!="
            
            KEYWORD: "if" | "else" | "while" | "for" | "def" | "class" | "return" | "and" | "or" | "not" | "print"
            NAME: /(?!KEYWORD)[a-zA-Z_]\w*/
            NUMBER: /\d+(\.\d+)?/
            STRING: /"[^"]*"/
            COMMENT: /#[^\n]*/

            %import common.WS_INLINE
            %declare _INDENT _DEDENT
            %ignore WS_INLINE
            %import common.NEWLINE -> _NEWLINE
        """, parser='lalr', lexer='standard', propagate_positions=True)

    def analizar(self):
        # Análisis con Lark
        for token in self.lark_parser.lex(self.codigo_fuente):
            tipo_token = self.mapear_tipo_token_lark(token.type, token.value)
            self.tokens.append(Token(tipo_token, token.value, token.line, token.column))

        return self.tokens

    def mapear_tipo_token_lark(self, tipo_lark, valor):
        mapa = {
            'NUMBER': TipoToken.NUMERO,
            'STRING': TipoToken.CADENA,
            'NAME': TipoToken.IDENTIFICADOR,
            'OP': TipoToken.OPERADOR_ARITMETICO,
            'COMMENT': TipoToken.COMENTARIO,
            '_NEWLINE': TipoToken.FIN_DE_LINEA,
            'LPAR': TipoToken.PARENTESIS_IZQ,
            'RPAR': TipoToken.PARENTESIS_DER,
            'LBRACE': TipoToken.LLAVE_IZQ,
            'RBRACE': TipoToken.LLAVE_DER,
            'COMMA': TipoToken.COMA,
            'COLON': TipoToken.DOS_PUNTOS,
            'KEYWORD': TipoToken.PALABRA_CLAVE,
        }
        if valor in ["if", "else", "while", "for", "def", "class", "return", "and", "or", "not", "print"]:
            return TipoToken.PALABRA_CLAVE
        return mapa.get(tipo_lark, TipoToken.IDENTIFICADOR)

# Ejemplo de uso
codigo = """
def calcular(x, y):
    # Esta función calcula la suma de dos números
    resultado = x + y  # Suma
    if resultado > 10:
        print("El resultado es mayor que 10")
    return resultado

# Llamada a la función
total = calcular(5, 7)
"""

try:
    analizador = AnalizadorLexico(codigo)
    tokens = analizador.analizar()
    for token in tokens:
        print(token)
except ErrorLexico as e:
    print(f"Error léxico: {e}")

# Pruebas unitarias
import unittest

class TestAnalizadorLexico(unittest.TestCase):
    def test_numeros(self):
        codigo = "42 3.14"
        analizador = AnalizadorLexico(codigo)
        tokens = analizador.analizar()
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].tipo, TipoToken.NUMERO)
        self.assertEqual(tokens[0].valor, "42")
        self.assertEqual(tokens[1].tipo, TipoToken.NUMERO)
        self.assertEqual(tokens[1].valor, "3.14")

    def test_operadores(self):
        codigo = "+ - * / > < >= <= == !="
        analizador = AnalizadorLexico(codigo)
        tokens = analizador.analizar()
        self.assertEqual(len(tokens), 10)
        for token in tokens:
            self.assertEqual(token.tipo, TipoToken.OPERADOR_ARITMETICO)

    def test_palabras_clave(self):
        codigo = "if else while for def class return and or not print"
        analizador = AnalizadorLexico(codigo)
        tokens = analizador.analizar()
        self.assertEqual(len(tokens), 11)
        for token in tokens:
            self.assertEqual(token.tipo, TipoToken.PALABRA_CLAVE)

    def test_identificadores(self):
        codigo = "variable_1 _underscore camelCase"
        analizador = AnalizadorLexico(codigo)
        tokens = analizador.analizar()
        self.assertEqual(len(tokens), 3)
        for token in tokens:
            self.assertEqual(token.tipo, TipoToken.IDENTIFICADOR)

if __name__ == '__main__':
    unittest.main()