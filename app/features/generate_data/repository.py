from app.shared.dbmodels import User, ClothesItem
from .dto import UserDTO, ClothesItemDTO
from app.shared.extensions import db


class GenearateRepository:
    async def add_user(self, user_dto: UserDTO):
        """Добавление нового пользователя в MongoDB"""
        try:
            new_user = User(
                login=user_dto.login,
                is_impulsive=user_dto.is_impulsive,
                password_hash=user_dto.password_hash,
            )
            await new_user.insert()
        except Exception as e:
            raise Exception(str(e))

    async def add_clothes_item(self, clothes_item_dto: ClothesItemDTO):
        """Добавление нового предмета одежды в MongoDB"""
        try:
            new_clothes_item = ClothesItem(
                descripton=clothes_item_dto.descripton,
                name=clothes_item_dto.name,
                price=clothes_item_dto.price,
            )
            await new_clothes_item.insert()
        except Exception as e:
            raise Exception(e)


generate_repo = GenearateRepository()
