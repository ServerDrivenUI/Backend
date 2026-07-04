from abc import ABC, abstractmethod


class BaseCreator(ABC):
    page_type: str = ""

    @abstractmethod
    async def get_page(self):
        pass


class MainCreator(BaseCreator):
    page_type: str = "main_market_page"

    async def get_page(self):
        print("self")


creators = [MainCreator()]
