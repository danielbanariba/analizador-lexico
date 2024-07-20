import re

class Token:
    """
    Representa un token individual en el análisis léxico.
    
    Atributos:
    - tipo: El tipo de token (por ejemplo, 'NUMERO', 'IDENTIFICADOR', etc.)
    - valor: El valor literal del token
    - linea: El número de línea donde se encontró el token
    - columna: La posición de la columna donde comienza el token
    """
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna

    def __str__(self):
        return f'Token({self.tipo}, {self.valor}, linea:{self.linea}, columna:{self.columna})'

class AnalizadorLexico:
    """
    Clase principal para realizar el análisis léxico del código fuente.
    
    Atributos:
    - codigo_fuente: El texto del código fuente a analizar
    - tokens: Lista para almacenar los tokens generados
    - linea_actual: Número de línea actual en el análisis
    - columna_actual: Número de columna actual en el análisis
    """
    def __init__(self, codigo_fuente):
        self.codigo_fuente = codigo_fuente
        self.tokens = []
        self.linea_actual = 1
        self.columna_actual = 1

    def analizar(self):
        """
        Realiza el análisis léxico del código fuente.
        
        Retorna:
        - Una lista de objetos Token si el análisis es exitoso
        - None si se encuentra un error durante el análisis
        """
        # Definición de patrones para cada tipo de token
        patrones = [
            ('NUMERO', r'\d+(\.\d+)?'),  # Enteros o flotantes
            ('IDENTIFICADOR', r'[a-zA-Z_]\w*'),  # Identificadores
            ('OPERADOR', r'[+\-*/=]'),  # Operadores básicos
            ('PARENTESIS_IZQ', r'\('),  # Paréntesis izquierdo
            ('PARENTESIS_DER', r'\)'),  # Paréntesis derecho
            ('ESPACIO', r'\s+'),  # Espacios en blanco (ignorados en tokens finales)
        ]

        while self.codigo_fuente:
            match = None
            for token_tipo, patron in patrones:
                regex = re.compile(patron)
                match = regex.match(self.codigo_fuente)
                if match:
                    valor = match.group(0)
                    if token_tipo != 'ESPACIO':
                        # Crear y almacenar el token si no es un espacio
                        token = Token(token_tipo, valor, self.linea_actual, self.columna_actual)
                        self.tokens.append(token)
                    self.actualizar_posicion(valor)
                    # Avanzar en el código fuente
                    self.codigo_fuente = self.codigo_fuente[len(valor):]
                    break
            
            if not match:
                # Reportar error si no se reconoce el carácter
                print(f"Error: Carácter no reconocido en línea {self.linea_actual}, columna {self.columna_actual}")
                return None

        return self.tokens

    def actualizar_posicion(self, valor):
        """
        Actualiza la posición actual (línea y columna) después de procesar un token.
        
        Parámetros:
        - valor: El valor del token procesado
        """
        lineas = valor.split('\n')
        if len(lineas) > 1:
            # Si el valor contiene saltos de línea
            self.linea_actual += len(lineas) - 1
            self.columna_actual = len(lineas[-1]) + 1
        else:
            # Si es en la misma línea, solo avanzamos la columna
            self.columna_actual += len(valor)

# Ejemplo de uso del analizador léxico
codigo = """
x = 10
y = 20.5
resultado = (x + y) * 2
"""

# Crear una instancia del analizador y procesar el código
analizador = AnalizadorLexico(codigo)
tokens = analizador.analizar()

# Imprimir los tokens generados
if tokens:
    for token in tokens:
        print(token)