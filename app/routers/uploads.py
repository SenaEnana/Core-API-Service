import shutil
from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.models import UserModel
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/uploads",
    tags=["Uploads"],
)

UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/file")
def upload_file(
    file: UploadFile = File(...),
    current_user: UserModel = Depends(get_current_user),
):
   