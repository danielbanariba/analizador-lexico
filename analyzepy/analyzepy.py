
from analyzepy.index import index
import analyzepy.styles.styles as styles

import reflex as rx

app = rx.App(
    stylesheets=styles.STYLESHEETS,
    style=styles.BASE_STYLE,
)
app.add_page(index)