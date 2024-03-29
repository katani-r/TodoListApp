

# TodoListApp
このリポジトリは、私の初めてのプログラミングプロジェクトです。PythonとFlaskを使用して基本的なTodoリストアプリを作成しました。シンプルなUIでタスク管理を実現。初心者としての学習過程を通じて作られた、基本的なWebアプリケーションです。

### アプリケーション概要
ToDoリストアプリケーションは、ユーザーが日々のタスクを管理できるウェブベースのアプリケーションです。ユーザーはタスクの追加、編集、削除、およびカテゴリ別の整理ができ、各タスクには期限日、優先度、状態（未完了/完了）を設定することができます。また、ユーザーは自身のプロフィールを管理し、プロフィール画像をアップロードすることも可能です。

### 技術スタック
- **プログラミング言語:** Python
- **フレームワーク:** Flask（バージョン2.0.2）
- **データベース:** SQLAlchemy（バージョン2.5.1）、Flask-Migrate（バージョン4.0.5）を使用してSQLiteデータベースを操作
- **フロントエンド:** HTML, CSS, JavaScript
- **フォーム処理:** WTForms（バージョン3.1.0）
- **ユーザー認証:** Flask-Login（バージョン0.6.2）
- **画像アップロード:** Flask-Reuploaded（バージョン1.4.0）

### セットアップ手順

1. **環境準備:** Python 3.8 以上をインストールしてください。
2. **リポジトリのクローン:** GitHubからアプリケーションのリポジトリをクローンします。
3. **仮想環境のセットアップ:** プロジェクトディレクトリ内でPythonの仮想環境を作成し、アクティベートします。
   - 仮想環境作成コマンド：  
     `python -m venv venv`
   - 仮想環境をアクティベート（Windowsの場合）：  
     `venv\Scripts\activate`
   - 仮想環境をアクティベート（macOS/Linuxの場合）：  
     `source venv/bin/activate`
4. **依存関係のインストール:** `requirements.txt`ファイルを使用して必要なパッケージをインストールします。
   - コマンド：  
     `pip install -r requirements.txt`
5. **データベースの設定:** Flask-Migrateを使用してデータベースを初期化します。
   - コマンド：  
     ```
     flask db init
     flask db migrate
     flask db upgrade
     ```
6. **アプリケーションの実行:** コマンドラインで以下のコマンドを実行し、ローカルサーバーを起動します。
   - コマンド：  
     `flask run`
7. **ブラウザでのアクセス:** http://127.0.0.1:5000/ にアクセスしてアプリケーションを使用します。

### 機能の説明  
- **タスク管理:** ユーザーはタスクを追加、編集、削除できます。各タスクにはタイトル、説明、期限、優先度、カテゴリを設定できます。  
- **カテゴリ管理:** タスクをカテゴリ別に整理できます。新しいカテゴリの追加や既存のカテゴリの削除も可能です。  
- **ユーザー認証:** ユーザー登録、ログイン、ログアウト機能があります。セキュアな認証システムを通じてユーザー情報を保護します。  
- **プロフィール管理:** ユーザーは自身のプロフィール情報を編集し、プロフィール画像をアップロードできます。  

### データベーススキーマ  
ToDoリストアプリケーションのデータベースは以下の主要なモデルを含みます。  
- **User:** ユーザー情報を格納するモデル。ユーザー名、メールアドレス、パスワード（ハッシュ化）、プロフィール画像を含みます。  
- **Task:** タスク情報を格納するモデル。タイトル、説明、作成日、期限日、優先度、カテゴリ、ステータス（未完了/完了）、ユーザーIDを含みます。  
- **Category:** カテゴリ情報を格納するモデル。カテゴリ名とユーザーIDを含みます。  

### UI/UXデザイン  
- **レイアウト:** クリーンで直感的なレイアウト。ナビゲーションバーにはアプリケーションタイトルとユーザー関連オプションが配置されています。サイドバーにはカテゴリ管理のオプションがあります。  
- **スタイリング:** BootstrapとカスタムCSSを使用してスタイリッシュなデザインが施されています。フォーム、ボタン、テーブルなどの要素に一貫性のあるスタイルが適用されています。  
- **インタラクティビティ:** JavaScriptを使用した動的な要素（タスクのドラッグアンドドロップ、モーダルウィンドウ、アラートメッセージ）が組み込まれています。  


### コードの説明  
- **models.py:** データモデルの定義。User、Task、Categoryモデルがあり、SQLAlchemyを使用して関連付けられています。  
- **forms.py:** WTFormsを使用してフォームクラスを定義。ユーザー登録、ログイン、タスク編集などのフォームが含まれます。  
- **routes.py:** Flaskのルーティングとビュー関数。タスクの追加、編集、削除、カテゴリ管理、ユーザー認証関連のルートが定義されています。  
- **__init__.py:** Flaskアプリケーションの作成と設定。データベースと認証システムの初期化もここで行われます。  
- **HTML/CSS/JSファイル:** ユーザーインターフェースの構築とスタイリング。Bootstrapをベースにしており、scripts.js でインタラクティブな要素（ドラッグアンドドロップ、モーダルウィンドウ）を管理しています。  
