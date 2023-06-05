import boto3
from django.conf import settings
def vendor_files(request):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    bucket_name = 'ai-gallery'
    vendor_dir = 'static/vendor'  # S3 버킷 내 정적 파일 디렉토리 경로

    js_files = []
    css_files = []

    # JavaScript 파일 목록 가져오기
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=f'{vendor_dir}/', Delimiter='/')
    for obj in response.get('Contents', []):
        if obj['Key'].endswith('.js'):
            js_files.append(obj['Key'])

    # CSS 파일 목록 가져오기
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=f'{vendor_dir}/', Delimiter='/')
    for obj in response.get('Contents', []):
        if obj['Key'].endswith('.css'):
            css_files.append(obj['Key'])

    return {
        "vendor_js_files": js_files,
        "vendor_css_files": css_files,
    }
