# FastAPI imports
from fastapi import File, UploadFile
from fastapi.responses import FileResponse

# Own imports
from ..utils.file import FileUploadDirectoryEnum, Files


class FileRequest:
    async def read_slide_async(self, hash: str):
        path = await Files.get_path_file_async(
            hash=hash, dir=FileUploadDirectoryEnum.SLIDES
        )
        return FileResponse(path)

    async def upload_slide_async(self, file: UploadFile = File(...)):
        files = Files(file=file, dir=FileUploadDirectoryEnum.SLIDES)
        file = await files.save_async
        return {
            "upload_dir": file,
        }
