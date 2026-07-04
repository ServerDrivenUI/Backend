import logging
from .repository import pages_repo
import json
from app.shared.page_builder import page_builder
from pydivkit import DivData
from pydivkit.div import Div
from app.shared.consts import SDUI_TEMPLATES


class PagesService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def get_page(self, type: str):
        """Выбирает нужную страницу по ее типу из БД"""
        page = await pages_repo.get_page_by_type(type)
        if not page:
            self.logger.error(f"Страница с типом '{type}' не найдена в базе данных")
            return None

        page_json = json.loads(page.json_dict)

        if type == "main_market_page":
            try:
                page_with_data, values = await page_builder.build_main_market_page(
                    page_json
                )

                final_response = {
                    "card": {
                        "log_id": f"screen_{type}",
                        "states": [{"state_id": 0, "div": page_with_data}],
                        "variables": values,
                    },
                    "templates": SDUI_TEMPLATES,
                }

                return final_response
            except Exception as e:
                self.logger.error(e)
                return None


pages_service = PagesService()
