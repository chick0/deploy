__all__ = [
    "auth",
    "project",
    "projects",
    "token",
    "pull",
    "upload",
]

from fastapi import APIRouter


def init():
    router = APIRouter(prefix="/v1")
    for r in [getattr(__import__(f"{__name__}.{x}"), x).router for x in __all__]:
        if not r.deprecated:
            router.include_router(router=r)

    return router
