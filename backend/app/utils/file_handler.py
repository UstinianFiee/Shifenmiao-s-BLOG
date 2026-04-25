import os
import uuid
from flask import current_app

ALLOWED_IMAGE = {"png", "jpg", "jpeg", "gif", "webp", "svg"}
ALLOWED_VIDEO = {"mp4", "webm", "ogg", "mov"}
ALLOWED_AUDIO = {"mp3", "wav", "flac", "aac", "m4a"}
ALLOWED_ALL = ALLOWED_IMAGE | ALLOWED_VIDEO | ALLOWED_AUDIO

def get_ext(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

def get_file_type(ext: str) -> str:
    if ext in ALLOWED_VIDEO:
        return "video"
    if ext in ALLOWED_AUDIO:
        return "audio"
    return "image"

def save_upload(file, allowed: set = None) -> dict:
    """
    保存上传文件，返回 {"url": "/uploads/xxx.ext", "type": "image|video|audio", "name": "原始文件名"}
    失败时抛出 ValueError
    """
    if allowed is None:
        allowed = ALLOWED_ALL
    ext = get_ext(file.filename)
    if not ext or ext not in allowed:
        raise ValueError(f"不支持的文件类型 .{ext}")
    name = f"{uuid.uuid4().hex}.{ext}"
    folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(folder, exist_ok=True)
    file.save(os.path.join(folder, name))
    return {
        "url": f"/uploads/{name}",
        "type": get_file_type(ext),
        "name": file.filename,
    }
