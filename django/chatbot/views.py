from django.shortcuts import render
import openai
from core.env import config
api_key= config("OPENAI_KEY", default=None)
openai.api_key = api_key

def chatbot(request):
    chatbot_response = None
    print("request", request)
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



