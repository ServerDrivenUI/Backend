JWT_ACCESS_TOKEN_EXPIRES = 10

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
            "text_alignment_horizontal": "center",
            "text_alignment_vertical": "center",
            "border": {"$corner_radius": "corners"},
            "paddings": {"bottom": 24, "left": 28, "right": 28, "top": 22},
            "width": {"type": "wrap_content"},
        },
    }
}

COLORS = ["#42b077", "#018a51", "#f0fff0", "#121212", "#e6121212", "#b3121212"]

LOCAL_PHOTO = "http://localhost:5200/assets/clothes.jpg"
GLOBAL_PHOTO = (
    "https://i.pinimg.com/originals/fa/f4/06/faf406a7a9f1aca387946d5d96d59c34.jpg"
)
