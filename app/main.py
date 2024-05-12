import time
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.rooms.router import router as router_rooms
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.importer.router import router as router_importer
from app.logger import logger
from app.pages.router import router as router_pages
from app.prometheus.router import router as router_prometheus
from app.users.router import router_auth as router_auth
from app.users.router import router_user as router_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(
    title="Бронирование Отелей",
    root_path="/api"
)

for router in [
    router_auth,
    router_users,
    router_bookings,
    router_hotels,
    router_rooms,
    router_pages,
    router_images,
    router_importer,
    router_prometheus,
]:
    app.include_router(router)

origins = settings.ORIGINS.split(";")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

app = VersionedFastAPI(app, version_format="{major}", prefix_format="/v{major}", lifespan=lifespan)

if settings.MODE == "TEST":
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")

instrumentator = Instrumentator(should_group_status_codes=False, excluded_handlers=[".*admin.*", "/metrics"])
instrumentator.instrument(app).expose(app)


if settings.MODE != "TEST":
    sentry_sdk.init(
        dsn=settings.SENTRY_DNS,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

admin = Admin(app, engine, authentication_backend=authentication_backend)

for admin_view in [UsersAdmin, BookingsAdmin, HotelsAdmin, RoomsAdmin]:
    admin.add_view(admin_view)

app.mount("/static", StaticFiles(directory="app/static"), "static")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={"process_time": round(process_time, 4)})
    return response
