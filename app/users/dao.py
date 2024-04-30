from app.dao.base import SQLAlchemyDAO
from app.users.models import Users


class UserDAO(SQLAlchemyDAO):
    model = Users
