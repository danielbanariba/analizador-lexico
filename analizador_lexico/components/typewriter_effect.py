import reflex as rx

class TypewriterEffect(rx.Component):
    library = "react"
    tag = "TypewriterEffect"
    
    def render(self):
        return rx.fragment(
            rx.script(
                """
                function TypewriterEffect() {
                    const [text, setText] = React.useState("Analizador y Traductor de Código ");
                    const fullText = "Analizador y Traductor de Código Python a JavaScript";
                    const baseText = "Analizador y Traductor de Código ";
                    const variations = ["Python", "a JavaScript"];
                    const [currentVariation, setCurrentVariation] = React.useState(0);
                    const [isDeleting, setIsDeleting] = React.useState(false);

                    React.useEffect(() => {
                        const typeEffect = () => {
                            const current = baseText + variations[currentVariation];
                            if (isDeleting) {
                                setText((prev) => prev.slice(0, -1));
                                if (text === baseText) {
                                    setIsDeleting(false);
                                    setCurrentVariation((prev) => (prev + 1) % variations.length);
                                }
                            } else {
                                setText(current.slice(0, text.length + 1));
                                if (text === current) {
                                    setIsDeleting(true);
                                }
                            }
                        };

                        const timeout = setTimeout(typeEffect, isDeleting ? 50 : 100);
                        return () => clearTimeout(timeout);
                    }, [text, isDeleting, currentVariation]);

                    return React.createElement("h1", { style: { color: "blue", fontSize: "2em" } }, text);
                }
                """
            ),
            self.tag.create()
        )

def typewriter_effect():
    return TypewriterEffect()