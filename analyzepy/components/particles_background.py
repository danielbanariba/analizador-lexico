import reflex as rx

def particles_background():
    return rx.html(
        """
        <div id="particles-js"></div>
        <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
        <script>
            document.addEventListener('DOMContentLoaded', (event) => {
                particlesJS("particles-js", {
                    "particles": {
                        "number": {
                            "value": 100,
                            "density": {
                                "enable": true,
                                "value_area": 1000
                            }
                        },
                        "color": {
                            "value": ["#aa73ff", "#f8c210", "#83d238", "#33b1f8"]
                        },
                        "shape": {
                            "type": "circle",
                            "stroke": {
                                "width": 0,
                                "color": "#fff"
                            },
                            "polygon": {
                                "nb_sides": 5
                            }
                        },
                        "opacity": {
                            "value": 0.6,
                            "random": false,
                            "anim": {
                                "enable": false,
                                "speed": 1,
                                "opacity_min": 0.1,
                                "sync": false
                            }
                        },
                        "size": {
                            "value": 2,
                            "random": true,
                            "anim": {
                                "enable": false,
                                "speed": 40,
                                "size_min": 0.1,
                                "sync": false
                            }
                        },
                        "line_linked": {
                            "enable": true,
                            "distance": 120,
                            "color": "#ffffff",
                            "opacity": 0.4,
                            "width": 1
                        }
                    },
                    "interactivity": {
                        "detect_on": "canvas",
                        "events": {
                            "onhover": {
                                "enable": true,
                                "mode": "grab"
                            },
                            "onclick": {
                                "enable": false
                            },
                            "resize": true
                        },
                        "modes": {
                            "grab": {
                                "distance": 140,
                                "line_linked": {
                                    "opacity": 1
                                }
                            }
                        }
                    },
                    "retina_detect": true
                });
            });
        </script>
        """
    )

particles_style = {
    "#particles-js": {
        "position": "fixed",
        "width": "100%",
        "height": "100%",
        "background": "#111111",
        "z_index": "-1"
    }
}