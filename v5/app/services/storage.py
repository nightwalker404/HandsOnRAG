import uuid
from pathlib import Path
from app.core import get_settings

def save_uploaded_file(file_bytes: bytes, original_filename: str) -> Path:
    """ Persist an uploaded file to disk and return its saved path. """
    settings = get_settings()
    settings.doc_dir.mkdir(parents=True, exist_ok=True) # create the folder if it's not exist

    ext = Path(original_filename).suffix
    stored_name = f"{uuid.uuid4()}{ext}"
    dest_path = settings.doc_dir / stored_name

    dest_path.write_bytes(file_bytes)
    return dest_path
