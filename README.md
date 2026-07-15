# SwiftReserve

会議室の空き状況をカレンダーで確認し、そのまま予約できる社内向け会議室予約アプリケーションです。  
直感的な予約体験と、同一会議室の予約重複を防ぐことを目的に制作しました。

## 主な機能

- 会議室一覧の表示（定員・所在地・説明・画像）
- FullCalendar による週／日単位の予約状況表示
- カレンダー上で時間帯を選択して予約を作成
- 同じ会議室・時間帯における予約の重複チェック
- ユーザー登録・ログイン／ログアウト
- マイページで自分の予約を一覧表示・キャンセル
- Django 管理画面からの会議室・予約データ管理

## 画面フロー

```text
会議室一覧 → 会議室詳細（予約カレンダー） → 時間帯選択 → 予約確定
                                      ↑
                         ログイン後に予約可能

マイページ → 自分の予約を確認・キャンセル
```

## 使用技術

| 分類 | 技術 |
| --- | --- |
| バックエンド | Python / Django 5.1 |
| フロントエンド | HTML, CSS, JavaScript, Bootstrap 5 |
| カレンダー UI | FullCalendar 6 |
| データベース | PostgreSQL（本番では `DATABASE_URL` を利用） |
| 画像ストレージ | Cloudinary |
| 静的ファイル配信 | WhiteNoise |
| WSGI サーバー | Gunicorn |

## 工夫した点

### 重複予約を防ぐ処理

予約作成時に、対象会議室で `既存予約の開始 < 新規予約の終了` かつ `既存予約の終了 > 新規予約の開始` となるレコードがあるかを判定しています。時間帯が重なる場合は予約を保存せず、エラーを返します。

### 非同期で予約を反映

予約は JSON を用いて送信し、成功時はページを再読み込みせずカレンダーのイベントを再取得します。操作の流れを止めない UI を目指しました。

### 他ユーザーの予約も分かりやすく表示

カレンダーのイベントは、自分の予約を青、他ユーザーの予約をグレーで返す API を用意し、利用状況を把握しやすくしています。

## セットアップ

### 前提条件

- Python 3.12 以降
- PostgreSQL

### 1. リポジトリを取得して仮想環境を作成

```bash
git clone <repository-url>
cd SwiftReserve
python -m venv .venv
```

Windows（PowerShell）の場合:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS / Linux の場合:

```bash
source .venv/bin/activate
```

### 2. 依存パッケージをインストール

```bash
pip install -r requirements.txt
```

### 3. 環境変数を設定

PostgreSQL の接続先を `DATABASE_URL` に設定します。

```bash
# macOS / Linux の例
export DATABASE_URL='postgresql://<user>:<password>@localhost:5432/swift_reserve'
export SECRET_KEY='<your-secret-key>'
```

PowerShell の例:

```powershell
$env:DATABASE_URL = 'postgresql://<user>:<password>@localhost:5432/swift_reserve'
$env:SECRET_KEY = '<your-secret-key>'
```

会議室画像を Cloudinary で管理する場合は、次の環境変数も設定します。

```bash
export CLOUDINARY_URL='cloudinary://<api_key>:<api_secret>@<cloud_name>'
```

### 4. マイグレーションと管理ユーザー作成

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. 開発サーバーを起動

```bash
python manage.py runserver
```

`http://127.0.0.1:8000/` にアクセスしてください。会議室は `http://127.0.0.1:8000/admin/` から登録できます。

## ディレクトリ構成

```text
.
├── accounts/             # カスタムユーザー、認証、マイページ
├── config/               # Django プロジェクト設定
├── core/                 # 会議室・予約モデル、予約 API、画面ロジック
├── static/               # JavaScript・スタイルなどの静的ファイル
├── templates/            # Django テンプレート
├── requirements.txt      # Python 依存パッケージ
└── manage.py
```

## 今後の改善案

- 予約の編集機能とカレンダー上からのキャンセル
- 会議室名・日付・空き時間による絞り込み
- 会議室設備のタグ付けと検索
- 予約前のリマインド通知
- テストコードの拡充と予約 API のエラーハンドリング強化

## License

このリポジトリはポートフォリオ用途として公開しています。
