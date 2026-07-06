from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth import login
from .forms import SignupForm, CustomUserCreationForm
from core.models import Booking
from django.contrib.auth.mixins import LoginRequiredMixin

class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('core:home') # 登録後のリダイレクト先

    def form_valid(self, form):
        # 保存したユーザーを有効化し、そのままログインさせる
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid

class MyPageView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'accounts/mypage.html'
    context_object_name = 'booking_list'

    def get_queryset(self):
        # ログインしているユーザーの予約だけを、日付が新しい順に取得
        return Booking.objects.filter(user=self.request.user).order_by('start_time')
