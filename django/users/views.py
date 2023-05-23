from django.shortcuts import render, redirect
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('http://127.0.0.1:8000/')  # 회원 가입 후 리다이렉트할 URL 설정
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
