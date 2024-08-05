import reflex as rx
from enum import Enum, auto
import re
import json
import os

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
    CORCHETE_IZQ = auto()
    CORCHETE_DER = auto()
    PALABRA_CLAVE = auto()
    CADENA = auto()
    COMENTARIO = auto()
    FIN_DE_LINEA = auto()
    ESPACIO = auto()
    COMA = auto()
    PUNTO_Y_COMA = auto()
    DOS_PUNTOS = auto()
    PUNTO = auto()
    DIRECTIVA_PREPROCESADOR = auto()

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
        self.lenguaje = self.detectar_lenguaje()

    def detectar_lenguaje(self):
        caracteristicas = {
            'python': [
                (r'\bdef\s+\w+\s*\(', 'definición de función'),
                (r'\bclass\s+\w+:', 'definición de clase'),
                (r':\s*$', 'uso de dos puntos al final de la línea'),
                (r'\bif\s+.*:\s*$', 'estructura if con dos puntos'),
                (r'\bimport\s+\w+', 'declaración de importación'),
                (r'#.*$', 'comentario de una línea'),
            ],
            'java': [
                (r'\bpublic\s+class\s+\w+', 'definición de clase pública'),
                (r'\bprivate|protected|public', 'modificadores de acceso'),
                (r'\bvoid\s+main\s*\(String\[\]\s+\w+\)', 'método main'),
                (r'System\.out\.println', 'impresión en consola'),
                (r'//.*$', 'comentario de una línea'),
                (r'/\*[\s\S]*?\*/', 'comentario multilínea'),
            ],
            'c++': [
                (r'#include\s*<\w+>', 'inclusión de biblioteca'),
                (r'\bstd::', 'uso del espacio de nombres std'),
                (r'\bcout\s*<<', 'impresión en consola'),
                (r'\busing\s+namespace\s+std;', 'declaración de espacio de nombres'),
                (r'//.*$', 'comentario de una línea'),
                (r'/\*[\s\S]*?\*/', 'comentario multilínea'),
            ],
            'javascript': [
                (r'\bfunction\s+\w+\s*\(', 'definición de función'),
                (r'\bconst\s+\w+\s*=', 'declaración de constante'),
                (r'\blet\s+\w+\s*=', 'declaración de variable con let'),
                (r'\bconsole\.log\s*\(', 'impresión en consola'),
                (r'\bconst\s+\w+\s*=\s*\(\)\s*=>', 'función flecha'),
                (r'//.*$', 'comentario de una línea'),
                (r'/\*[\s\S]*?\*/', 'comentario multilínea'),
            ]
        }

        puntuaciones = {lenguaje: 0 for lenguaje in caracteristicas}

        for lenguaje, patrones in caracteristicas.items():
            for patron, _ in patrones:
                if re.search(patron, self.codigo_fuente, re.MULTILINE):
                    puntuaciones[lenguaje] += 1

        lenguaje_detectado = max(puntuaciones, key=puntuaciones.get)
        confianza = puntuaciones[lenguaje_detectado] / sum(puntuaciones.values()) if sum(puntuaciones.values()) > 0 else 0

        if confianza < 0.5:
            return 'desconocido'
        return lenguaje_detectado

    def analizar(self):
        self.tokens = []  # Reiniciamos la lista de tokens
        patrones = self.obtener_patrones()

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

    def obtener_patrones(self):
        patrones_comunes = [
            (TipoToken.ESPACIO, r'\s+'),
            (TipoToken.NUMERO, r'\d+(\.\d+)?'),
            (TipoToken.OPERADOR_COMPARACION, r'==|!=|<=|>=|<|>'),
            (TipoToken.OPERADOR_ARITMETICO, r'[+\-*/]'),
            (TipoToken.OPERADOR_ASIGNACION, r'='),
            (TipoToken.PARENTESIS_IZQ, r'\('),
            (TipoToken.PARENTESIS_DER, r'\)'),
            (TipoToken.LLAVE_IZQ, r'\{'),
            (TipoToken.LLAVE_DER, r'\}'),
            (TipoToken.CORCHETE_IZQ, r'\['),
            (TipoToken.CORCHETE_DER, r'\]'),
            (TipoToken.COMA, r','),
            (TipoToken.PUNTO_Y_COMA, r';'),
            (TipoToken.DOS_PUNTOS, r':'),
            (TipoToken.PUNTO, r'\.'),
        ]

        if self.lenguaje == 'python':
            return patrones_comunes + [
                (TipoToken.COMENTARIO, r'#.*'),
                (TipoToken.PALABRA_CLAVE, r'\b(if|else|elif|while|for|def|class|return|and|or|not|in|is|True|False|None|import|from|as|try|except|finally|with|lambda|nonlocal|global|yield)\b'),
                (TipoToken.CADENA, r'(\'\'\'[\s\S]*?\'\'\'|"""[\s\S]*?"""|"[^"]*"|\'[^\']*\')'),
                (TipoToken.IDENTIFICADOR, r'[a-zA-Z_]\w*'),
            ]
        elif self.lenguaje == 'java':
            return patrones_comunes + [
                (TipoToken.COMENTARIO, r'//.*|/\*[\s\S]*?\*/'),
                (TipoToken.PALABRA_CLAVE, r'\b(if|else|while|for|class|return|public|private|protected|static|final|void|int|double|boolean|String|new|try|catch|throws|throw|interface|implements|extends|abstract|super|this)\b'),
                (TipoToken.CADENA, r'"[^"]*"'),
                (TipoToken.IDENTIFICADOR, r'[a-zA-Z_$][a-zA-Z0-9_$]*'),
            ]
        elif self.lenguaje == 'c++':
            return patrones_comunes + [
                (TipoToken.DIRECTIVA_PREPROCESADOR, r'#\w+'),  # Nueva regla para #include y otras directivas
                (TipoToken.COMENTARIO, r'//.*|/\*[\s\S]*?\*/'),
                (TipoToken.PALABRA_CLAVE, r'\b(if|else|while|for|class|return|public|private|protected|static|const|void|int|double|float|bool|char|struct|template|namespace|using|try|catch|throw|virtual|friend|inline|operator|delete|new|this)\b'),
                (TipoToken.CADENA, r'"[^"]*"'),
                (TipoToken.IDENTIFICADOR, r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ]
        elif self.lenguaje == 'javascript':
            return patrones_comunes + [
                (TipoToken.COMENTARIO, r'//.*|/\*[\s\S]*?\*/'),
                (TipoToken.PALABRA_CLAVE, r'\b(if|else|while|for|function|return|var|let|const|class|import|export|from|async|await|try|catch|finally|throw|typeof|instanceof|in|of|new|this|super|delete|yield|debugger|break|continue)\b'),
                (TipoToken.CADENA, r'(\'\'\'[\s\S]*?\'\'\'|"""[\s\S]*?"""|"[^"]*"|\'[^\']*\')'),
                (TipoToken.IDENTIFICADOR, r'[a-zA-Z_$][a-zA-Z0-9_$]*'),
            ]
        else:
            return patrones_comunes + [
                (TipoToken.COMENTARIO, r'(#.*|//.*|/\*[\s\S]*?\*/)'),
                (TipoToken.PALABRA_CLAVE, r'\b\w+\b'),
                (TipoToken.CADENA, r'(\'\'\'[\s\S]*?\'\'\'|"""[\s\S]*?"""|"[^"]*"|\'[^\']*\')'),
                (TipoToken.IDENTIFICADOR, r'[a-zA-Z_$][a-zA-Z0-9_$]*'),
                (TipoToken.DIRECTIVA_PREPROCESADOR, r'#\w+'),  # Añadido para cubrir casos generales
            ]

    def actualizar_posicion(self, valor):
        for char in valor:
            if char == '\n':
                self.linea_actual += 1
                self.columna_actual = 1
            else:
                self.columna_actual += 1

class State(rx.State):
    codigo: str = """def calcular(x, y):
    # Esta función calcula la suma de dos números
    resultado = x + y  # Suma
    if resultado > 10:
        print("El resultado es mayor que 10")
    return resultado

# Llamada a la función
total = calcular(5, 7)
"""
    resultado: list = []
    archivo_subido: str = ""
    debug_info: str = ""
    lenguaje_detectado: str = ""

    def analizar(self):
        codigo_a_analizar = self.archivo_subido if self.archivo_subido else self.codigo
        analizador = AnalizadorLexico(codigo_a_analizar)
        self.lenguaje_detectado = analizador.lenguaje
        self.debug_info = f"Lenguaje detectado: {self.lenguaje_detectado}\n"
        self.debug_info += f"Código a analizar:\n{codigo_a_analizar[:500]}..."
        try:
            tokens = analizador.analizar()
            self.resultado = [str(token) for token in tokens]
            self.debug_info += f"\nAnálisis completado. Tokens encontrados: {len(self.resultado)}"
        except ErrorLexico as e:
            self.resultado = [f"Error léxico: {e}"]
            self.debug_info += f"\nError léxico durante el análisis: {str(e)}"
        except Exception as e:
            self.resultado = [f"Error inesperado: {str(e)}"]
            self.debug_info += f"\nError inesperado durante el análisis: {str(e)}"

    def handle_upload(self, files: list[dict]):
        """Maneja la carga de archivos."""
        self.debug_info = f"Recibido: {json.dumps(files, indent=2)}"
        if files and len(files) > 0:
            file_data = files[0]
            self.debug_info += f"\nPrimer archivo: {json.dumps(file_data, indent=2)}"
            
            if 'path' in file_data:
                file_path = file_data['path']
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        file_content = file.read()
                    self.archivo_subido = file_content
                    self.codigo = file_content
                    self.debug_info += f"\nArchivo leído con éxito: {file_path}"
                    self.debug_info += f"\nContenido del archivo:\n{file_content[:500]}..."
                    self.analizar()
                except Exception as e:
                    self.debug_info += f"\nError al leer el archivo: {str(e)}"
            else:
                self.debug_info += "\nEstructura de archivo no reconocida."
        else:
            self.archivo_subido = ""
            self.debug_info += "\nNo se recibieron archivos."

def index():
    return rx.container(
        rx.vstack(
            rx.heading("Analizador Léxico con Detección Automática", size="lg"),
            rx.upload(
                rx.text("Arrastra y suelta un archivo aquí o haz clic para seleccionar"),
                border="1px dashed",
                padding="20px",
                border_radius="md",
                multiple=False,
                accept={
                    ".txt": "text/plain",
                    ".py": "text/x-python",
                    ".java": "text/x-java-source",
                    ".cpp": "text/x-c++src",
                    ".js": "text/javascript"
                },
                max_files=1,
                on_drop=State.handle_upload,
            ),
            rx.text_area(
                value=State.codigo,
                on_change=State.set_codigo,
                placeholder="Ingrese el código a analizar",
                height="200px",
                width="100%",
            ),
            rx.button("Analizar", on_click=State.analizar),
            rx.divider(),
            rx.heading("Lenguaje Detectado", size="md"),
            rx.text(State.lenguaje_detectado),
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