## Project

AI image ordering/production e-commerce using `DALLE` and `chatGPT`

- personal project
- Create images with AI using OpenAI’s DALLE engine
- Manage customer interactions using chatbots using OpenAI’s ChatGPT engine

  
## Stack
- Javascript
- Python, Django
- PostgreSQL
- Docker, Nginx
- Amazon S3, Amazon EC2, Amazon RDS


## UI 

<br>

#### [Creating images with DALLE]
<img width="663" alt="Screen Shot 2023-07-02 at 16 34 53" src="https://github.com/iankimdev/AI-gallery-django/assets/120093816/ebd674e2-f137-4393-864e-5d1c5402d119">

#### [Order]
<img width="690" alt="Screen Shot 2023-07-02 at 16 33 54" src="https://github.com/iankimdev/AI-gallery-django/assets/120093816/b6664b1b-9abe-4825-9053-e6ea208edd94">

#### [Payment]
<img width="685" alt="Screen Shot 2023-07-02 at 16 34 05" src="https://github.com/iankimdev/AI-gallery-django/assets/120093816/c8adb95f-4a76-40b6-95af-4b6e0bf0edc3">

#### [Check order details]
<img width="693" alt="Screen Shot 2023-07-02 at 16 34 22" src="https://github.com/iankimdev/AI-gallery-django/assets/120093816/bbc4e738-043b-4b61-88c1-203e972eb009">

#### [Confirm order list]
<img width="690" alt="Screen Shot 2023-07-02 at 16 34 25" src="https://github.com/iankimdev/AI-gallery-django/assets/120093816/0cf95045-bf76-4d29-9012-adc3e7d6dedd">


<br>

## APPS

For `Django APP`, `User`, `DALLE`, `Product`, `Payment`, and `ChatGPT` were used.

### DALLE 

`Image AI` from `openai` was used. You can use `DALLE` by creating a `secretkey` in `openai` and requesting `api`.
`phrase`, the text entered by the user, and `ai_image`, the generated image, were used as the `DB table`.

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

Otherwise, if you create an image and then place an order, it is created as a ‘product’.<br>
Views.py was created with the idea that when Dali creates an image, an e-commerce manager can download it and sell it as a product. <br>
However, because this method was considered inefficient, this module was no longer used and was changed to allow users to create the image they want as a 'custom' and order it directly.<br>
`handle` was set to `uinque` and used as `slug`.<br>

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
    
    # STRIPE 
    stripe_product_id = models.CharField(max_length=220, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=220, blank=True, null=True)
    stripe_price = models.IntegerField(default=999) # 100 * price
    price_changed_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    
    
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
        
    
    
```


### Purchases

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

I thought about ‘customer center’ and connected ‘OpenAI’’s ‘chatbot’. Although it does not actually function as a customer center, we have implemented a backend so that if a chatbot that functions as a customer center is modeled, it can be immediately connected and used.
The chatbot engine is `text-davinchi-003`, the old model of `chatgpt`.

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






## Security


For security-related items such as `aws credentials`, `DB`, and `SECRET_KEY`, `.env` was created to manage environment variables and prevent sensitive information from being exposed to the source code.

```
DATABASE_URL='......'
DJANGO_SECRET_KEY='......'
ALLOWED_HOST='......'

OPENAI_KEY='......'
STRIPE_SECRET_KEY='......'

