from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
    
'''
User 모델과 Profile 모델 간의 일대일 관계를 설정한 후에 이전에 생성된 User 객체에 대한 Profile 객체를 생성해야 함


# Django shell 실행
python manage.py shell

# shell 내에서 다음 코드 실행
from django.contrib.auth.models import User
from users.models import Profile

# User 객체 가져오기
user = User.objects.get(username='사용자명')

# Profile 객체 생성
profile = Profile(user=user, address='주소', ...)  # 주소와 다른 필드들을 적절하게 설정

# Profile 객체 저장
profile.save()
'''
