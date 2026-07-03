from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import Room, Booking
import json
from django.utils.dateparse import parse_datetime
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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
class CreateBookingView(View):
    def post(self, request, *args, **kwargs):
        # 1. ログインチェック（API的に401を返す）
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'error',
                'message': 'セッションが切れました。ログインし直してください。'
            }, status=401)

        try:
            # 2. JSから送られたJSONデータを解析
            data = json.loads(request.body)

            # 3. データの取り出し
            room_id = data.get('room_id')
            title = data.get('title', '無題の予約')

            start_dt = parse_datetime(data.get('start'))
            end_dt = parse_datetime(data.get('end'))

            # 4. バリデーション（簡易）
            if not all([room_id, start_dt, end_dt]):
                return JsonResponse({
                    'status': 'error',
                    'message': '予約時間が正しく送信されませんでした。'
                }, status=400)

            # 5. 保存実行
            booking = Booking.objects.create(
                room_id=room_id,
                user=request.user,
                title=title,
                start_time=start_dt,
                end_time=end_dt
            )

            return JsonResponse({
                'status': 'success',
                'booking_id': booking.id
            })

        except Exception as e:
            # エラーログを表示
            print(f"Booking Error: {e}")
            return JsonResponse({
                'status': 'error',
                'message': '保存中にエラーが発生しました。'
            }, status=400)

        try:
            # データの保存
            # 注意：モデルのフィールド名が 'start_at' か 'start_time' か、プロジェクトの定義に合わせてください
            booking = Booking.objects.create(
                room_id=data.get('room_id'),
                user=request.user,
                title=data.get('title', '無題の予約'),  # titleがない場合のデフォルト値
                start_at=parse_datetime(data.get('start')),  # フィールド名がstart_atの場合
                end_at=parse_datetime(data.get('end')),  # フィールド名がend_atの場合
            )
            return JsonResponse({'status': 'success', 'booking_id': booking.id})

        except Exception as e:
            # デバッグ用にエラー内容を出力
            print(f"Booking Error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

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

class BookingDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Booking
    success_url = reverse_lazy('accounts:mypage') # 削除後はマイページへ

    def test_func(self):
        # ログインユーザーと予約者が一致するかチェック
        booking = self.get_object()
        return self.request.user == booking.user
