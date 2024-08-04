import re
from enum import Enum, auto

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
    DOS_PUNTOS = auto()  # Nuevo tipo de token para los dos puntos

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

    def analizar(self):
        patrones = [
            (TipoToken.ESPACIO, r'\s+'),
            (TipoToken.COMENTARIO, r'#.*'),
            (TipoToken.PALABRA_CLAVE, r'\b(if|else|while|for|def|class|return|and|or|not|print)\b'),
            (TipoToken.NUMERO, r'\d+(\.\d+)?'),
            (TipoToken.OPERADOR_COMPARACION, r'==|!=|<=|>=|<|>'),
            (TipoToken.OPERADOR_ARITMETICO, r'[+\-*/]'),
            (TipoToken.OPERADOR_ASIGNACION, r'='),
            (TipoToken.PARENTESIS_IZQ, r'\('),
            (TipoToken.PARENTESIS_DER, r'\)'),
            (TipoToken.LLAVE_IZQ, r'\{'),
            (TipoToken.LLAVE_DER, r'\}'),
            (TipoToken.COMA, r','),
            (TipoToken.PUNTO_Y_COMA, r';'),
            (TipoToken.DOS_PUNTOS, r':'),  # Nuevo patrón para los dos puntos
            (TipoToken.CADENA, r'"[^"]*"'),
            (TipoToken.IDENTIFICADOR, r'[a-zA-Z_]\w*'),
        ]

        while self.codigo_fuente:
            match = None
            for token_tipo, patron in patrones:
                regex = re.compile(patron)
                match = regex.match(self.codigo_fuente)
                if match:
                    valor = match.group(0)
                    if token_tipo not in [TipoToken.ESPACIO, TipoToken.COMENTARIO]:
                        token = Token(token_tipo, valor, self.linea_actual, self.columna_actual)
                        self.tokens.append(token)
                        self.actualizar_contexto(token)
                    self.actualizar_posicion(valor)
                    self.codigo_fuente = self.codigo_fuente[len(valor):]
                    break
            
            if not match:
                raise ErrorLexico(f"Carácter no reconocido '{self.codigo_fuente[0]}' en línea {self.linea_actual}, columna {self.columna_actual}")

        return self.tokens

    def actualizar_posicion(self, valor):
        for char in valor:
            if char == '\n':
                self.linea_actual += 1
                self.columna_actual = 1
            else:
                self.columna_actual += 1

    def actualizar_contexto(self, token):
        if token.tipo in [TipoToken.PARENTESIS_IZQ, TipoToken.LLAVE_IZQ]:
            self.contexto.append(token.tipo)
        elif token.tipo in [TipoToken.PARENTESIS_DER, TipoToken.LLAVE_DER]:
            if self.contexto:
                self.contexto.pop()
            else:
                raise ErrorLexico(f"Error de contexto: '{token.valor}' inesperado en línea {token.linea}, columna {token.columna}")

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
        codigo = "+ - * / == != < > <= >= = :"
        analizador = AnalizadorLexico(codigo)
        tokens = analizador.analizar()
        self.assertEqual(len(tokens), 12)
        self.assertEqual(tokens[0].tipo, TipoToken.OPERADOR_ARITMETICO)
        self.assertEqual(tokens[4].tipo, TipoToken.OPERADOR_COMPARACION)
        self.assertEqual(tokens[-2].tipo, TipoToken.OPERADOR_ASIGNACION)
        self.assertEqual(tokens[-1].tipo, TipoToken.DOS_PUNTOS)

    def test_palabras_clave(self):
        codigo = "if else while for def class return and or not print"
        analizador = AnalizadorLexico(codigo)
        tokens = analizador.analizar()
        self.assertEqual(len(tokens), 11)
        for token in tokens:
            self.assertEqual(token.tipo, TipoToken.PALABRA_CLAVE)

    def test_error_lexico(self):
        codigo = "42 @ 3.14"
        analizador = AnalizadorLexico(codigo)
        with self.assertRaises(ErrorLexico):
            analizador.analizar()

if __name__ == '__main__':
    unittest.main()