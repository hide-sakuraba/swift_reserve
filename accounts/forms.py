from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email") # 必要に応じてemailなどを追加