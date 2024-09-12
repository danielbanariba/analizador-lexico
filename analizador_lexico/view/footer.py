import reflex as rx
import datetime
import analizador_lexico.styles.styles as styles
from analizador_lexico.styles.styles import Size, Color, TextColor
import analizador_lexico.data.url as URL 

def footer() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.link(
                rx.text(
                    """DANIEL\nBANARIBA""",
                    color=Color.LOGO_CANAL.value,
                    style=styles.logo_canal,
                    alt="Logotipo de DanielBanariba.",
                ),
                href=URL.DANIEL_BANARIBA,
                target="_blank",
                is_external=True,
                font_size=Size.ALGO_GRANDE.value,
            ),
            rx.text(
                "Transformando Ideas en Código | Ingeniero de Software Full Stack",
                font_size=Size.MEDIUM.value,
            ),
            rx.center(
                rx.text(
                    f" © 2023-{datetime.datetime.today().year}",
                    font_size=Size.MEDIUM.value,  
                ),
            ),
            width="100%",
            align_items="center",
            padding_top=Size.DEFAULT.value,
            margin_bottom=Size.ZERO.value,
            padding_botoom=Size.ZERO.value, # Para que se separare el texto de la parte de abajo
            padding_x=Size.BIG.value, # Responsive, se separe el texto de los lados
            spacing=Size.ZERO.value,
            color=TextColor.FOOTER.value
        )
    )