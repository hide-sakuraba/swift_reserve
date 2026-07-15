# SwiftReserve

会議室の予約状況をカレンダーで確認し、オンラインで予約できる会議室予約アプリです。

ユーザーは会議室の空き時間を確認し、カレンダー上で時間帯を選択して予約できます。予約の重複はサーバー側で検証し、同じ会議室への二重予約を防止します。

## Features

- 会議室の一覧表示
  - 会議室名、定員、所在地、説明、画像を表示
- カレンダーで予約状況を確認
  - 週表示・日表示に対応
  - 表示時間を 8:00〜21:00 に設定
- 会議室予約
  - カレンダー上で時間帯を選択して予約
  - 未ログイン時はログイン画面へ誘導
  - 過去日時・終了時刻が開始時刻以前の予約を防止
  - 同一会議室・時間帯の重複予約を防止
- ユーザー認証
  - 新規登録、ログイン、ログアウト
- マイページ
  - 自分の予約一覧を確認
  - 予約をキャンセル
- 管理画面
  - 会議室・予約情報を管理

## Tech Stack

| Category | Technology |
| --- | --- |
| Backend | Python / Django 5.1 |
| Frontend | HTML / CSS / JavaScript |
| UI Framework | Bootstrap 5 |
| Calendar | FullCalendar 6 |
| Database | PostgreSQL |
| Image Storage | Cloudinary |
| Static File Serving | WhiteNoise |
| Application Server | Gunicorn |

## Architecture

```text
Browser
  │
  ├─ Django Templates + Bootstrap
  ├─ FullCalendar
  │
Django Application
  ├─ accounts: 認証・ユーザー・マイページ
  └─ core: 会議室・予約・予約 API
  │
PostgreSQL
  │
Cloudinary（会議室画像）
```

## Booking Validation

予約作成時、同じ会議室に対して次の条件を満たす予約が存在するかを確認しています。

```text
既存予約の開始時刻 < 新規予約の終了時刻
かつ
既存予約の終了時刻 > 新規予約の開始時刻
```

条件に該当する場合は、予約時間が重複しているため新規予約を作成しません。

## Getting Started

### Prerequisites

- Python 3.12 以降
- PostgreSQL
- Cloudinary アカウント（画像機能を利用する場合）

### Installation

```bash
git clone <repository-url>
cd SwiftReserve

python -m venv .venv
```

仮想環境を有効化します。

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

依存パッケージをインストールします。

```bash
pip install -r requirements.txt
```

### Environment Variables

環境変数を設定します。

```bash
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/swift_reserve
SECRET_KEY=<your-secret-key>
CLOUDINARY_URL=cloudinary://<api_key>:<api_secret>@<cloud_name>
```

PowerShell での設定例:

```powershell
$env:DATABASE_URL = 'postgresql://<user>:<password>@localhost:5432/swift_reserve'
$env:SECRET_KEY = 'your-secret-key'
$env:CLOUDINARY_URL = 'cloudinary://<api_key>:<api_secret>@<cloud_name>'
```

### Database Setup

```bash
python manage.py migrate
python manage.py createsuperuser
```

### Run Development Server

```bash
python manage.py runserver
```

ブラウザで以下にアクセスします。

```text
http://127.0.0.1:8000/
```

管理画面:

```text
http://127.0.0.1:8000/admin/
```

## Project Structure

```text
SwiftReserve/
├── accounts/             # カスタムユーザー、認証、マイページ
├── config/               # Django 設定
├── core/                 # 会議室・予約・API
├── static/               # JavaScript・CSS などの静的ファイル
├── templates/            # Django テンプレート
├── requirements.txt      # 依存パッケージ
└── manage.py
```

## Future Improvements

- 予約内容の編集
- カレンダー画面からの予約キャンセル
- 会議室・設備・空き時間による検索
- 予約通知・リマインドメール
- 予約 API と画面操作に対するテストの追加
- 権限管理の拡充

## License

This project is available for portfolio purposes.
