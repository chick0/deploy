from fastapi import APIRouter
from fastapi import Depends
from fastapi import UploadFile

from v1.const import deploy
from v1.models.upload import UploadResult

router = APIRouter(
    tags=["Upload"]
)


@router.post(
    "/upload/:uuid",
    description="배포할 파일을 압축 파일로 업로드 합니다.",
    response_model=UploadResult
)
async def upload_and_deploy(uuid: str, file: UploadFile, token=Depends(deploy)):
    """
    Upload deploy file then deploy system will unzip to deploy folder

    :param uuid: project uuid
    :param file: file to deploy
    :param token:
    :return: upload request result
    """
    return {}
