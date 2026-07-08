from .base_creator import BaseCreator
from typing import Dict, Type

CREATORS_DICT: Dict[str, BaseCreator] = {}


def register_creator(creator_class: Type[BaseCreator]):
    """Декоратор для регистрации креаторов"""
    instance = creator_class()
    CREATORS_DICT[creator_class.item_type] = instance
    return creator_class
