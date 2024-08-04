import reflex as rx
from enum import Enum, auto
import re

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
            (TipoToken.DOS_PUNTOS, r':'),
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

class State(rx.State):
    codigo: str = """
def calcular(x, y):
    # Esta función calcula la suma de dos números
    resultado = x + y  # Suma
    if resultado > 10:
        print("El resultado es mayor que 10")
    return resultado

# Llamada a la función
total = calcular(5, 7)
"""
    resultado: list = []

    def analizar(self):
        analizador = AnalizadorLexico(self.codigo)
        try:
            tokens = analizador.analizar()
            self.resultado = [str(token) for token in tokens]
        except ErrorLexico as e:
            self.resultado = [f"Error léxico: {e}"]

def index():
    return rx.container(
        rx.vstack(
            rx.heading("Analizador Léxico", size="lg"),
            rx.text_area(
                value=State.codigo,
                on_change=State.set_codigo,
                placeholder="Ingrese el código a analizar",
                height="200px",
                width="100%",
            ),
            rx.button("Analizar", on_click=State.analizar),
            rx.divider(),
            rx.heading("Resultados", size="md"),
            rx.vstack(
                rx.foreach(
                    State.resultado,
                    lambda item: rx.box(
                        rx.text(item),
                        padding="10px",
                        border_radius="md",
                        bg="gray.100",
                        width="100%",
                    )
                ),
                width="100%",
                align_items="stretch",
            ),
            width="100%",
            max_width="800px",
            margin="0 auto",
            padding="20px",
        )
    )

app = rx.App()
app.add_page(index)

if __name__ == "__main__":
    app.compile()