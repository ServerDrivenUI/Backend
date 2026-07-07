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
