from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Room, Booking
import json
from django.utils.dateparse import parse_datetime
from django.views import View
from django.http import JsonResponse

# Create your views here
class HomeView(ListView):
    model = Room
    template_name = 'core/home.html'
    context_object_name = 'rooms' # テンプレート内で使う変数名

# 会議室詳細画面（カレンダー表示）
class RoomDetailView(DetailView):
    model = Room
    template_name = 'core/room.html'
    context_object_name = 'room'

# カレンダーに表示する予約データをJsonで返すビュー
def get_bookings(request, room_id):
    # 特定の会議室の予約を取得
    bookings = Booking.objects.filter(room=room_id)

    # FullCalendarが読み込める形式に変換
    events = []
    for b in bookings:
        events.append({
            'id': b.id,
            'title': b.title,
            'start': b.start_time.isoformat(),
            'end': b.end_time.isoformat(),
        })
    return JsonResponse(events, safe=False)

# 予約作成用ビュー
class CreateBookingView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            # データの保存
            booking = Booking.objects.create(
                room_id=data['room_id'],
                user=request.user,
                title=data['title'],
                start_time=parse_datetime(data['start']),
                end_time=parse_datetime(data['end']),
            )
            return JsonResponse({'status': 'success', 'booking_id': booking.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)