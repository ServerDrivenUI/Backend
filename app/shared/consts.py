from enum import StrEnum

SDUI_TEMPLATES = {
    "templates": {
        "_template_close": {
            "accessibility": {
                "description": "Закрыть",
                "mode": "merge",
                "type": "button",
            },
            "actions": [{"log_id": "close_popup", "url": "div-screen://close"}],
            "image_url": "https://yastatic.net/s3/home/div/div_fullscreens/cross2.3.png",
            "tint_color": "#73000000",
            "type": "image",
        },
        "_template_button": {
            "type": "text",
            "$actions": "actions",
            "text_alignment_horizontal": "center",
            "text_alignment_vertical": "center",
            "border": {"$corner_radius": "corners"},
            "paddings": {"bottom": 24, "left": 28, "right": 28, "top": 22},
            "width": {"type": "wrap_content"},
        },
    }
}


class Colors(StrEnum):
    PRIMARY: str = "#42b077"
    DARK: str = "#018a51"
    WHITE: str = "#f0fff0"
    BLACK: str = "#121212"
    BLACK_TEXT_1: str = "#e6121212"
    BLACK_TEXT_2: str = "#b3121212"


class DesignIds(StrEnum):
    GREEN: str = "green"
    BLACK: str = "black"


LOCAL_PHOTO = "http://localhost:5200/assets/clothes.jpg"
GLOBAL_PHOTO = (
    "https://i.pinimg.com/originals/fa/f4/06/faf406a7a9f1aca387946d5d96d59c34.jpg"
)
