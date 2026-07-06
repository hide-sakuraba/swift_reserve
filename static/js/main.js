// 1. CSRFトークンを取得する関数を定義（再利用しやすくするため）
function getCsrfToken() {
    const metaTag = document.querySelector('meta[name="csrf-token"]');
    return metaTag ? metaTag.getAttribute('content') : '';
}

// 2. 予約データを送信する関数（例）
async function createBooking(bookingData) {
    try {
        const response = await fetch('/core/booking/create/', { // URLは適宜合わせてください
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken() // ここでトークンを取得してセット
            },
            body: JSON.stringify(bookingData)
        });

        const data = await response.json();
        if (data.status === 'success') {
            alert('予約が完了しました！');
            location.reload(); // 画面を更新
        } else {
            alert('エラー: ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('通信エラーが発生しました。');
    }
}

// ... (前略: getCsrfToken関数などはそのまま) ...

function initCalendar() {
    const calendarEl = document.getElementById('calendar');
    const roomId = document.getElementById('roomId')?.value;
    if (!calendarEl || !roomId) return;

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        locale: 'ja',
        selectable: true,
        allDaySlot: false,
        events: `/core/api/bookings/?room_id=${roomId}`,

        // --- 新規予約（範囲選択） ---
        select: function(info) {
            const bookingModal = new bootstrap.Modal(document.getElementById('bookingModal'));
            document.getElementById('bookingModalLabel').innerText = "新規予約";
            document.getElementById('title').value = "";
            document.getElementById('start_display').value = info.startStr.replace('T', ' ').substring(0, 16);
            document.getElementById('end_display').value = info.endStr.replace('T', ' ').substring(0, 16);

            const saveBtn = document.getElementById('saveBooking');
            saveBtn.style.display = "block"; // 保存ボタンを表示

            // 削除ボタンがあれば隠す
            let delBtn = document.getElementById('deleteBooking');
            if (delBtn) delBtn.style.display = "none";

            saveBtn.onclick = async function() {
                // ... (既存の保存処理) ...
                const title = document.getElementById('title').value;
                const response = await fetch('/core/booking/create/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
                    body: JSON.stringify({ room_id: roomId, title: title, start: info.startStr, end: info.endStr })
                });
                const data = await response.json();
                if (data.status === 'success') {
                    bookingModal.hide();
                    calendar.refetchEvents();
                } else { alert(data.message); }
            };
            bookingModal.show();
        },

        // --- 既存予約のクリック（詳細・キャンセル） ---
        eventClick: function(info) {
            // 他人の予約（色がグレーなど）の場合は何もしない、または閲覧のみ
            if (info.event.backgroundColor === '#6c757d') {
                alert("他の方の予約です。");
                return;
            }

            const bookingModal = new bootstrap.Modal(document.getElementById('bookingModal'));
            document.getElementById('bookingModalLabel').innerText = "予約の確認・キャンセル";
            document.getElementById('title').value = info.event.title;
            document.getElementById('start_display').value = info.event.startStr.replace('T', ' ').substring(0, 16);
            document.getElementById('end_display').value = info.event.endStr.replace('T', ' ').substring(0, 16);

            // 保存ボタンを隠し、削除ボタンを表示
            document.getElementById('saveBooking').style.display = "none";
            let delBtn = document.getElementById('deleteBooking');

            // モーダル内に削除ボタンがなければ作成（あるいは最初からHTMLに隠しておいてもOK）
            if (!delBtn) {
                const footer = document.querySelector('.modal-footer');
                delBtn = document.createElement('button');
                delBtn.id = 'deleteBooking';
                delBtn.className = 'btn btn-danger';
                delBtn.innerText = '予約をキャンセルする';
                footer.appendChild(delBtn);
            }
            delBtn.style.display = "block";

            delBtn.onclick = async function() {
                if (!confirm("この予約をキャンセルしてもよろしいですか？")) return;

                const response = await fetch(`/core/api/booking/${info.event.id}/delete/`, {
                    method: 'POST', // Djangoの仕様上POST推奨
                    headers: { 'X-CSRFToken': getCsrfToken() }
                });

                const data = await response.json();
                if (data.status === 'success') {
                    bookingModal.hide();
                    calendar.refetchEvents();
                } else {
                    alert(data.message);
                }
            };

            bookingModal.show();
        }
    });

    calendar.render();
}
