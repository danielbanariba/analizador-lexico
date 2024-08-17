import reflex as rx
from analizador_lexico.state import State

def file_upload_component():
    return rx.box(
        rx.upload(
            rx.center(
                rx.vstack(
                    rx.center(
                        rx.icon("upload", stroke_width=2.5, size=42), 
                        size="lg", 
                        color="fff0ff", 
                        width="100%",
                    ),
                    rx.text("Arrastra y suelta un archivo Python aquí o haz clic para seleccionar"),
                ),
            ),
            id="python_file_upload",
            accept={".py": ["text/x-python"]},
            max_files=1,
            border="1px dashed",
            padding="2em",
            on_drop=State.handle_file_upload(rx.upload_files(upload_id="python_file_upload")),
        ),
        rx.hstack(rx.foreach(rx.selected_files("python_file_upload"), rx.text)),
        spacing="4",
    )