from core.env import config
from django.conf import settings

AWS_ACCESS_KEY_ID=config("AWS_ACCESS_KEY_ID", default=None)
AWS_SECRET_ACCESS_KEY=config("AWS_SECRET_ACCESS_KEY", default=None)
AWS_S3_SIGNATURE_VERSION="s3v4"

AWS_STORAGE_BUCKET_NAME="ai-gallery"
AWS_STORAGE_BUCKET_REGION="ap-northeast-2"

AWS_DEFAULT_ACL="public-read"
AWS_S3_USE_SSL=True

DEFAULT_FILE_STORAGE = 'core.storages.backends.MediaStorage'
STATICFILES_STORAGE = 'core.storages.backends.StaticFileStorage'