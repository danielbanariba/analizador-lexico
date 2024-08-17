import reflex as rx

def infinite_background_style() -> dict:
    symbols = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Cstyle%3E.symbol %7B fill: %23ffffff; font-family: monospace; font-size: 14px; opacity: 0.15;%7D%3C/style%3E%3Ctext x='10' y='20' class='symbol'%3E%7B%7D%3C/text%3E%3Ctext x='60' y='20' class='symbol'%3E%28%29%3C/text%3E%3Ctext x='30' y='50' class='symbol'%3E%5B%5D%3C/text%3E%3Ctext x='70' y='50' class='symbol'%3E%3C%3E%3C/text%3E%3Ctext x='10' y='80' class='symbol'%3E%3B%3D%3C/text%3E%3Ctext x='60' y='80' class='symbol'%3E%2B-%3C/text%3E%3C/svg%3E"
    
    return {
        "min_height": "100vh",
        "width": "100%",
        "margin": "0",
        "padding": "0",
        "color": "#e0e0e0",
        "font_family": "exo, ubuntu, 'segoe ui', helvetica, arial, sans-serif",
        "font_weight": "400",
        "font_size": "16px",
        "line_height": "1.5",
        "text_align": "center",
        "background_color": "#1a1a1a",
        "background_image": f"url('{symbols}')",
        "background_repeat": "repeat",
        "background_size": "100px 100px",
        "animation": "bg-scrolling 20s infinite linear",
        "@keyframes bg-scrolling": {
            "0%": {"background_position": "0 0"},
            "100%": {"background_position": "100px 100px"},
        },
    }

def infinity_text_style() -> dict:
    return {
        "position": "fixed",
        "top": "50%",
        "left": "50%",
        "transform": "translate(-50%, -50%)",
        "font_size": "8rem",
        "font_weight": "100",
        "font_style": "normal",
        "color": "rgba(255, 255, 255, 0.1)",
        "z_index": "-1",
    }
    
def background_component():
    return rx.box(
        rx.html("""
        <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" style="position: fixed; top: 0; left: 0; z-index: -1;">
            <pattern id="pattern" x="0" y="0" width="100" height="100" patternUnits="userSpaceOnUse">
                <text x="10" y="20" fill="#ffffff" opacity="0.1" font-family="monospace" font-size="14">{}</text>
                <text x="60" y="20" fill="#ffffff" opacity="0.1" font-family="monospace" font-size="14">()</text>
                <text x="30" y="50" fill="#ffffff" opacity="0.1" font-family="monospace" font-size="14">[]</text>
                <text x="70" y="50" fill="#ffffff" opacity="0.1" font-family="monospace" font-size="14"><></text>
                <text x="10" y="80" fill="#ffffff" opacity="0.1" font-family="monospace" font-size="14">;=</text>
                <text x="60" y="80" fill="#ffffff" opacity="0.1" font-family="monospace" font-size="14">+-</text>
            </pattern>
            <rect x="0" y="0" width="100%" height="100%" fill="url(#pattern)">
                <animate attributeName="x" from="0" to="100" dur="20s" repeatCount="indefinite"/>
                <animate attributeName="y" from="0" to="100" dur="20s" repeatCount="indefinite"/>
            </rect>
        </svg>
        """),
        style={
            "position": "fixed",
            "top": "0",
            "left": "0",
            "width": "100%",
            "height": "100%",
            "z_index": "-1",
        }
    )