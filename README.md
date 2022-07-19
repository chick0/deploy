# deploy

귀찮은 일을 대신해주는 deploy API

## 배포 방법

1. upload
    - push이후 빌드된 파일을 압축해서 API로 업로드하면 API가 압축 풀고 적용
2. pull
    - push이후 API로 신호가 오면 API가 `git pull` 명령을 실행 한 다음 서버 재시작

두 방법 모두 별도의 [deploy-cli](#)를 사용합니다.

## 사용자 관리

사용자를 추가하려면 `useradd.py`를 사용해야 합니다.

사용자를 삭제하려면 `userdel.py`를 사용해야 합니다.

배포 할 때는 로그인 할 때 사용하는 인증 토큰이 아닌 별도의 배포 토큰이 있습니다.

## 토큰 관리

배포 토큰은 [웹 클라이언트](https://github.com/chick0/deploy-client)를 통해 관리 할 수 있습니다.

## 서버 설정

1. 의존성 설치
    - `pip install -r requirements.txt`를 사용해도 되지만 [pip-tools](https://github.com/jazzband/pip-tools)의 `pip-sync`를 사용해도 됩니다.
2. 서버 설정
    - `.env.example` 파일을 `.env` 파일로 복사합니다.
    - 그 다음 `SQLALCHEMY_DATABASE_URI`에는 본인의 데이터베이스 접속 관련 정보를 입력해주세요.
    - 그 다음 `ISS`는 토큰의 발급자(issuer)로 API 서버가 사용 할 도메인 주소를 입력해주세요.
3. 데이터베이스 모델 적용
    - `alembic upgrade c78545df2f8e`
    - 위 명령어를 통해 적용 할 수 있습니다.
