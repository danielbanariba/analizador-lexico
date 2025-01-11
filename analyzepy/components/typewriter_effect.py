import reflex as rx

def typewriter_effect():
    return rx.html(
        """
        <!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Text Carousel Animation</title>
            <style>
                .typing-container {
                display: inline-block;
                font-size: 24px;
                font-family: monospace;
                white-space: nowrap;
                overflow: hidden;
                }
                .input-cursor {
                display: inline-block;
                width: 2px;
                height: 1em;
                background-color: black;
                animation: blink 0.7s step-end infinite;
                }
                @keyframes blink {
                from, to {
                    background-color: transparent;
                }
                50% {
                    background-color: black;
                }
                }
            </style>
            <!-- Include jQuery -->
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            </head>
            <body>
            <div class="typing-container">
                <span id="sentence" class="sentence">Analizador y Traductor de Código </span>
                <span id="feature-text"></span>
                <span class="input-cursor"></span>
            </div>

            <script>
                const carouselText = [
                {text: "Python"},
                {text: "JavaScript"},
                {text: "Python a JavaScript"}
                ];

                $(document).ready(async function() {
                carousel(carouselText, "#feature-text");
                });

                async function typeSentence(sentence, eleRef, delay = 100) {
                const letters = sentence.split("");
                let i = 0;
                while (i < letters.length) {
                    await waitForMs(delay);
                    $(eleRef).append(letters[i]);
                    i++;
                }
                return;
                }

                async function deleteSentence(eleRef) {
                const sentence = $(eleRef).html();
                const letters = sentence.split("");
                let i = 0;
                while (letters.length > 0) {
                    await waitForMs(100);
                    letters.pop();
                    $(eleRef).html(letters.join(""));
                }
                }

                async function carousel(carouselList, eleRef) {
                var i = 0;
                while (true) {
                    updateFontColor(eleRef, carouselList[i].color);
                    await typeSentence(carouselList[i].text, eleRef);
                    await waitForMs(1500);
                    await deleteSentence(eleRef);
                    await waitForMs(500);
                    i++;
                    if (i >= carouselList.length) {
                    i = 0;
                    }
                }
                }

                function updateFontColor(eleRef, color) {
                $(eleRef).css('color', color);
                }

                function waitForMs(ms) {
                return new Promise(resolve => setTimeout(resolve, ms));
                }
            </script>
            </body>
            </html>

        """
    )