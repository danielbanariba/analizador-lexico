
from analizador_lexico.index import index
import analizador_lexico.styles.styles as styles

import reflex as rx

app = rx.App(
    stylesheets=styles.STYLESHEETS,
    style=styles.BASE_STYLE,
)
app.add_page(index)