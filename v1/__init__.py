__all__ = [
    "auth",
    "project",
    "projects",
    "token",
    "pull",
    "upload",
]

from fastapi import APIRouter


def init() -> APIRouter:
    """
    Get v1 api router

    :return: v1
    """
    router = APIRouter(prefix="/v1")
    for _router in [getattr(__import__(f"{__name__}.{x}"), x).router for x in __all__]:
        if not _router.deprecated:
            router.include_router(router=_router)

    return router
