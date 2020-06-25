import sentry_sdk
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from core import settings
from core.server.application import MIDDLEWARES, MOUNTS
from core.server.db import db
from core.routes import apps
from core.settings import settings
from core.service import service_route

_app = None


def get_app():
    global _app
    if not _app:
        _app = FastAPI(
            **settings.AppSettings().dict(),
            middleware=MIDDLEWARES
        )

        _app.include_router(service_route)
        _app.include_router(apps)

        if settings.SENTRY_DSN:
            sentry_sdk.init(dsn=settings.SENTRY_DSN)
            _app.add_middleware(SentryAsgiMiddleware)
        for _mount in MOUNTS:
            _app.mount(*_mount)
        db.init_app(_app)
    return _app
