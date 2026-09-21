import boto3
from botocore.client import Config
from app.core import get_settings
from pathlib import Path

settings = get_settings()

class StorageService:
    def __init__(self) -> None:
        self.s3 = boto3.client(
            "s3",
            endpoint_url=settings.garage_endpoint,
            aws_access_key_id=settings.garage_access_key,
            aws_secret_access_key=settings.garage_secret_key,
            region_name=settings.garage_region,
            config=Config(signature_version="s3v4"),
        )
        self.bucket = settings.garage_bucket

    def upload_file(self, local_path: Path, object_key: str) -> str:
        """ Upload a file to Garage and return the object key """
        self.s3.upload_file(
            str(local_path),
            self.bucket,
            object_key
        )
        return object_key

    def download_file(self, object_key: str, local_path: Path):
        """ Download a file from Garage """
        self.s3.download_file(
            self.bucket,
            object_key,
            str(local_path)
        )
