## 프로젝트 소개

`DALLE` 와 `chatGPT`를 활용한 AI 이미지 주문/제작 이커머스

- 개인 프로젝트
- OpenAI의 DALLE 엔진을 사용하여 이미지를 AI로 제작
- OpenAI의 ChatGPT 엔진을 사용하여 chatbot을 사용하여 고객 상담 관리

## 배포 URL
- http://13.125.33.210:8002
  
## 기술 스택
- Javascript
- Python, Django
- PostgreSQL
- Docker, Nginx
- Amazon S3, Amazon EC2, Amazon RDS


## UI 

<br>

#### [DALLE로 이미지 생성]
<img width="663" alt="Screen Shot 2023-07-02 at 16 34 53" src="https://github.com/iankimdev/AI-gallery-django/assets/120093816/ebd674e2-f137-4393-864e-5d1c5402d119">

#### [주문]
<img width="690" alt="Screen Shot 2023-07-02 at 16 33 54" src="https://github.com/iankimdev/AI-gallery-django/assets/120093816/b6664b1b-9abe-4825-9053-e6ea208edd94">

#### [결제]
<img width="685" alt="Screen Shot 2023-07-02 at 16 34 05" src="https://github.com/iankimdev/AI-gallery-django/assets/120093816/c8adb95f-4a76-40b6-95af-4b6e0bf0edc3">

#### [주문 확인(유저)]
<img width="693" alt="Screen Shot 2023-07-02 at 16 34 22" src="https://github.com/iankimdev/AI-gallery-django/assets/120093816/bbc4e738-043b-4b61-88c1-203e972eb009">

#### [모든 유저의 전체 주문 확인(매니저)]
<img width="690" alt="Screen Shot 2023-07-02 at 16 34 25" src="https://github.com/iankimdev/AI-gallery-django/assets/120093816/0cf95045-bf76-4d29-9012-adc3e7d6dedd">


<br>

## APPS

`Django APP`으로는 `유저`, `DALLE`, `상품`, `결제`, `ChatGPT`를 사용하였다.

### DALLE 

`openai`의 `Image AI`를 사용하였다. `openai`에서 `secretkey`를 생성하고 `api`를 요청하면 `DALLE`를 사용할 수 있다.
유저가 입력하는 text인 `phrase`와 생성되는 이미지인 `ai_image`를 `DB 테이블`로 사용하였다.

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




### Products (AI image)

달리 이미지를 생성 후 주문하면 `상품`으로 생성되게 구현하였다.<br>
달리가 이미지를 생성하면 이커머스 관리자가 다운로드 받아서 그것을 상품으로 올려 판매하는 것을 생각하고 Views.py를 만들었다. <br>
그러나 이런 방식이 비효율적이라고 생각했기 때문에 이 모듈은 더 이상 사용하지 않고 유저가 직접 원하는 이미지를 `커스텀`으로 만들어서 그것을 바로 주문하는 것으로 변경하였다.<br>
`handle`을 `uinque`로 두어서 `slug`로 사용했다.<br>

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


### Purchases (결제)

```python
class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    stripe_checkout_session_id = models.CharField(max_length=220, blank=True, null=True)
    completed = models.BooleanField(default=False)
    stripe_price = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
```



### chatbot

`고객센터`를 생각하고 `OpenAI`의 `챗봇`을 연결해두었다. 실제로 고객센터의 기능은 하지 않지만 고객센터 역할을 하는 챗봇이 모델링 된다면 바로 연결해서 쓸 수 있게 백엔드를 구현해두었다.
챗봇의 엔진은 `chatgpt`의 예전 모델인 `text-davinchi-003`이다. 


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





## 데이터베이스

`dj-database-url`을 사용해 데이터베이스 URL을 Django의 `settings.py` 파일에서 사용할 수 있도록 하였고
`PostgreSQL` 데이터베이스를 사용하기로 하였다. 
`PostgreSQL` 를 연결할 수 있는 라이브러리인 `psycopg2`를 사용하였고 `psycopg2`는 에러가 나서 `psycopg2-binary` 라이브러리를 사용해 연결과 쿼리 실행을 처리했다.

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



기존에는 serverless neon postgresql을 사용하였다. <br>
그러나 스키마를 변경해야할 필요성이 있었고, neon postgresql은 스키마를 변경하기에 적합하지 않았다. <br>
postgresql를 설치 후 Amazon RDS에 올렸다.<br>

## AWS

### S3
`정적파일`을 따로 관리하고 달리로 생성되는 이미지인 `미디어파일`을 관리하기 위해 `스토리지`의 필요성을 느꼈다. <br>
`boto3`, `django-storages` 라이브러리를 통해 AWS S3을 Django와 연결하였다. <br>
s3에서 정적호스팅을 활성화하고 퍼블릭 액세스를 허용하였다.<br>


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





