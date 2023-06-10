import boto3
from botocore.client import Config
from django.conf import settings

def generate_presigned_url(filepath, location = "protected"):
    object_storage_key = f"{location}/{filepath}"
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(addressing_style=settings.AWS_S3_ADDRESSING_STYLE)
    )
    url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params = {
            "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
            "Key": object_storage_key,
            "ResponseContentDisposition": "attachment"
        },
        # ExpiresIn=3600, # URL ends in 1 hour
    )
    return url