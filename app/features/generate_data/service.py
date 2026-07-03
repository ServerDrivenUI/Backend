from .dto import UserDTO, ClothesItemDTO
from faker import Faker
from .repository import generate_repo
import logging
import faker_commerce
import random


class GenerateService:
    def __init__(self):
        self.faker = Faker()
        self.faker.add_provider(faker_commerce.Provider)
        self.logger = logging.getLogger(__name__)

    async def generate_users(self, count: int):
        """Генерирует пользователей"""
        for i in range(count):
            user_dto = UserDTO(
                login=self.faker.email(),
                password_hash=self._generate_password_hash(self.faker.password()),
                is_impulsive=True,
            )
            try:
                await generate_repo.add_user(user_dto)
            except Exception as e:
                self.logger.error(f"Ошибка при добавлении пользователя: {str(e)}")
        self.logger.debug("Пользователи добавлены")

    def _generate_password_hash(self, password: str) -> bytes:
        """Генерирует hash паролей"""
        # TODO: добавить генерацию хешей
        return password

    async def generate_clothes(self, count: int):
        """Генерирует вещи в каталоге"""
        for i in range(count):
            words_count = random.randint(5, 10)
            clothes_item_dto = ClothesItemDTO(
                price=self.faker.pyint(min_value=100, max_value=10000),
                name=self.faker.ecommerce_name(),
                descripton=self.faker.sentence(words_count),
            )
            try:
                await generate_repo.add_clothes_item(clothes_item_dto)
            except Exception as e:
                self.logger.error(f"ошибка создания одежды: {str(e)}")
        self.logger.debug("Одежда добавлена")


genearate_service = GenerateService()
