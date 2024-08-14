import reflex as rx

def github_icon() -> rx.Component:
    return rx.link(
        rx.icon(
            "github",
            size=40,
            color="#808080",
            _hover={"color": "#ffffff"}
        ),
        href="https://github.com/danielbanariba/analizador-lexico",
        position="fixed",
        top="1em",
        right="1em",
        z_index="1000",
        target="_blank",
        rel="noopener noreferrer"
    )