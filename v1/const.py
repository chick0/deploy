from fastapi.security import HTTPBearer

auth = HTTPBearer(
    scheme_name="Auth Token",
    description="사용자 인증 토큰"
)

deploy = HTTPBearer(
    scheme_name="Deploy Token",
    description="배포 토큰"
)

any_ = HTTPBearer(
    scheme_name="Auth or Deploy Token",
    description="사용자 인증 토큰 또는 배포 토큰"
)
