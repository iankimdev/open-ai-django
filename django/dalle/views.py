from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import openai, os, requests
from django.core.files.base import ContentFile
from .models import DalleImage
from django.contrib.auth.decorators import login_required
from core.env import config
from products.models import Product
# Create your views here.
api_key= config("OPENAI_KEY", default=None)
#api_key = os.getenv("OPENAI_KEY")
openai.api_key = api_key


def download_image(request, image_id):
    image = get_object_or_404(DalleImage, id=image_id)
    file_path = image.ai_image.path

    with open(file_path, "rb") as f:
        response = HttpResponse(f.read(), content_type="image/jpeg")
        response["Content-Disposition"] = f"attachment; filename={image.ai_image.name}"
        return response

@login_required
def generate_image_from_txt_for_custom(request):
    obj = None
    if api_key is not None and request.method == 'POST':
        user_input = request.POST.get("user_input")
        response = openai.Image.create(
            prompt = user_input,
            size = "512x512",
        )
        #print(response)
        img_url = response["data"][0]["url"]
        img_response = requests.get(img_url)
        img_file = ContentFile(img_response.content) #Bytes => Images
        #print(img_file)
        count = DalleImage.objects.count() + 1
        #fname = f"image-{count}.jpg"
        fname = f"image-{count}.jpg"
        
        obj = DalleImage(phrase=user_input)
        obj.ai_image.save(fname, img_file)
        obj.save()
    return render(request, "custom/custom-dalle.html", {"product":obj})

