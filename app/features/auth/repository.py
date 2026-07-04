from app.shared.dbmodels import User


class AuthReposotory:
    async def get_user(self, login: str) -> User | None:
        user = await User.find_one(User.login == login)
        return user


auth_repo = AuthReposotory()
