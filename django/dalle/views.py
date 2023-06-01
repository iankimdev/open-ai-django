from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import openai, os, requests, openai.error
from django.core.files.base import ContentFile
from .models import DalleImage
from django.contrib.auth.decorators import login_required
from core.env import config
from rest_framework.decorators import api_view
from openai import error as openai_error



# Create your views here.
api_key= config("OPENAI_KEY", default=None)
openai.api_key = api_key


def download_image(request, image_id):
    image = get_object_or_404(DalleImage, id=image_id)
    file_path = image.ai_image.path

    with open(file_path, "rb") as f:
        response = HttpResponse(f.read(), content_type="image/jpeg")
        response["Content-Disposition"] = f"attachment; filename={image.ai_image.name}"
        return response

@api_view(['GET', 'POST'])
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
                    error_message = "OPEN AI's usage limit has been reached. Please contact support for assistance. OPEN AI의 사용량이 초과하였습니다. 저에게 알려주시면 처리하겠습니다."
                    return render(request, "custom/custom-dalle.html", {"error_message": error_message})
    return render(request, "custom/custom-dalle.html", {"product": dalle})