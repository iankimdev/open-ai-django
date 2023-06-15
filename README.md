이스트소프트의 백엔드 부트캠프에 참여하며 AI에 관심을 가지고 만든 `chatGPT`와 `DALLE`를 활용한 AI 이미지 주문/제작 이커머스입니다.

## 배포 URL
http://3.39.15.18:8002
```
<testuser>
username : public
password : password123
```
  
## 목표
자신이 원하는 이미지를 AI로 주문 제작하여 미술품으로 집으로 배송받을 수 있는 서비스

## 기능

- OpenAI의 DALLE 엔진을 사용하여 이미지를 AI로 제작
- OpenAI의 ChatGPT 엔진을 사용하여 chatbot을 사용하여 고객상담 관리


## 개발/서비스 배포 환경 

python 3.10.6<br>
Node.js 18.16.0<br>
tailwindcss@3.2.7<br>
django 4.1.8<br>
djangorestframework 3.14.0<br>
stripe 5.4.0<br>
openai 0.27.7<br>
gunicorn 20.1.0 <br>
nginx 1.19.0-alpine<br>
boto3 1.26.137 <br>
Docker <br>
AWS EC2/S3/RDS <br>

## 프로젝트 구조
<details>
<summary>트리</summary>

<!-- summary 아래 한칸 공백 두어야함 -->

```
├── django
│   ├── chatbot
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── config
│   │   └── entrypoint.sh
│   ├── core
│   │   ├── asgi.py
│   │   ├── context_processors.py
│   │   ├── db.py
│   │   ├── env.py
│   │   ├── settings.py
│   │   ├── storages
│   │   │   ├── backends.py
│   │   │   ├── conf.py
│   │   │   └── utils.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── wsgi.py
│   ├── dalle
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── manage.py
│   ├── products
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   └── views.py
│   ├── purchases
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── requirements
│   │   └── requirements.in
│   ├── requirements.txt
│   ├── static
│   │   ├── css
│   │   │   └── output.css
│   │   ├── tailwind
│   │   │   └── tailwind-input.css
│   │   └── vendor
│   │       ├── flowbite
│   │       └── htmx
│   │           └── htmx.min.js
│   ├── templates
│   │   ├── admin
│   │   │   └── change_form.html
│   │   ├── base
│   │   │   ├── css.html
│   │   │   ├── footer.html
│   │   │   ├── js.html
│   │   │   └── navbar.html
│   │   ├── base.html
│   │   ├── contact.html
│   │   ├── custom
│   │   │   └── custom-dalle.html
│   │   ├── home.html
│   │   ├── products
│   │   │   ├── attachments-table.html
│   │   │   ├── create.html
│   │   │   ├── delete.html
│   │   │   ├── detail.html
│   │   │   ├── list-card.html
│   │   │   ├── list.html
│   │   │   └── manager.html
│   │   ├── purchases
│   │   │   ├── buy-btn-form.html
│   │   │   ├── list.html
│   │   │   └── my-order.html
│   │   └── users
│   │       ├── delete.html
│   │       ├── password-change.html
│   │       ├── profile.html
│   │       ├── signin.html
│   │       └── signup.html
│   └── users
│       ├── admin.py
│       ├── apps.py
│       ├── migrations
│       ├── forms.py
│       ├── migrations
│       ├── models.py
│       ├── serializers.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── docker-compose.yml
├── Dockerfile
├── nginx
│   ├── Dockerfile
│   └── default.conf
├── package-lock.json
├── package.json
├── rav.yaml
├── tailwind.config.js
└── venv
```
</details>




## UI / BM
<details>
<summary>User Interface</summary>

