from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
import os
import shutil

router = APIRouter()

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Generate a unique filename
        ext = file.filename.split('.')[-1] if '.' in file.filename else 'bin'
        filename = f"{uuid.uuid4()}.{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Return the relative URL path
        return {"url": f"/static/uploads/{filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not upload file: {str(e)}")
