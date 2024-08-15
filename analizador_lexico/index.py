
from analizador_lexico.components.custom_table import custom_table
from analizador_lexico.components.github_icon import github_icon
from analizador_lexico.state import State
import reflex as rx

def index():
    return rx.container(
        github_icon(),
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
            rx.divider(),
            rx.heading("Análisis Sintáctico", size="md"),
            rx.code_block(
                State.syntax_output,
                theme="twilight", #twilight, xonokai
                language="apex",
                show_line_numbers=True,
                width="100%"
            ),
            rx.divider(),
            rx.heading("Árbol Sintáctico", size="md"),
            rx.box(
                State.tree_image,
                width="100%",
                overflow_x="auto",
                white_space="pre-wrap",
                font_family="monospace",
                bg="gray.100",
                p="4",
                border_radius="md",
            ),
            rx.divider(),
            rx.heading("Código JavaScript", size="md"),
            rx.code_block(
                State.js_output, 
                theme="one-dark",
                language="javascript",
                show_line_numbers=True,
                width="100%"
            ),
            # rx.heading("Información de Depuración", size="md"),
            # rx.text_area(value=State.debug_output, is_read_only=True, height="300px", width="100%"),
            width="100%",
            max_width="800px",
            spacing="4",
        )
    )