## Nginx, gunicorn and Docker


`웹서버`를 두어 WAS의 부담을 줄이고 `비동기 처리`와 `리버스 프록시(Reverse proxy)`로 사용 가능한 `Nginx`를 선택하였고 <br>
 배포 환경에서 `WSGI middleware`인 `gunicorn`을 선택하였다. <br>
`gunicorn`은 pip패키지를 통해 설치하였고, `Dockerfile`을 통해 NGINX 웹 서버를 설치하였다. <br>
`entrypoint.sh`에 `gunicorn`과 `nginx`를 설정했다.<br>

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




```
#!/bin/bash
APP_PORT=${PORT:-8000}

cd /app/

/opt/venv/bin/python manage.py collectstatic --noinput
/opt/venv/bin/gunicorn core.wsgi:application --bind "0.0.0.0:${APP_PORT}"
nginx -g "daemon off;"
```

`docker-compse.yml`을 통해 django 서버와 nginx 서버 컨테이너 환경을 구성 <br>
`default.conf`를 통해 정적파일, 미디어파일 등의 설정과 프록시 설정을 하였다. <br>

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




## 에러처리 기록

<br>

### null value in column violates not-null constraint


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

기존의 user model에 address만 따로 핸들링하여 address가 없으면 생성해주고 save할 수 있게 변경해주었다.



```python
if not profile:
            profile = Profile(user=user) 
            profile.address = profile_serializer.validated_data.get('address')
            profile.save()
            return Response({'success': True, 'message': 'Your profile is updated successfully'}, status=status.HTTP_200_OK)
```


### value too long for type character varying(50)

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

### "Billing hard limit has been reached"

이것은 OpenAI에서 무료 제공하는 기본 사용량을 초과할 때 발생하는 에러 메세지이다.
개발하고 테스트를 진행하는 동안 기본 사용량을 초과하였고, 그 때문에 서버에러가 뜨기에 이 메세지를 핸들링 할 필요성을 느끼고 에러를 브라우저에 표시해주는 코드를 구현하였다.
그리고 Open AI의 지불과 사용량을 조절하였다.
``` python
 except openai_error.InvalidRequestError as e:
       if str(e) == "Billing hard limit has been reached":
           error_message = "OPEN AI's usage limit has been reached. Please contact support for assistance.
               return render(request, "custom/custom-dalle.html", {"error_message": error_message})
``` 

### AuthorizationQueryParametersError

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

이 에러를 분석해보니 AWS S3에 대한 권한 및 리전 설정과 관련이 있었다. 에러 메시지에 따르면 "AuthorizationQueryParametersError"가 발생하였으며, "X-Amz-Credential" 매개변수를 파싱하는 중에 문제가 발생했다고 한다. 내가 실제로 지정한 리전은 `'ap-northeast-2'`였는데 오류 메시지는 올바른 리전을 예상하고 있으나 `'us-east-1'`이라는 잘못된 리전이 포함되어 있다고 언급하고 있었다. 

내 자격증명을 살펴보고 `AWS_S3_SIGNATURE_VERSION = "s3v4"`  와 관련이 있다는 것을 알게되었고 찾아보니 예상대로였다. 내가 사용한 ` s3v4` 는 ` us-east-1` 에 매칭되었고 나의 리전인 ` 'ap-northeast-2'` 에 매칭되는 `AWS_S3_ADDRESSING_STYLE = "virtual"` 을 사용하였다.

https://github.com/jschneier/django-storages/issues/782

### media파일이 만료되는 문제

