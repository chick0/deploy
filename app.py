from sys import argv
from os.path import join

from fastapi import FastAPI

try:
    version = open(join(".git", open(join(".git", "HEAD"), mode="r").read()[5:].strip()), mode="r").read()[:7]
except (FileNotFoundError, Exception):
    version = "*MISSING HEAD*"

app = FastAPI(
    title="Deploy API",
    description="배포를 도와주는 API 서버",
    version=version,
    openapi_url="/openapi.json" if '--dev' in argv else None
)
