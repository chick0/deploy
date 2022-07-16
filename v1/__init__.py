__all__ = [
    "auth",
    "project",
    "projects",
    "token",
    "pull",
    "upload",
]

from . import *
from fastapi import APIRouter


def init():
    router = APIRouter(prefix="/v1")
    for r in [getattr(__import__(__name__), x).router for x in __all__]:
        if not r.deprecated:
            router.include_router(router=r)

    return router
