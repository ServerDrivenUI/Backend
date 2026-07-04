from typing import List, Optional
from beanie import Document, Link
from pydantic import Field


class User(Document):
    """Модель Пользователя"""

    login: str = Field(unique=True)
    password_hash: str
    is_impulsive: bool = Field(default=False)

    class Settings:
        name = "users"


class ClothesItem(Document):
    """Модель Вещи (clothes)"""

    price: int
    name: str
    descripton: str

    class Settings:
        name = "clothes_items"


class Cart(Document):
    """Модель Корзины"""

    user: Link[User]
    clothes: Link[ClothesItem]

    class Settings:
        name = "carts"


class Order(Document):
    """Модель Заказа"""

    user: Link[User]

    class Settings:
        name = "orders"


class OrderItem(Document):
    """Модель Элемента заказа"""

    order: Link[Order]
    clothes: Link[ClothesItem]

    class Settings:
        name = "order_items"


class Page(Document):
    """Модель Страницы (независимая)"""

    type: str
    json_dict: str

    class Settings:
        name = "pages"


class UIElement(Document):
    """Модель Элемента UI (независимая)"""

    is_for_impulsive: bool = Field(default=False)
    json_dict: str
    type: str

    class Settings:
        name = "ui_elements"


def get_beanie_models():
    """Регистрация всех новых моделей для DatabaseExtension"""
    return [User, ClothesItem, Cart, Order, OrderItem, Page, UIElement]

