import logging
from app.shared.page_builder import page_builder
from app.shared.consts import SDUI_TEMPLATES


class PagesService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def get_page(self, page_type: str):
        """Выбирает нужную страницу по ее типу из БД"""
        if page_type == "main_market_page":
            try:
                page_with_data, values = await page_builder.build_page(page_type)

                final_response = {
                    "card": {
                        "log_id": f"screen_{page_type}",
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
