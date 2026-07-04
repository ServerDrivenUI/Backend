from app.shared.dbmodels import Page


class PagesRepository:
    async def get_page_by_type(self, type: str) -> Page | None:
        page = await Page.find_one(Page.type == type)
        return page


pages_repo = PagesRepository()
