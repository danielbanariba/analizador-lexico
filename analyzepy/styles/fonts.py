from enum import Enum

class Font(Enum):
    DEFAULT = "Poppins" # tiene que tener el mismo nombre que la variable StileSheets, dentro del css
    TITLE = "Poppins"
    LOGO = "DinaRemasterII"
    LOGO_CANAL = "Pulse_virgin"


class FontWeight(Enum):
    LIGHT = "300"
    MEDIUM = "500"