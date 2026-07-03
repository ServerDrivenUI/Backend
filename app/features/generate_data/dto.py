from dataclasses import dataclass


@dataclass
class UserDTO:
    login: str
    password_hash: str
    is_impulsive: bool


@dataclass
class ClothesItemDTO:
    price: int
    name: str
    descripton: str