"""
{
  "card": {
    "log_id": "div2_sample_card",
    "states": [
      {
        "state_id": 0,
        "div": {
          "items": [
            {
              "type": "container",
              "width": {
                "type": "match_parent"
              },
              "height": {
                "type": "match_parent"
              },
              "items": [
                {
                  "type": "image",
                  "image_url": "empty://",
                  "width": {
                    "type": "match_parent"
                  },
                  "height": {
                    "type": "match_parent"
                  },
                  "preload_required": true,
                  "margins": {
                    "bottom": 10
                  },
                  "border": {
                    "corner_radius": 20
                  }
                },
                {
                  "type": "text",
                  "text": "text",
                  "font_size": 25,
                  "width": {
                    "type": "match_parent"
                  },
                  "font_weight": "bold",
                  "text_color": "#e6121212",
                  "height": {
                    "type": "fixed",
                    "value": 32
                  }
                },
                {
                  "type": "text",
                  "text": "text",
                  "font_size": 20,
                  "width": {
                    "type": "match_parent"
                  },
                  "margins": {
                    "bottom": 20
                  },
                  "text_color": "#b3121212"
                },
                {
                  "text": "В корзину",
                  "background": [
                    {
                      "type": "solid",
                      "color": "#42b077"
                    }
                  ],
                  "text_color": "#fff",
                  "corners": 4,
                  "type": "_template_button",
                  "width": {
                    "type": "match_parent"
                  },
                  "margins": {
                    "bottom": 10
                  },
                  "font_size": 20,
                  "paddings": {
                    "top": 10,
                    "right": 28,
                    "bottom": 10,
                    "left": 28
                  },
                  "text_alignment_horizontal": "center",
                  "border": {
                    "corner_radius": 15
                  }
                },
                {
                  "text": "Купить",
                  "background": [
                    {
                      "type": "solid",
                      "color": "#018a51"
                    }
                  ],
                  "text_color": "#fff",
                  "corners": 4,
                  "type": "_template_button",
                  "width": {
                    "type": "match_parent"
                  },
                  "font_size": 20,
                  "paddings": {
                    "top": 15,
                    "right": 28,
                    "bottom": 15,
                    "left": 28
                  },
                  "border": {
                    "corner_radius": 15
                  }
                }
              ],
              "border": {
                "corner_radius": 15
              },
              "paddings": {
                "right": 15,
                "left": 15,
                "top": 15,
                "bottom": 10
              },
              "alpha": 1,
              "background": [
                {
                  "type": "solid",
                  "color": "#f0fff0"
                }
              ]
            }
          ],
          "background": [
            {
              "color": "#000000",
              "type": "solid"
            }
          ],
          "height": {
            "type": "match_parent"
          },
          "orientation": "vertical",
          "type": "container",
          "content_alignment_vertical": "top",
          "content_alignment_horizontal": "center"
        }
      }
    ]
  },
  "templates": {
    "_template_close": {
      "accessibility": {
        "description": "Закрыть",
        "mode": "merge",
        "type": "button"
      },
      "actions": [
        {
          "log_id": "close_popup",
          "url": "div-screen://close"
        }
      ],
      "image_url": "https://yastatic.net/s3/home/div/div_fullscreens/cross2.3.png",
      "tint_color": "#73000000",
      "type": "image"
    },
    "_template_button": {
      "type": "text",
      "text_alignment_horizontal": "center",
      "text_alignment_vertical": "center",
      "border": {
        "$corner_radius": "corners"
      },
      "paddings": {
        "bottom": 24,
        "left": 28,
        "right": 28,
        "top": 22
      },
      "width": {
        "type": "wrap_content"
      }
    }
  }
}
"""
"""
{
              "type": "container",
              "width": {
                "type": "match_parent"
              },
              "height": {
                "type": "match_parent"
              },
              "items": [
                {
                  "type": "image",
                  "image_url": "empty://",
                  "width": {
                    "type": "match_parent"
                  },
                  "height": {
                    "type": "match_parent"
                  },
                  "preload_required": true,
                  "margins": {
                    "bottom": 10
                  },
                  "border": {
                    "corner_radius": 20
                  }
                },
                {
                  "type": "text",
                  "text": "text",
                  "font_size": 25,
                  "width": {
                    "type": "match_parent"
                  },
                  "font_weight": "bold",
                  "text_color": "#e6121212",
                  "height": {
                    "type": "fixed",
                    "value": 32
                  }
                },
                {
                  "type": "text",
                  "text": "text",
                  "font_size": 20,
                  "width": {
                    "type": "match_parent"
                  },
                  "margins": {
                    "bottom": 20
                  },
                  "text_color": "#b3121212"
                },
                {
                  "text": "В корзину",
                  "background": [
                    {
                      "type": "solid",
                      "color": "#42b077"
                    }
                  ],
                  "text_color": "#fff",
                  "corners": 4,
                  "type": "_template_button",
                  "width": {
                    "type": "match_parent"
                  },
                  "margins": {
                    "bottom": 10
                  },
                  "font_size": 20,
                  "paddings": {
                    "top": 10,
                    "right": 28,
                    "bottom": 10,
                    "left": 28
                  },
                  "text_alignment_horizontal": "center",
                  "border": {
                    "corner_radius": 15
                  }
                },
                {
                  "text": "Купить",
                  "background": [
                    {
                      "type": "solid",
                      "color": "#018a51"
                    }
                  ],
                  "text_color": "#fff",
                  "corners": 4,
                  "type": "_template_button",
                  "width": {
                    "type": "match_parent"
                  },
                  "font_size": 20,
                  "paddings": {
                    "top": 15,
                    "right": 28,
                    "bottom": 15,
                    "left": 28
                  },
                  "border": {
                    "corner_radius": 15
                  }
                }
              ],
              "border": {
                "corner_radius": 15
              },
              "paddings": {
                "right": 15,
                "left": 15,
                "top": 15,
                "bottom": 10
              },
              "alpha": 1,
              "background": [
                {
                  "type": "solid",
                  "color": "#f0fff0"
                }
              ]
            }
"""
"""
{
              "type": "container",
              "width": {
                "type": "match_parent"
              },
              "height": {
                "type": "match_parent"
              },
              "items": [
                {
                  "type": "container",
                  "width": {
                    "type": "match_parent"
                  },
                  "height": {
                    "type": "wrap_content"
                  },
                  "items": [
                    {
                      "type": "text",
                      "text": "Главная",
                      "width": {
                        "type": "wrap_content"
                      },
                      "text_color": "#f0fff0",
                      "font_size": 30,
                      "font_weight": "bold"
                    },
                    {
                      "type": "separator",
                      "width": {
                        "type": "match_parent"
                      },
                      "height": {
                        "type": "fixed",
                        "value": 10
                      },
                      "delimiter_style": {
                        "color": "#00000000"
                      }
                    },
                    {
                      "text": "Войти",
                      "background": [
                        {
                          "type": "solid",
                          "color": "#00159861"
                        }
                      ],
                      "text_color": "#fff",
                      "corners": 4,
                      "type": "_template_button",
                      "width": {
                        "type": "wrap_content",
                        "constrained": false
                      },
                      "paddings": {
                        "top": 1,
                        "right": 1,
                        "bottom": 1,
                        "left": 1
                      },
                      "height": {
                        "constrained": false,
                        "type": "wrap_content"
                      },
                      "alignment_vertical": "center",
                      "alignment_horizontal": "end",
                      "font_size": 15
                    }
                  ],
                  "accessibility": {
                    "type": "tab_bar"
                  },
                  "orientation": "horizontal",
                  "background": [
                    {
                      "type": "solid",
                      "color": "#018a51"
                    }
                  ],
                  "paddings": {
                    "top": 10,
                    "right": 10,
                    "bottom": 10,
                    "left": 10
                  },
                  "clip_to_bounds": true,
                  "content_alignment_horizontal": "start",
                  "content_alignment_vertical": "center"
                }
              ],
              "background": [
                {
                  "type": "solid",
                  "color": "#f0fff0"
                }
              ]
            }
"""
"""
{
  "card": {
    "log_id": "div2_sample_card",
    "states": [
      {
        "state_id": 0,
        "div": {
          "items": [
            {
              "type": "container",
              "width": {
                "type": "match_parent"
              },
              "height": {
                "type": "match_parent"
              },
              "items": [
                {
                  "type": "container",
                  "width": {
                    "type": "match_parent"
                  },
                  "height": {
                    "type": "wrap_content"
                  },
                  "items": [
                    {
                      "type": "text",
                      "text": "Главная",
                      "width": {
                        "type": "wrap_content"
                      },
                      "text_color": "#f0fff0",
                      "font_size": 30,
                      "font_weight": "bold"
                    },
                    {
                      "type": "separator",
                      "width": {
                        "type": "match_parent"
                      },
                      "height": {
                        "type": "fixed",
                        "value": 10
                      },
                      "delimiter_style": {
                        "color": "#00000000"
                      }
                    },
                    {
                      "text": "Войти",
                      "background": [
                        {
                          "type": "solid",
                          "color": "#00159861"
                        }
                      ],
                      "text_color": "#fff",
                      "corners": 4,
                      "type": "_template_button",
                      "width": {
                        "type": "wrap_content",
                        "constrained": false
                      },
                      "paddings": {
                        "top": 1,
                        "right": 1,
                        "bottom": 1,
                        "left": 1
                      },
                      "height": {
                        "constrained": false,
                        "type": "wrap_content"
                      },
                      "alignment_vertical": "center",
                      "alignment_horizontal": "end",
                      "font_size": 15
                    }
                  ],
                  "accessibility": {
                    "type": "tab_bar"
                  },
                  "orientation": "horizontal",
                  "background": [
                    {
                      "type": "solid",
                      "color": "#018a51"
                    }
                  ],
                  "paddings": {
                    "top": 10,
                    "right": 10,
                    "bottom": 10,
                    "left": 10
                  },
                  "clip_to_bounds": true,
                  "content_alignment_horizontal": "start",
                  "content_alignment_vertical": "center"
                },
                {
                  "type": "grid",
                  "column_count": 2,
                  "width": {
                    "type": "match_parent"
                  },
                  "items": [
                    {
                      "type": "image",
                      "image_url": "empty://",
                      "width": {
                        "type": "fixed",
                        "value": 100
                      },
                      "height": {
                        "type": "fixed",
                        "value": 100
                      },
                      "preload_required": true
                    }
                  ],
                  "paddings": {
                    "left": 10,
                    "right": 10
                  },
                  "row_span": 2,
                  "column_span": 2,
                  "margins": {
                    "top": 10,
                    "bottom": 10
                  }
                }
              ],
              "background": [
                {
                  "type": "solid",
                  "color": "#f0fff0"
                }
              ]
            }
          ],
          "background": [
            {
              "color": "#000000",
              "type": "solid"
            }
          ],
          "height": {
            "type": "match_parent"
          },
          "orientation": "vertical",
          "type": "container",
          "content_alignment_vertical": "top",
          "content_alignment_horizontal": "center"
        }
      }
    ]
  },
  "templates": {
    "_template_close": {
      "accessibility": {
        "description": "Закрыть",
        "mode": "merge",
        "type": "button"
      },
      "actions": [
        {
          "log_id": "close_popup",
          "url": "div-screen://close"
        }
      ],
      "image_url": "https://yastatic.net/s3/home/div/div_fullscreens/cross2.3.png",
      "tint_color": "#73000000",
      "type": "image"
    },
    "_template_button": {
      "type": "text",
      "text_alignment_horizontal": "center",
      "text_alignment_vertical": "center",
      "border": {
        "$corner_radius": "corners"
      },
      "paddings": {
        "bottom": 24,
        "left": 28,
        "right": 28,
        "top": 22
      },
      "width": {
        "type": "wrap_content"
      }
    }
  }
}
"""