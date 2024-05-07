from datetime import timedelta
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.config import settings
from app.users.auth import authenticate_user, create_jwt
from app.users.dependencies import get_current_user_by_token, get_payload
from app.users.models import Users


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        user: Users  = await authenticate_user(username, password)
        if user and user.is_admin:
            data = {"sub": str(user.id)}
            access_token = create_jwt(token_type="access", token_data=data)
            refresh_token = create_jwt(
                token_type="refresh",
                token_data=data,
                expire_timedelta=timedelta(days=settings.JWT_TOKEN.refresh_token_expire_days))
            request.session.update({"access_token": access_token, "refresh_token": refresh_token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request):
        access_token = request.session.get("access_token")
        refresh_token = request.session.get("refresh_token")

        if not access_token or not refresh_token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        access_payload = get_payload(access_token)
        user_id = access_payload.get("sub")

        user = await get_current_user_by_token(access_payload)
        if user:
            return True

        refresh_payload = get_payload(refresh_token)
        if user_id == refresh_payload.get("sub"):
            new_access_token = create_jwt(token_type="access", token_data={"sub": str(user_id)})
            request.session.update({"access_token": new_access_token})
            return True

        return RedirectResponse(request.url_for("admin:login"), status_code=302)


authentication_backend = AdminAuth(secret_key="...")