AWS_ACCESS_KEY_ID='......'
AWS_SECRET_ACCESS_KEY='......'
```



I created `env.py` and used the `python-decouple` library to enable `.env` and environment variables to be loaded externally.


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





## Database

Use `dj-database-url` to make the database URL available in Django's `settings.py` file.
I decided to use the `PostgreSQL` database.
I used `psycopg2`, a library that can connect `PostgreSQL`, and `psycopg2` gave an error, so I used the `psycopg2-binary` library to handle connection and query execution.

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


Previously, serverless neon postgresql was used. <br>
However, there was a need to change the schema, and neon postgresql was not suitable for changing the schema. <br>
After installing postgresql, I uploaded it to Amazon RDS.<br>

## AWS

### S3

I felt the need for ‘storage’ to manage ‘static files’ separately and ‘media files’, which are images created with Dali. <br>
AWS S3 was connected to Django through the `boto3` and `django-storages` libraries. <br>
Static hosting was enabled on s3 and public access was allowed.<br>


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

I installed a `web server` to reduce the burden on WAS and chose `Nginx`, which can be used as `asynchronous processing` and `reverse proxy` <br>
 In the deployment environment, `gunicorn`, `WSGI middleware`, was selected. <br>
`gunicorn` was installed through the pip package, and the NGINX web server was installed through `Dockerfile`. <br>
`gunicorn` and `nginx` were set in `entrypoint.sh`.<br>

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

Configure django server and nginx server container environment through `docker-compse.yml` <br>
Static files, media files, etc. and proxy settings were set through `default.conf`. <br>

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




## error logs

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


In the existing user model, only addresses were handled separately, so if addresses did not exist, they were created and saved.



```python
if not profile:
            profile = Profile(user=user) 
            profile.address = profile_serializer.validated_data.get('address')
            profile.save()
            return Response({'success': True, 'message': 'Your profile is updated successfully'}, status=status.HTTP_200_OK)
```


### value too long for type character varying(50)


When creating the DALLE image, the input value was "A sunlit indoor lounge area with a pool containing a flamingo".
The phrase was a little over 50 characters, so I thought it occurred when the phrase was over 50 characters. I changed the max_length of the model, but this time a different error occurred.

```
value too long for type character varying(100)
```

I didn't set anything to 100, but it came out as 100, and I eventually realized that I needed to change the schema. After checking the schema, I found out that the problem was not with name and handle, but rather with the image table.

```
ALTER TABLE products_product ALTER COLUMN handle TYPE character varying(255);
ALTER TABLE products_product ALTER COLUMN image TYPE character varying(1024);
```
I changed it through the command, and max_length in models.py was returned to its original state.
In the browser, the phrase was controlled by setting max_length to 255.
```javascript
<input type="text" maxlength="255" class="form-control" 
name="user_input" 
placeholder="A sunlit indoor lounge area with a pool containing a flamingo" />
```

The server side displayed an error message in case an error occurred.
```python
if len(handle) > 255:
            error_message = "Dalle phrase length should be less than or equal to 255 characters."
            raise ValidationError(error_message)
```          

### "Billing hard limit has been reached"

This is an error message that occurs when you exceed the basic usage amount provided free of charge by OpenAI.
During development and testing, the default usage amount was exceeded, and as a result, a server error occurred, so I felt the need to handle this message and implemented code to display the error in the browser.
And the payment and usage of Open AI were adjusted..
``` python
 except openai_error.InvalidRequestError as e:
       if str(e) == "Billing hard limit has been reached":
           error_message = "OPEN AI's usage limit has been reached. Please contact support for assistance.
               return render(request, "custom/custom-dalle.html", {"error_message": error_message})
``` 

### AuthorizationQueryParametersError

At first, a 404 error appeared. This problem occurred because the signature should have appeared immediately after the credentials, but the signatures were placed later in the order.
```

AWS_ACCESS_KEY_ID=config("AWS_ACCESS_KEY_ID", default=None)
AWS_SECRET_ACCESS_KEY=config("AWS_SECRET_ACCESS_KEY", default=None)
AWS_S3_SIGNATURE_VERSION = "s3v4"

```

The 404 error was resolved, but now the media file is not loaded. When I checked the endpoint of the image and ran it, the error below appeared.
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

Analysis of this error revealed that it was related to permissions and region settings for AWS S3. According to the error message, "AuthorizationQueryParametersError" occurred and a problem occurred while parsing the "X-Amz-Credential" parameter. The region I actually specified was `'ap-northeast-2'`, but the error message stated that it was expecting the correct region, but included an incorrect region called `'us-east-1'`.

I looked at my credentials and found that it had something to do with `AWS_S3_SIGNATURE_VERSION = "s3v4"` and when I looked it up, it was as expected. The `s3v4` I used matched `us-east-1` and I used `AWS_S3_ADDRESSING_STYLE = "virtual"` which matched my region `'ap-northeast-2'`.

https://github.com/jschneier/django-storages/issues/782

### Problem with media files expiring

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

## Improvements
1. Introduction of price setting with manager authority
2. Diversification of payment API module
3. Chatbot optimization (response length, response direction, etc.)
