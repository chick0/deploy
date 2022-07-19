from sys import argv
from os import environ
from os.path import join

from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware

try:
    ENCODING = "utf-8"

    with open(join(".git", "HEAD"), mode="r", encoding=ENCODING) as head_reader:
        head = head_reader.read()[5:].strip()

    with open(join(".git", head), mode="r", encoding=ENCODING) as hash_reader:
        VERSION = hash_reader.read()[:7]
except FileNotFoundError:
    VERSION = "*MISSING HEAD*"

app = FastAPI(
    title="Deploy API",
    description="배포를 도와주는 API 서버",
    version=VERSION,
    openapi_url="/openapi.json" if '--dev' in argv else None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[environ['CORS_ORIGIN'].strip()],
    allow_methods=[
        "GET",
        "PATCH",
        "POST",
        "DELETE"
    ],
    allow_headers=[
        "Authorization"
    ]
)

api = APIRouter(prefix="/api")
api_versions = [
    "v1",
]

for v in [__import__(x) for x in api_versions]:
    router: APIRouter = getattr(v, "init")()
    if not router.deprecated:
        api.include_router(router=router)

app.include_router(router=api)
