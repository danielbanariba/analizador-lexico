import reflex as rx
from analizador_lexico.components.custom_table import custom_table
from ..analizador_lexico import State

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
            rx.hstack(
                rx.button("Analizar y Traducir", on_click=State.analyze_code),
                rx.button("Limpiar", on_click=State.clear_all),
            ),
            rx.divider(),
            rx.heading("Análisis Léxico", size="md"),
            custom_table(State.lexical_output),
            rx.heading("Análisis Sintáctico", size="md"),
            rx.text_area(value=State.syntax_output, is_read_only=True, height="200px", width="100%"),
            rx.heading("Árbol Sintáctico", size="md"),
            rx.text_area(value=State.tree_image, is_read_only=True, height="200px", width="100%", font_family="monospace", white_space="pre-wrap"),
            rx.heading("Código JavaScript", size="md"),
            rx.text_area(value=State.js_output, is_read_only=True, height="200px", width="100%"),
            rx.heading("Información de Depuración", size="md"),
            rx.text_area(value=State.debug_output, is_read_only=True, height="300px", width="100%"),
            width="100%",
            max_width="800px",
            spacing="4",
        )
    )