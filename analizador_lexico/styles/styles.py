import reflex as rx
from enum import Enum
from analizador_lexico.styles.colors import Color, TextColor
from analizador_lexico.styles.fonts import Font, FontWeight

# Ancho maximo de la pagina 
MAX_WIDTH = "800px"
TAMANIO_ICON = 1.7

#Hojas de estilos
STYLESHEETS = [
    "https://fonts.googleapis.com/css2?family=Poppins:wght@300;500&display=swap",
    "fonts/fonts.css"
]

class Size(Enum):
    ZERO = "0px !important"
    VERY_SMALL = "0.2em"
    SMALL = "0.5em"
    MEDIUM = "0.8em"
    DEFAULT = "1em"
    ALGO_GRANDE = "1.1em"
    LARGE = "1.5em"
    GRANDELOGO = "1.7em"
    BIG = "2.2em"
    VERY_BIG = "3em"


# Styles
BASE_STYLE = {
    rx.link: {    
        "text_decoration": "none",    
        "_hover": {
            "text_decoration": "none"    
        }
    }
}

logo_canal = dict(
    font_family=Font.LOGO_CANAL.value,
    font_weight=FontWeight.MEDIUM.value,
    font_size=Size.GRANDELOGO.value,
    _hover={"color": "#626c80"},
)

# Estilos de los textos que van arriba de los botones
title_style = dict(
    width="100%",
    padding_top=Size.DEFAULT.value,
    font_size=Size.LARGE.value
)