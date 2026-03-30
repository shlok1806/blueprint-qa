import os
import shutil
from pathlib import Path
from fastapi import UploadFile
from backend.config import get_settings

settings = get_settings()


class LocalStorage:
    def __init__(self):
        self.upload_dir = Path(settings.upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save(self, file: UploadFile, filename: str) -> str:
        dest = self.upload_dir / filename
        with open(dest, "wb") as f:
            shutil.copyfileobj(file.file, f)
        return str(dest)

    def get_path(self, file_path: str) -> str:
        return file_path

    def delete(self, file_path: str) -> None:
        path = Path(file_path)
        if path.exists():
            path.unlink()

    def exists(self, file_path: str) -> bool:
        return Path(file_path).exists()
