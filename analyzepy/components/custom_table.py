import reflex as rx
from typing import List, Dict

def custom_table(data: rx.Var[List[Dict[str, str]]]):
    return rx.vstack(
        rx.box(
            rx.hstack(
                rx.box("Línea", font_weight="bold", width="20%"),
                rx.box("Tipo de Token", font_weight="bold", width="40%"),
                rx.box("Valor", font_weight="bold", width="40%"),
                width="100%",
                padding="0.5em",
                bg="gray.100",
            ),
            position="sticky",
            top="0",
            z_index="1",
            width="100%",
        ),
        rx.box(
            rx.vstack(
                rx.foreach(
                    data,
                    lambda item: rx.hstack(
                        rx.box(item["linea"], width="20%"),
                        rx.box(item["tipo"], width="40%"),
                        rx.box(item["valor"], width="40%"),
                        width="100%",
                        padding="0.5em",
                        _hover={"bg": "gray.50"},
                    )
                ),
                width="100%",
            ),
            overflow_y="auto",
            height="180px",
            width="100%",
        ),
        height="200px",
        width="100%",
        border="1px solid #ccc",
        border_radius="5px",
    )