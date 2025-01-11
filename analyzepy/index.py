from analyzepy.components.custom_table import custom_table
from analyzepy.components.github_icon import github_icon
from analyzepy.components.file_upload import file_upload_component
from analyzepy.components.icons import python_icon, javascript_icon
from analyzepy.components.typewriter_effect import typewriter_effect
from analyzepy.components.particles_background import particles_background, particles_style
from analyzepy.state import State
from analyzepy.view.footer import footer
from analyzepy.styles.styles import Size, Color, TextColor
import reflex as rx

def index():
    return rx.box(
        rx.box(
            particles_background(),
            rx.vstack(
                rx.heading(
                    "Analizador y Traductor de Código Python a JavaScript",
                    text_align="center",
                    width="100%",
                ),
                rx.hstack(
                    rx.spacer(),
                    rx.hstack(
                        python_icon("95", "95"),
                        rx.icon("arrow-right", stroke_width=2.5, size=100),
                        javascript_icon("95", "95"),
                        spacing=Size.ZERO.value,
                    ),
                    rx.spacer(),
                    github_icon(),
                    width="100%",
                    justify="between",
                ),
                rx.box(
                    file_upload_component(),
                    width="100%",
                ),
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
                rx.heading("Análisis Léxico", size="3"),
                custom_table(State.lexical_output),
                rx.divider(),
                rx.heading("Análisis Sintáctico", size="3"),
                rx.code_block(
                    State.syntax_output,
                    theme=rx.code_block.themes.twilight,
                    language="apex",
                    show_line_numbers=True,
                    width="100%"
                ),
                rx.divider(),
                rx.heading("Árbol Sintáctico", size="3"),
                rx.box(
                    State.tree_image,
                    width="100%",
                    overflow_x="auto",
                    white_space="pre-wrap",
                    font_family="monospace",
                    bg="gray.100",
                    p="4",
                    border_radius="3",
                ),
                rx.divider(),
                rx.heading("Código JavaScript", size="3"),
                rx.code_block(
                    State.js_output,
                    theme=rx.code_block.themes.one_dark,
                    language="javascript",
                    show_line_numbers=True,
                    width="100%"
                ),
                width="100%",
                max_width="700px",
                margin="0 auto",
                spacing="4",
                padding="4",
                bg="rgba(17, 17, 17, 0.9)",
                border_radius="3",
                box_shadow="lg",
            ),
            width="100%",
            height="100%",
            overflow_y="auto",
            padding_top="1em",
            style=particles_style,
        ),
        footer()
    )