<!-- summary 아래 한칸 공백 두어야함 -->
### Home
![](https://velog.velcdn.com/images/iankimdev/post/fdd29ab4-4579-405a-93c0-69816bb032c5/image.png)
### 회원가입
![](https://velog.velcdn.com/images/iankimdev/post/e08cbe7f-643e-4ec1-b301-90d646a7187e/image.png)
### 로그인
![](https://velog.velcdn.com/images/iankimdev/post/aebae044-1ae1-4807-8bd6-2ba3db0efa0c/image.png)
### 주문
![](https://velog.velcdn.com/images/iankimdev/post/5cf64947-c69f-4290-bdd3-b73ef2cb25d5/image.png)
![](https://velog.velcdn.com/images/iankimdev/post/751744b0-2b48-4342-98e9-4177e8896351/image.png)
### 결제
![](https://velog.velcdn.com/images/iankimdev/post/6b41895f-8e6d-4489-ba6c-4ddb81289c32/image.png)
### 결제완료 및 주문내역 확인
![](https://velog.velcdn.com/images/iankimdev/post/ea6ef01f-fb39-4246-9f8d-a8426cc1ed5d/image.png)
![](https://velog.velcdn.com/images/iankimdev/post/3cfe41d0-67e6-45e9-a041-e4c716eff7e8/image.png)
### 모든 주문 목록 확인(매니저 권한)
![](https://velog.velcdn.com/images/iankimdev/post/7d2df4be-473c-4422-8d2f-ec56ea7a541c/image.png)
### 갤러리 (유저들이 주문제작한 이미지들)
![](https://velog.velcdn.com/images/iankimdev/post/91f50d68-e4ca-4315-8498-c75e0308e445/image.png)
### 챗봇 고객센터
![](https://velog.velcdn.com/images/iankimdev/post/4b7d1395-ba09-4b3c-8164-fb986102c001/image.png)
</details>




## Initial settings

### 가상환경 및 패키지 관리
Pyenv로 가상환경 버전을 관리하였으며 프로젝트의 의존성 패키지를 명시적으로 정의하기 위해 requirements.txt를 생성하였다.
그 과정에서 rav.yaml이라는 관리 프로그램을 알게 되었고 이것을 이용하여 requirements.txt를 생성하고 여러 명령어들을 미리 셋팅해놓았다.


### static / media setting
초기에는 `htmx`와 `flowbite` 등 적용해보려고 했지만 `fetch`, `axios` 등으로 `AJAX`통신을 하였고 CSS는 `tailwind CSS`만 간단히 사용하였다.

<details>
<summary>Initial settings</summary>

<!-- summary 아래 한칸 공백 두어야함 -->

settings.py
```python
SECRET_KEY = config("DJANGO_SECRET_KEY", default=None)
from .db import * 

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "local-cdn" / "static"
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / "local-cdn" / "media"
```
urls.py
```python
urlpatterns = [
  ...
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

</details>



static파일과 media파일을 관리하기 위해 추가하였다.
이미지 관리를 위해 pillow 라이브러리를 사용하였다.


## APPS

`Django APP`으로는 `유저`, `DALLE`, `상품`, `결제`, `챗봇`을 사용하였다.

### DALLE 

`openai`의 `Image AI`를 사용하였다. `openai`에서 `secretkey`를 생성하고 `api`를 요청하면 `DALLE`를 사용할 수 있다.
유저가 입력하는 text인 `phrase`와 생성되는 이미지인 `ai_image`를 `DB 테이블`로 사용하였다.
<details>
<summary>views.py</summary>

<!-- summary 아래 한칸 공백 두어야함 -->
```python
@login_required
def generate_image(request):
    dalle = None
    error_message = None
    if api_key is not None and request.method == 'POST':
        user_input = request.POST.get("user_input")
        if user_input:
            try:
                response = openai.Image.create(
                    prompt=user_input,
                    size="512x512",
                )
                img_url = response["data"][0]["url"]
                img_response = requests.get(img_url)
                img_file = ContentFile(img_response.content)
                count = DalleImage.objects.count() + 1
                fname = f"image-{count}.jpg"

                dalle = DalleImage(phrase=user_input)
                dalle.ai_image.save(fname, img_file)
                dalle.save()
            except openai_error.InvalidRequestError as e:
                if str(e) == "Billing hard limit has been reached":
                    error_message = "OPEN AI's usage limit has been reached. Please contact support for assistance. 
                    return render(request, "custom/custom-dalle.html", {"error_message": error_message})
    return render(request, "custom/custom-dalle.html", {"product": dalle})
```
</details>




### Products (AI image)

달리 이미지를 생성 후 주문하면 `상품`으로 생성되게 구현하였다.<br>
달리가 이미지를 생성하면 이커머스 관리자가 다운로드 받아서 그것을 상품으로 올려 판매하는 것을 생각하고 Views.py를 만들었다. <br>
그러나 이런 방식이 비효율적이라고 생각했기 때문에 이 모듈은 더 이상 사용하지 않고 유저가 직접 원하는 이미지를 `커스텀`으로 만들어서 그것을 바로 주문하는 것으로 변경하였다.<br>
`handle`을 `uinque`로 두어서 `slug`로 사용했다.<br>
<details>
<summary>models.py</summary>

<!-- summary 아래 한칸 공백 두어야함 -->
```python
class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    name = models.CharField(max_length=200)
    handle = models.SlugField(unique=True, max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    og_price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    
    # STRIPE 결제
    stripe_product_id = models.CharField(max_length=220, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=220, blank=True, null=True)
    stripe_price = models.IntegerField(default=999) # 100 * price
    price_changed_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    
    (생략)
    
```
</details>

<details>
<summary>views.py</summary>

<!-- summary 아래 한칸 공백 두어야함 -->
```python
def products_list(request):
    products_list = Product.objects.all()
    
    for product in products_list:
        url = str(product.image)
        url_without_query = url.split('?')[0]
        product.image = url_without_query

    return render(request, 'products/list.html', {"products_list": products_list})

@login_required
@api_view(['POST'])
def products_create(request):
    if request.method == 'POST':
        phrase = unquote(request.data.get('phrase'))
        id = request.data.get('id')
        handle=request.data.get('handle')
        dalle_image = get_object_or_404(DalleImage, id=id)
        price = 9.99
        
        if len(handle) > 255:
            error_message = "Dalle phrase length should be less than or equal to 255 characters."
            raise ValidationError(error_message)
        Product.objects.create(
            image=dalle_image.get_image_url(),
            name=phrase,
            handle=handle,
            price=price,
            id=id
        )
        return Response(status=status.HTTP_201_CREATED)
    else:
        return HttpResponseBadRequest("Invalid request method.")
        
    (생략)
    
```
</details>

### Purchases (결제)
<details>
<summary>models.py</summary>

<!-- summary 아래 한칸 공백 두어야함 -->
```python
class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    stripe_checkout_session_id = models.CharField(max_length=220, blank=True, null=True)
    completed = models.BooleanField(default=False)
    stripe_price = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
```
</details>



### chatbot

`고객센터`를 생각하고 `OpenAI`의 `챗봇`을 연결해두었다. 실제로 고객센터의 기능은 하지 않지만 고객센터 역할을 하는 챗봇이 모델링 된다면 바로 연결해서 쓸 수 있게 백엔드를 구현해두었다.
챗봇의 엔진은 `chatgpt`의 예전 모델인 `text-davinchi-003`이다. 

<details>
<summary>views.py</summary>

<!-- summary 아래 한칸 공백 두어야함 -->
```python 
api_key= config("OPENAI_KEY", default=None)
openai.api_key = api_key

def chatbot(request):
    chatbot_response = None
    
    if request.method == 'POST':
        openai.api_key = api_key
        prompts = request.POST.get('text')
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompts,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0

        )
        chatbot_response = response["choices"][0]["text"]
    return render(request, 'contact.html', {"response":chatbot_response})
```    
</details>






## 보안

`aws자격증명`, `DB`,`SECRET_KEY` 등 보안과 관련된 것들은 `.env` 를 만들어 환경변수를 관리하고 민감한 정보가 소스 코드에 노출되지 않도록 하였다.
```
DATABASE_URL='......'
DJANGO_SECRET_KEY='......'
ALLOWED_HOST='......'

OPENAI_KEY='......'
STRIPE_SECRET_KEY='......'

AWS_ACCESS_KEY_ID='......'
AWS_SECRET_ACCESS_KEY='......'
```


`env.py`를 만들고 `python-decouple`라이브러리를 사용하여 `.env` 와 환경변수를 외부에서 로드할 수 있도록 하였다.

<details>
<summary>env.py</summary>

<!-- summary 아래 한칸 공백 두어야함 -->
```python
from functools import lru_cache
from pathlib import Path
from decouple import config as decouple_config, Config, RepositoryEnv
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR.parent
ENV_FILE_PATH = PROJECT_DIR / ".env"


@lru_cache()
def get_config():
    if ENV_FILE_PATH.exists():
        return Config(RepositoryEnv(str(ENV_FILE_PATH)))
    return decouple_config

config = get_config()
```
</details>




## 데이터베이스

`dj-database-url`을 사용해 데이터베이스 URL을 Django의 `settings.py` 파일에서 사용할 수 있도록 하였고
`PostgreSQL` 데이터베이스를 사용하기로 하였다. 
`PostgreSQL` 를 연결할 수 있는 라이브러리인 `psycopg2`를 사용하였고 `psycopg2`는 에러가 나서 `psycopg2-binary` 라이브러리를 사용해 연결과 쿼리 실행을 처리했다.

<details>
<summary>db.py</summary>

<!-- summary 아래 한칸 공백 두어야함 -->
```python
from core.env import config
import dj_database_url

DATABASE_URL= config("DATABASE_URL", default=None)
if DATABASE_URL is not None:
    DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True
    )
}
```
</details>


기존에는 serverless neon postgresql을 사용하였다. <br>
그러나 스키마를 변경해야할 필요성이 있었고, neon postgresql은 스키마를 변경하기에 적합하지 않았다. <br>
postgresql를 설치 후 Amazon RDS에 올렸다.<br>

## AWS


### IAM
Root user를 만들고, AWS_ACCESS_KEY_IDdhk AWS_SECRET_ACCESS_KEY를 발급 받았다.<br>
권한 정책으로 AmazonS3FullAccess를 두었다. <br>

### S3
`정적파일`을 따로 관리하고 달리로 생성되는 이미지인 `미디어파일`을 관리하기 위해 `스토리지`의 필요성을 느꼈다. <br>
`boto3`, `django-storages` 라이브러리를 통해 AWS S3을 Django와 연결하였다. <br>
s3에서 정적호스팅을 활성화하고 퍼블릭 액세스를 허용하였다.<br>
<details>
<summary>Public Access config</summary>

<!-- summary 아래 한칸 공백 두어야함 -->
![](https://velog.velcdn.com/images/iankimdev/post/b8aa8c1d-bd46-47cc-a56a-be0191727099/image.png)
![](https://velog.velcdn.com/images/iankimdev/post/b5c58e6e-93f7-438f-88e4-664f009dca6b/image.png)
![](https://velog.velcdn.com/images/iankimdev/post/8f8eb2f1-252e-4050-aefe-880f7e5a93cb/image.png)
  
퍼블릭 액세스에 버킷 ACL을 읽기를 부여해 두었다.<br>
![](https://velog.velcdn.com/images/iankimdev/post/ce6d0c30-5484-4282-b6f3-619bf87eae65/image.png)
</details>

<details>
<summary>Bucket Policy</summary>

<!-- summary 아래 한칸 공백 두어야함 -->
```
{
    "Version": "2008-10-17",
    "Statement": [
        {
            "Sid": "PublicReadForGetBucketObjects",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::ai-gallery/*"
        },
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": [
                "s3:PutObject",
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::ai-gallery",
                "arn:aws:s3:::ai-gallery/*"
            ]
        }
    ]
}
```
</details>


<details>
<summary>AWS Configuration for S3</summary>

<!-- summary 아래 한칸 공백 두어야함 -->
```
from core.env import config

AWS_ACCESS_KEY_ID=config("AWS_ACCESS_KEY_ID", default=None)
AWS_SECRET_ACCESS_KEY=config("AWS_SECRET_ACCESS_KEY", default=None)
AWS_S3_ADDRESSING_STYLE = "virtual"

AWS_STORAGE_BUCKET_NAME=config("AWS_STORAGE_BUCKET_NAME", default="ai-gallery")
AWS_S3_REGION_NAME="ap-northeast-2"

AWS_DEFAULT_ACL="public-read"
AWS_S3_USE_SSL=True

DEFAULT_FILE_STORAGE = 'core.storages.backends.MediaStorage'
STATICFILES_STORAGE = 'core.storages.backends.StaticFileStorage'
```

```
from storages.backends.s3boto3 import S3Boto3Storage
class MediaStorage(S3Boto3Storage):
    location = "media"

class StaticFileStorage(S3Boto3Storage):
    location = "static"

```
</details>




### EC2

인스턴스가 종료 후 재시작될 때 Public IP의 변경을 막기 위해 탄력적(엘라스틱)IP를 도입하였다. <br>
인바운드 규칙으로 SSH, HTTP, HTTPS를 열어두었다. <br>
플랫폼으로는 Ubuntu를 사용하였고 SSH Key pair를 발급받았다. <br>
처음에는 SSH를 이용해 Github를 EC2에 클론하여 서버를 실행하였지만, Docker를 사용하여 컨테이너로 이미지를 실행하는 것으로 변경하였다. <br>

### RDS

Local에 있는 Postgresql을 AWS RDS에 올려 실행시켰다. <br>

```
brew services start postgresql
psql -U postgres -h database.c43cpyyflb8m.ap-northeast-2.rds.amazonaws.com -p 5432
```


Amazon RDS 보안그룹 인바운드 규칙 생성
![](https://velog.velcdn.com/images/iankimdev/post/bbe754c1-b5fc-436f-acc3-a4e685af0447/image.png)



## Nginx, gunicorn and Docker


`웹서버`를 두어 WAS의 부담을 줄이고 `비동기 처리`와 `리버스 프록시(Reverse proxy)`로 사용 가능한 `Nginx`를 선택하였고 <br>
 배포 환경에서 `WSGI middleware`인 `gunicorn`을 선택하였다. <br>
`gunicorn`은 pip패키지를 통해 설치하였고, `Dockerfile`을 통해 NGINX 웹 서버를 설치하였다. <br>
`entrypoint.sh`에 `gunicorn`과 `nginx`를 설정했다.<br>

<details>
<summary>Dockerfile</summary>

<!-- summary 아래 한칸 공백 두어야함 -->
```
FROM python:3.10.6-slim

# Copy your Django project files
COPY ./django/ /app/

WORKDIR /app

# os-level installs
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    python3-dev \
    python3-setuptools \
    libpq-dev \
    gcc \
    make \
    nginx

# venv & installs
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/python -m pip install pip --upgrade && \
    /opt/venv/bin/python -m pip install -r /app/requirements.txt

# purge unused
RUN apt-get remove -y --purge make gcc build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN chmod +x ./config/entrypoint.sh
CMD ["./config/entrypoint.sh"]
```
</details>



<details>
<summary>entrypoint.sh</summary>

<!-- summary 아래 한칸 공백 두어야함 -->
```
#!/bin/bash
APP_PORT=${PORT:-8000}

cd /app/

/opt/venv/bin/python manage.py collectstatic --noinput
/opt/venv/bin/gunicorn core.wsgi:application --bind "0.0.0.0:${APP_PORT}"
nginx -g "daemon off;"
```
</details>

`docker-compse.yml`을 통해 django 서버와 nginx 서버 컨테이너 환경을 구성 <br>
`default.conf`를 통해 정적파일, 미디어파일 등의 설정과 프록시 설정을 하였다. <br>

<details>
<summary>docker-compose.yml</summary>

<!-- summary 아래 한칸 공백 두어야함 -->
```
version: "3.8"
name: ai-gallery
services:
  django:
    container_name: django
    env_file:
      - .env-prod
    build:
      context: .
      dockerfile: Dockerfile
    image: django
    ports:
      - "8002:8000"
  nginx:
    container_name: nginx
    build:
      context: .
      dockerfile: nginx/Dockerfile
    image: nginx
    ports:
      - "80:80"
    depends_on:
      - django

```
</details>

<details>
<summary>default.conf</summary>

<!-- summary 아래 한칸 공백 두어야함 -->
```
upstream django {
    server django:8002;
}

server {
    listen 80;

    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_pass http://django/static/;
    }

    location /media/ {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_pass http://django/media/;
    }
    
    location = /favicon.ico {
        access_log off;
        log_not_found off;
        return 204;
    }
}

```
</details>


`docker image`를 `build` 후 `docker Hub`에 `push`하였다. <br>
![](https://velog.velcdn.com/images/iankimdev/post/09133186-3a49-4ecc-bea2-91639400b8a3/image.png)

EC2에서 pull로 image를 받은 후 container를 실행하였다.



## 에러처리


<details>
<summary> 프로필 페이지에서 주소를 생성할 때의 서버에러 </summary>

<!-- summary 아래 한칸 공백 두어야함 -->

![](https://velog.velcdn.com/images/iankimdev/post/88ba2733-bab7-4202-bbef-579c4e013aa9/image.png)
모델을 만들 때 shell을 통해서 직접 User객체와 Profile객체를 이어주어서 에러가 없었다가 데이터베이스를 변경하고 마이그레이션 파일들을 재생성해준 후에 발견한 에러이다. 
처음에는 유효성만 통과하면 200을 보내게 구현하였다.

`models.py`
```python
from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
```  

`views.py`
```python
if user_serializer.is_valid() and profile_serializer.is_valid():
            user_serializer.save()
            profile_serializer.save()
            return Response({'success': True, 'message': 'Your profile is updated successfully'}, status=status.HTTP_200_OK)
```

나중에는 기존의 user model에 address만 따로 핸들링하여 address가 없으면 생성해주고 save할 수 있게 변경해주었다.



```python
if not profile:
            profile = Profile(user=user) 
            profile.address = profile_serializer.validated_data.get('address')
            profile.save()
            return Response({'success': True, 'message': 'Your profile is updated successfully'}, status=status.HTTP_200_OK)
```
</details>
<details>
<summary>value too long for type character varying(50)</summary>

<!-- summary 아래 한칸 공백 두어야함 -->

DALLE 이미지를 만들 때 입력값은 "A sunlit indoor lounge area with a pool containing a flamingo" 였다.
phrase는 50자를 조금 넘겼고 그래서 phrase가 50자가 넘으면 발생한다고 생각했다. model의 max_length를 변경하였지만 이번에는 다른 에러가 나왔다. 

```
value too long for type character varying(100)
```
100으로 설정한게 없는데 100이 나왔고 결국에 스키마를 변경해야한다는 것을 알게 되었다. 스키마를 확인해보니 name과 handle이 아닌 오히려 image 테이블의 문제였다는 것을 알게 되었다. 

```
ALTER TABLE products_product ALTER COLUMN handle TYPE character varying(255);
ALTER TABLE products_product ALTER COLUMN image TYPE character varying(1024);
```
명령어를 통해 변경해주고 models.py의 max_length는 원래대로 되돌렸다.
브라우저에는 max_length를 255로 주어 phrase를 컨트롤 하였고 
```javascript
<input type="text" maxlength="255" class="form-control" 
name="user_input" 
placeholder="A sunlit indoor lounge area with a pool containing a flamingo" />
```

서버측에서는 에러가 발생할 때를 대비해 에러메세지를 띄웠다.
```python
if len(handle) > 255:
            error_message = "Dalle phrase length should be less than or equal to 255 characters."
            raise ValidationError(error_message)
```          
</details>



<details>
<summary>openai : "Billing hard limit has been reached"</summary>

<!-- summary 아래 한칸 공백 두어야함 -->

이것은 OpenAI에서 무료 제공하는 기본 사용량을 초과할 때 발생하는 에러 메세지이다.
개발하고 테스트를 진행하는 동안 기본 사용량을 초과하였고, 그 때문에 서버에러가 뜨기에 이 메세지를 핸들링 할 필요성을 느끼고 에러를 브라우저에 표시해주는 코드를 구현하였다.
그리고 Open AI의 지불과 사용량을 조절하였다.
``` python
 except openai_error.InvalidRequestError as e:
       if str(e) == "Billing hard limit has been reached":
           error_message = "OPEN AI's usage limit has been reached. Please contact support for assistance.
               return render(request, "custom/custom-dalle.html", {"error_message": error_message})
``` 
</details>


<details>
<summary>static error</summary>

<!-- summary 아래 한칸 공백 두어야함 -->

Static파일과 Media파일을 S3로 옮기고 처음 접한 에러였다. 로컬에서의 Static파일은 status 200이 나와 정상적으로 실행되었지만 테스트로 실행한 EC2와 Docker container에서의 실행은 status 404가 나왔다. S3 bucket이 static file을 serving 하지 못하는 현상이었다.
S3로 변경후 staticfile을 load하는데서 aws s3 endpoint로 설정하지 않은 첫번째 문제가 있었고, EC2환경과 Docker환경에서의 Collectstatic을 해줘야하는 필요성도 있었다. 

``` html
{# COMMENT: css/output.css comes from the tailwind output #}
<link rel="stylesheet" href="https://ai-gallery.s3.amazonaws.com/static/css/output.css" />

{# COMMENT: vendor_css_files comes from core.context_processors.vendor_files #}
{% for css_file in vendor_css_files %}
<link rel="stylesheet" href="https://ai-gallery.s3.amazonaws.com/static/{{ css_file }}" />
{% endfor %}

{% load static %} {# COMMENT: vendor_js_files comes from core.context_processors.vendor_files #}
{% for js_file in vendor_js_files %}
<script src="https://ai-gallery.s3.amazonaws.com/static/{{ js_file }}" preload></script>
{% endfor %}

```  

``` python
python manage.py collectstatic
``` 

Static이 정상적으로 서빙려면 또 S3버킷에서 정적 웹호스팅을 설정해주었고  bucket policy, ACL, Public Access, 보안그룹 등 기타 설정이 필요했다. 설정들을 끝마치고 비로소 Static file이 로드되었다.
</details>


<details>
<summary>media error</summary>

<!-- summary 아래 한칸 공백 두어야함 -->

처음엔 404에러가 나왔다. 이 문제는 자격증명 다음에 바로 서명이 나왔어야 하는데 서명의 순서가 뒤에 있어서 발생하는 문제가 있었다.
```
# AWS자격증명과 서명이 가장 위에있어야함
AWS_ACCESS_KEY_ID=config("AWS_ACCESS_KEY_ID", default=None)
AWS_SECRET_ACCESS_KEY=config("AWS_SECRET_ACCESS_KEY", default=None)
AWS_S3_SIGNATURE_VERSION = "s3v4"

```

404에러는 해결되었지만 이제는 미디어 파일이 로드되지 않았다. 이미지의 엔드포인트를 확인하여 실행해보니 밑의 에러가 나왔다.
```  
This XML file does not appear to have any style information associated with it. The document tree is shown below.
<Error>
<Code>AuthorizationQueryParametersError</Code>
<Message>Error parsing the X-Amz-Credential parameter; the region 'us-east-1' is wrong; expecting 'ap-northeast-2'</Message>
<Region>ap-northeast-2</Region>
<RequestId>FQG11ZKWWR3C8S61</RequestId>
<HostId>QQnh9RAD3EywoHXAQcDkmMKYv8nvYil8lqXehmxRhW6Ojwl32tVjm2JPd/8RvUlNm9ViajDO++Q=</HostId>
</Error>
```  
![](https://velog.velcdn.com/images/iankimdev/post/35ea96f6-410a-4d64-9a19-162d66c4d995/image.png)

이 에러를 분석해보니 AWS S3에 대한 권한 및 리전 설정과 관련이 있었다. 에러 메시지에 따르면 "AuthorizationQueryParametersError"가 발생하였으며, "X-Amz-Credential" 매개변수를 파싱하는 중에 문제가 발생했다고 한다. 

내가 실제로 지정한 리전은 `'ap-northeast-2'`였는데 오류 메시지는 올바른 리전을 예상하고 있으나 `'us-east-1'`이라는 잘못된 리전이 포함되어 있다고 언급하고 있었다. 

내 자격증명을 찬찬히 살펴보고 `AWS_S3_SIGNATURE_VERSION = "s3v4"`  와 관련이 있다는 것을 알게되었고 찾아보니 예상대로였다. 내가 사용한 ` s3v4` 는 ` us-east-1` 에 매칭되었고 나의 리전인 ` 'ap-northeast-2'` 에 매칭되는 `AWS_S3_ADDRESSING_STYLE = "virtual"` 을 사용하였다.

https://github.com/jschneier/django-storages/issues/782
</details>



<details>
<summary>EC2에서 nginx 컨테이너가 실행되지 않는 문제</summary>

<!-- summary 아래 한칸 공백 두어야함 -->
docker logs nginx로 로그를 살펴보니 80번 포트를 계속 사용중이라는 에러였다. 그러나 80번을 사용하고 있는 프로세스는 없었다.

의아함을 느끼다가 가상환경 버전의 문제일까 생각해보았고 초기에 로컬의 가상환경 버전은 3.11.3이었다. 그러나 AWS EC2의 가장 최신버전은 3.10.6이었다. EC2의 파이썬버전으로 로컬의 가상환경 버전을 변경하였더니 nginx 컨테이너가 실행되었다.

그리고 run 명령어를 작성할 때 link를 통해 django와 nginx를 연결해주었다.
```  
sudo docker run -d --name nginx -p 80:80 link django iankimdev/nginx
```  
</details>


<details>
<summary>EC2에서 django 컨테이너가 실행되지 않는 문제</summary>

<!-- summary 아래 한칸 공백 두어야함 -->
![](https://velog.velcdn.com/images/iankimdev/post/e8038673-33cd-46c8-b593-9e7133557cf3/image.png)

docker logs django 를 사용해 로그를 살펴보니 SECRET KEY에 관한 에러 내용이었다.

SECRET KEY는 .env파일에 있었기 때문에 의아하다고 생각했고 하드코딩으로 settings.py에 적어주자 이번엔 AWS 자격증명에 관한 에러 내용이었다.
그래서 .env파일을 읽지 못한다는 것을 알아챘고 .env를 읽을 수 있는 명령어로 컨테이너를 실행했다.


```  
sudo docker run -d --name django -p 8002:8000 --env-file .env-prod iankimdev/django
sudo docker run -d --name nginx -p 80:80 --env-file .env-prod --link django iankimdev/nginx
```  
link라고 명시해주었다.

</details>

<details>
<summary>media파일이 만료되는 문제</summary>

<!-- summary 아래 한칸 공백 두어야함 -->

![](https://velog.velcdn.com/images/iankimdev/post/c12fa887-1a5d-4200-a683-df4e3b720906/image.png)


![](https://velog.velcdn.com/images/iankimdev/post/a4e44afb-ab2e-4661-b410-a5f65db5b924/image.png)
pre-signed url때문이었다. 우선 ExpiresIn=3600을 주석처리 하였고 product객체의 이미지에 같이 붙는 AWS자격증명을 지워주었다.


``` python

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
```  

``` python
def products_list(request):
    products_list = Product.objects.all()
    
    for product in products_list:
        url = str(product.image)
        url_without_query = url.split('?')[0]
        product.image = url_without_query

    return render(request, 'products/list.html', {"products_list": products_list})
```  
product.image<br>
AWS자격증명을 지운 수정된 product.image<br>
![](https://velog.velcdn.com/images/iankimdev/post/f02765cb-582b-43ef-a330-399267d6677d/image.png)
</details>

## 개선점
1. 매니저 권한의 가격 설정 도입
2. 결제 api 모듈의 다양화
3. chatbot의 최적화(응답 길이, 응답 방향 등)
4. 서버 최적화(로딩 속도)


