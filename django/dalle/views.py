from django.shortcuts import render
import openai, os, requests
from django.core.files.base import ContentFile
from .models import DalleImage
from django.views.decorators.csrf import csrf_exempt
from core.env import config
# Create your views here.
api_key= config("OPENAI_KEY", default=None)
#api_key = os.getenv("OPENAI_KEY")
openai.api_key = api_key
@csrf_exempt
def generate_image_from_txt(request):
    obj = None
    if api_key is not None and request.method == 'POST':
        user_input = request.POST.get("user_input")
        response = openai.Image.create(
            prompt = user_input,
            size = '256x256',
        )
        #print(response)
        img_url = response["data"][0]["url"]
        img_response = requests.get(img_url)
        img_file = ContentFile(img_response.content) #Bytes => Images
        #print(img_file)
        count = DalleImage.objects.count() + 1
        fname = f"image-{count}.jpg"

        obj = DalleImage(phrase=user_input)
        obj.ai_image.save(fname, img_file)
        obj.save()
        

    return render(request, "home.html", {"object":obj})