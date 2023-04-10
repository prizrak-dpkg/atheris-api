# Python imports
from enum import Enum
import hashlib
import os
import re
import shutil
import tempfile

# Starlette imports
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_410_GONE,
    HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

# FastAPI imports
from fastapi import UploadFile
from fastapi.exceptions import HTTPException

# Own imports
from config.base_settings import get_settings
from ..models.file import FileModel
from ..schemas.file import FileSchema


class FileUploadDirectoryEnum(Enum):
    SLIDES = ["uploads", "slides"]


class Files:
    def __init__(self, file: UploadFile, dir: FileUploadDirectoryEnum):
        self.__file = file
        self.__dir = [*dir.value]

    @property
    def _validate_file_size(self) -> UploadFile:
        max_size = get_settings().DATA_UPLOAD_MAX_MEMORY_SIZE
        if self.__file.size > max_size:
            raise HTTPException(
                status_code=HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=[
                    {
                        "field": "generalScope",
                        "msg": f"El archivo excede el tamaño máximo permitido de {max_size} bytes.",
                    },
                ],
            )
        return self.__file

    @property
    def _validate_file_mimetype(self) -> UploadFile:
        if (
            not self.__file.content_type
            or not self.__file.content_type in get_settings().ALLOWED_MIME_TYPES
        ):
            raise HTTPException(
                status_code=HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=[
                    {
                        "field": "generalScope",
                        "msg": f"El tipo de archivo no está en la lista de tipos MIME permitidos.",
                    },
                ],
            )
        return self.__file

    @property
    async def _write_file_async(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = f"{temp_dir}/{self.__file.filename}"
            sha256_hash = hashlib.sha256()
            with open(file_path, "wb") as buffer:
                for block in iter(lambda: self.__file.file.read(4096), b""):
                    sha256_hash.update(block)
                    buffer.write(block)
            md5_hash = hashlib.md5(f"{sha256_hash.hexdigest()}".encode())
            upload_dir = os.path.join(os.getcwd(), *self.__dir)
            os.makedirs(upload_dir, exist_ok=True)
            name, ext = os.path.splitext(self.__file.filename)
            name = hashlib.md5(
                f"{sha256_hash.hexdigest()}{md5_hash.hexdigest()}".encode()
            ).hexdigest()
            if await self._get_file_by_md5_async(md5=md5_hash.hexdigest()):
                raise HTTPException(
                    status_code=HTTP_409_CONFLICT,
                    detail=[
                        {
                            "field": "generalScope",
                            "msg": f"El archivo ya ha sido cargado anteriormente en el servidor.",
                        },
                    ],
                )
            with open(f"{upload_dir}/{name}{ext}", "wb") as buffer:
                with open(file_path, "rb") as temp_buffer:
                    shutil.copyfileobj(temp_buffer, buffer)
        return (sha256_hash.hexdigest(), md5_hash.hexdigest(), f"{ext}")

    @property
    async def save_async(self):
        self._validate_file_size
        self._validate_file_mimetype
        sha256, md5, ext = await self._write_file_async
        return await self._get_md5_async(
            buffer=FileSchema(sha256=sha256, md5=md5, ext=ext)
        )

    @property
    async def create_async(self):
        sha256, md5, ext = await self._write_file_async
        file = FileModel(sha256=sha256, md5=md5, ext=ext)
        return await FileModel.insert_one(file)

    async def _get_file_by_md5_async(self, md5: str):
        regex_pattern = f"^{re.escape(md5)}$"
        return await FileModel.find(
            {"md5": {"$regex": regex_pattern, "$options": "i"}}
        ).first_or_none()

    async def _get_file_by_sha256_async(self, sha256: str):
        regex_pattern = f"^{re.escape(sha256)}$"
        return await FileModel.find(
            {"sha256": {"$regex": regex_pattern, "$options": "i"}}
        ).first_or_none()

    async def _get_md5_async(self, buffer: FileSchema):
        file = FileModel(sha256=buffer.sha256, md5=buffer.md5, ext=buffer.ext)
        await FileModel.insert_one(file)
        return file.md5

    def _validate_file(self, file: FileModel, dir: FileUploadDirectoryEnum):
        search_path = os.path.join(os.getcwd(), *dir.value)
        file_path = "{}{}".format(
            hashlib.md5(f"{file.sha256}{file.md5}".encode()).hexdigest(), file.ext
        )
        path = os.path.join(search_path, file_path)
        if os.path.exists(path=path):
            if self.get_sha256(path=path) == file.sha256:
                return path
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail=[
                    {
                        "field": "generalScope",
                        "msg": "El recurso especificado se ha corrompido.",
                    },
                ],
            )
        raise HTTPException(
            status_code=HTTP_410_GONE,
            detail=[
                {
                    "field": "generalScope",
                    "msg": "El recurso especificado ya no está disponible.",
                },
            ],
        )

    @classmethod
    async def get_file_async(cls, hash: str, md5: bool = True):
        if md5:
            return await cls._get_file_by_md5_async(self=cls, md5=hash)
        else:
            return await cls._get_file_by_sha256_async(self=cls, sha256=hash)

    @classmethod
    async def get_path_file_async(
        cls, hash: str, dir: FileUploadDirectoryEnum, md5: bool = True
    ):
        file = await cls.get_file_async(hash=hash, md5=md5)
        if file:
            return cls._validate_file(self=cls, file=file, dir=dir)
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=[
                {
                    "field": "generalScope",
                    "msg": "El recurso especificado no existe.",
                },
            ],
        )

    @classmethod
    async def get_path_terms_async(cls, hash: str):
        terms = await cls._get_terms_by_md5_async(self=cls, md5=hash)
        if terms:
            return await cls._validate_terms_async(self=cls, terms=terms)
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=[
                {
                    "field": "generalScope",
                    "msg": "El recurso especificado no existe.",
                },
            ],
        )

    @staticmethod
    def get_sha256(path: str):
        with open(path, "rb") as buffer:
            sha256_hash = hashlib.sha256()
            for block in iter(lambda: buffer.read(4096), b""):
                sha256_hash.update(block)
        return sha256_hash.hexdigest()
