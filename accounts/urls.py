from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    # 新規登録
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('mypage/', views.MyPageView.as_view(), name='mypage'),
    path('', include('django.contrib.auth.urls')),
]