![](https://velog.velcdn.com/images/iankimdev/post/c12fa887-1a5d-4200-a683-df4e3b720906/image.png)
![](https://velog.velcdn.com/images/iankimdev/post/a4e44afb-ab2e-4661-b410-a5f65db5b924/image.png)
pre-signed url때문이었다. product객체의 이미지에 같이 붙는 AWS자격증명을 지워주었다.



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

## 개선점
1. 매니저 권한의 가격 설정 도입
2. 결제 api 모듈의 다양화
3. chatbot의 최적화(응답 길이, 응답 방향 등)

## 회고

`이스트소프트의 백엔드 교육`을 들으면서 `AI`에 관심을 가졌고, `Chatbot`이나 `DALLE` 등 AI 모델을 활용한 토이 프로젝트를 만들고 싶었다. 달리나 챗봇을 사용하며 api의 키를 것들을 숨기기 위한 고민도 많았다. 깃허브에는 이러한 중요 정보들이 올라가면 안되기 때문에 gitignore와 .env파일에 대한 것들을 공부하였고 .env파일의 환경변수를 가져올 수 있는 그런 코드를 먼저 구현하였다. 데이터베이스는 현재 회사에서 자주 사용했던 PostgreSQL을 선택하고 Amazon RDS와 pgAdmin 4를 활용하였다.

DALLE는 openai의 document를 보고 미리 구현해보았었다. 다른 레포지토리에 구현을 해두었었고 상품을 먼저 도입하고 달리를 그 후에 연결하기로 결정했다. 맨 처음에는 달리로 이미지를 만들면, 그 이미지를 다운로드해서 관리자가 갤러리에 진열을 해두는 것으로 기획했었다. 그래서 파일 업로드/다운로드와 첨부파일에 대한 코드를 작성을 했었다. 처음에 이 코드를 작성할 때는 formset 등 완벽하게 이해하진 못했지만 흐름을 이해하고 여러 자료들을 통해 기능이 작동하게끔 했었다. 달리의 여러 엔진 중 저렴하면서 성능이 괜찮은 버전의 엔진을 사용하였다. 달리를 통해 계속 이미지를 생성하니까 사용량이 초과하여 금액이 발생하는 상황이 있었다. Django의 Contentfile로 파일을 관리를 하고 생성된 이미지의 url은 `response["data"][0]["url"]`이다. 

openAI의 대표모델인 chatGPT 또한 이용하고 싶었다. 그래서 현재의 chatGPT모델 또한 가격과 사용량이 비쌌기에 이전 모델인 text-davinchi-003 engine을 사용하였다. 고객센터를 chatGPT로 도입한다고 가정하였으나 실제 내 사이트에 맞는 고객센터용 ai모델이 아닌 openAI의 테스트모델이기 때문에 내가 원하는대로의 답변은 해주지 못하였다. 하지만 chat engine을 가져와 사용하는 백엔드를 구축하며 나중에 필요할 때 사용할 수 있는 연습을 했다고 생각한다. chatbot의 최적화 역시 현재 사이트에서 중요한 역할이 아니었기 때문에 그에 대한 리팩토링은 후순위로 미루었다.

상품 모델을 구현할 때 slug를 통해 정보를 받아야겠다고 생각했고 slug로 handle을 두어 unique하게 구현하였다. Stripe결제를 사용했다. 결제 시 Stripe객체의 id값을 사용하였다. 카카오/네이버페이보다 해외 결제시스템에 대한 자료들이 더 많았고 이해하기가 쉬웠다. 우선 Stripe를 완벽히 이해하고 그 후에 카카오나 네이버페이 등을 구현하기로 결정했다.

유저를 구현하면서 기본 유저모델을 사용하며 유저가 주문 배송을 받는다고 가정하고 address필드만 추가로 커스텀하였다. 기본적인 회원가입/로그인을 구현하고 프로필 페이지에서 address를 추가할 수 있도록 구현하였다. 유저의 DRF도입 후 product도 개선이 필요하다고 생각하여 DRF로 개선하였다. 하지만 product의 create나 update는 기본적인 CRUD구현이 아니라 dalle에 의한 create이며 update도 따로 할 필요가 없었기에 완전한 CRUD의 DRF 리팩토링은 아니고 필요한 부분만 개선하였다. 유저 회원가입/로그인 시 정규식을 더 적극적으로 활용하고 여러 개선해야할 점이 보였지만 DALLE와 chatbot을 활용하는게 더 중요하다고 판단하여 그에 대한 리팩토링은 후순위로 미루었다.

서버는 AWS를 사용하였다. AWS에 회사에서 사용해 어느 정도 알고 있는 상태였지만 이번 프로젝트를 진행하며 조금 더 자세하게 알게 되었다. AWS에 서버를 올리기 전에 Storage의 사용이 필요하다고 생각했다. 현재 달리로 생성되는 이미지는 로컬에 지정된 경로에 생성되고 있었으며 서버에 올리면 서버에 계속 생성될 것이기 때문이다. 그리고 정적파일을 서빙하는 과정에서 WAS와 WS역할 그리고 최적화에 대해 알게 되었고 S3으로 이동하는 작업이 필요하다고 느꼈다. S3은 사용만해봤지 실제로 이동시키면서 생각하지 못했던 에러를 많이 만났다. 결국에는 다 해결하고 미디어파일과 정적파일을 S3에서 제공하였다. 그리고 Docker를 사용하여 컨테이너를 EC2 내에서 실행하였다. docker-compose.yml을 사용하여 이미지를 빌드하였고 추가로 Nginx를 통한 정적파일 관리를 하였다. 

 이 프로젝트는 팀 프로젝트 시작하는 기간에 비슷하게 맞춰 끝내고 팀 프로젝트에 집중했다. 이 개인 프로젝트 경험을 바탕으로 팀 프로젝트를 이끌었다.
