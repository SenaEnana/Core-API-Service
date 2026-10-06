import shutil
from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.models import UserModel
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/uploads",
    tags=["Uploads"],
)

