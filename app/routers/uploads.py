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
    """Upload a file associated with the authenticated user."""
    allowed_extensions = {".jpg", ".jpeg", ".png", ".pdf"}
    file_ext = Path(file.filename).suffix.lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File extension '{file_ext}' not allowed. Allowed: {allowed_extensions}",
        )

   