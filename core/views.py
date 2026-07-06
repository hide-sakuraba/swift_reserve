from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import Room, Booking
import json
from django.utils.dateparse import parse_datetime
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.contrib import messages

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
        # 1. ログインチェック
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'error',
                'message': 'セッションが切れました。ログインし直してください。'
            }, status=401)

        try:
            # 2. JSONデータの解析
            data = json.loads(request.body)

            room_id = data.get('room_id')
            title = data.get('title', '無題の予約')
            # JSからの文字列形式のISO日時をPythonのdatetimeオブジェクトに変換
            start_dt = parse_datetime(data.get('start'))
            end_dt = parse_datetime(data.get('end'))

            # 3. 基本的な入力バリデーション
            if not all([room_id, start_dt, end_dt]):
                return JsonResponse({
                    'status': 'error',
                    'message': '予約時間が正しく送信されませんでした。'
                }, status=400)

            # 4. ビジネスロジック・バリデーション
            # 現在時刻より前の予約は不可
            if start_dt < timezone.now():
                return JsonResponse({
                    'status': 'error',
                    'message': '過去の日時で予約することはできません。'
                }, status=400)

            # 終了時間は開始時間より後であること
            if start_dt >= end_dt:
                return JsonResponse({
                    'status': 'error',
                    'message': '終了時間は開始時間よりも後の時刻にしてください。'
                }, status=400)

            # 5. 重複チェック（重要！）
            # 条件: 同じ部屋(room_id)で、時間が重なっている予約があるか
            # 重複判定の公式: (既存の開始 < 入力の終了) AND (既存の終了 > 入力の開始)
            overlapping_bookings = Booking.objects.filter(
                room_id=room_id,
                start_time__lt=end_dt,
                end_time__gt=start_dt
            ).exists()

            if overlapping_bookings:
                return JsonResponse({
                    'status': 'error',
                    'message': '指定された時間帯は既に他の予約が入っています。'
                }, status=400)

            # 6. 保存実行
            booking = Booking.objects.create(
                room_id=room_id,
                user=request.user,
                title=title,
                start_time=start_dt,
                end_time=end_dt
            )

            return JsonResponse({
                'status': 'success',
                'booking_id': booking.id,
                'message': '予約を完了しました！'
            })

        except Exception as e:
            # デバッグ用にコンソールにエラーを表示
            print(f"Booking Error: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f'システムエラーが発生しました: {str(e)}'
            }, status=400)


class BookingEventsListView(View):
    """
    特定の部屋の予約一覧をJSONで返す（FullCalendar用）
    """

    def get(self, request, *args, **kwargs):
        room_id = request.GET.get('room_id')

        if not room_id:
            return JsonResponse([], safe=False)

        # 指定された会議室の予約を取得
        bookings = Booking.objects.filter(room_id=room_id)

        events = []
        for b in bookings:
            # FullCalendarが理解できる形式に変換
            events.append({
                'id': b.id,
                'title': b.title,
                'start': b.start_time.isoformat(),
                'end': b.end_time.isoformat(),
                # 自分の予約かどうかで色を変える（オプション）
                'color': '#0d6efd' if b.user == request.user else '#6c757d',
            })

        return JsonResponse(events, safe=False)

class BookingDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Booking
    success_url = reverse_lazy('accounts:mypage') # 削除後はマイページへ

    def deltete(self, request, *args, **kwargs):
        # 削除成功時にメッセージを表示
        messages.success(self.request, "予約をキャンセルしました。")
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        # ログインユーザーと予約者が一致するかチェック
        booking = self.get_object()
        return self.request.user == booking.user

class ApiDeleteBookingView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, pk, *args, **kwargs):
        try:
            booking = Booking.objects.get(pk=pk)
            booking.delete()
            return JsonResponse({'status': 'success', 'message': '予約をキャンセルしました。'})
        except Booking.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '予約が見つかりませんでした。'}, status=404)

    def test_func(self):
        # 自分の予約のみ削除可能にする
        booking = Booking.objects.get(pk=self.kwargs['pk'])
        return booking.user == self.request.user