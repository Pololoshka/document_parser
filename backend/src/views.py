from fastapi import APIRouter, Depends, HTTPException, UploadFile
from pydantic import BaseModel, field_validator

from src.db.db_connect import uow
from src.db.uow import SqlAlchemyUnitOfWork
from src.handler import CalculateTFIDFHandler
from src.models_pydantic import FileContent, WordScore

router = APIRouter(prefix="/api/documents")


class Request(BaseModel):
    file: UploadFile

    @field_validator("file")
    @classmethod
    def file_must_be_txt(cls, file: UploadFile) -> UploadFile:
        if not file.filename or not file.filename.endswith(".txt"):
            raise HTTPException(status_code=422, detail="The file must have the extension .txt")
        if file.content_type != "text/plain":
            raise HTTPException(status_code=422, detail="MIME type must be: text/plain")
        return file

    @field_validator("file")
    @classmethod
    def file_must_be_small(cls, file: UploadFile) -> UploadFile:
        if not file.size or file.size > 10e5:
            raise HTTPException(
                status_code=422, detail="The file must be no larger than 1 MB in size"
            )
        return file

    async def get_content(self) -> None | FileContent:
        content = await self.file.read()
        try:
            return FileContent.from_content(content)
        except UnicodeDecodeError:
            return None


@router.post("/")
async def add_document(
    request: Request = Depends(),
    uow: SqlAlchemyUnitOfWork = Depends(uow),
) -> list[WordScore]:
    content = await request.get_content()
    if not content:
        raise HTTPException(status_code=422, detail="The file encoding must be UTF-8")

    handler = CalculateTFIDFHandler(uow=uow)
    return await handler.execute(content=content)
