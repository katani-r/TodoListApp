from datetime import datetime
from flask import render_template, redirect, url_for, request, flash, abort, jsonify
from werkzeug.security import generate_password_hash
from app import app, db, photos
from app.models import Task, User, Category
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from flask_uploads import UploadNotAllowed
from app.forms import CategoryForm
import os

def delete_old_image(filename):
    if filename != "default_image.png":
        file_path = os.path.join(app.config['UPLOADED_IMAGES_DEST'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)

@app.route('/')
@app.route('/index')
@login_required
def index():
    # ソートのパラメータを取得
    sort = request.args.get('sort', 'order')
    order = request.args.get('order', 'asc')

    # タスクのクエリを作成
    query = Task.query.filter_by(user_id=current_user.id)
    if sort != 'order':
        if order == 'desc':
            query = query.order_by(Task.__table__.c[sort].desc(), Task.order)
        else:
            query = query.order_by(Task.__table__.c[sort], Task.order)
    else:
        query = query.order_by(Task.order.desc()) if order == 'desc' else query.order_by(Task.order)

    # カテゴリーを取得
    categories = Category.query.filter_by(user_id=current_user.id).all()

    # ソートされたタスクを取得
    tasks = query.all()

    # タスクとカテゴリーをテンプレートに渡す
    return render_template('index.html', tasks=tasks, categories=categories)


@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title')
    description = request.form.get('description')
    due_date_str = request.form.get('due_date')
    priority = request.form.get('priority')
    category = request.form.get('category')

    due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None

    # 新規タスクのorder値を0に設定（リストの最上部に追加）
    new_order = 0

    # タスクを現在のユーザーに関連付け、新しいorder値を設定
    task = Task(title=title, description=description, due_date=due_date, priority=priority, category=category, user_id=current_user.id, order=new_order)
    db.session.add(task)
    db.session.commit()

    # 既存のタスクのorder値を更新して新規タスクに対応
    Task.query.filter(Task.id != task.id).update({"order": Task.order + 1})
    db.session.commit()

    flash('タスクを追加しました。')
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
@login_required
def delete(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        flash('タスクを削除しました。')
    return redirect(url_for('index'))
 
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit(task_id):
    task = Task.query.get(task_id)
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None
        task.priority = request.form.get('priority')
        task.category = request.form.get('category')
        db.session.commit()
        flash('タスクを更新しました。')
        return redirect(url_for('index'))
    return render_template('edit_task.html', task=task)

@app.route('/toggle_status/<int:task_id>')
@login_required
def toggle_status(task_id):
    task = Task.query.get(task_id)
    if task:
        task.status = '完了' if task.status == '未完了' else '未完了'
        db.session.commit()
        flash('タスクのステータスを更新しました。')
    return redirect(url_for('index'))

@app.route('/task/<int:task_id>')
@login_required
def task_detail(task_id):
    task = Task.query.get(task_id)
    if not task:
        abort(404)  # Not Found
    return render_template('task_detail.html', task=task)

@app.route('/category/add', methods=['POST'])
@login_required
def add_category():
    data = request.get_json()
    category_name = data.get('category_name').strip()  # .strip() で余分な空白を削除

    if not category_name:
        return jsonify({'message': 'カテゴリ名は空にできません。'}), 400

    existing_category = Category.query.filter_by(name=category_name, user_id=current_user.id).first()
    if existing_category:
        return jsonify({'message': '同じ名前のカテゴリがすでに存在します。'}), 400

    new_category = Category(name=category_name, user_id=current_user.id)
    db.session.add(new_category)
    db.session.commit()

    return jsonify({
        'message': 'カテゴリが正常に追加されました。',
        'category_id': new_category.id,
        'category_name': new_category.name
    }), 200


@app.route('/category/delete/<int:category_id>', methods=['DELETE'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.user_id != current_user.id:
        abort(403)  # Forbidden

    db.session.delete(category)
    db.session.commit()

    # JSONレスポンスを返す
    return jsonify({'message': 'カテゴリが削除されました。'}), 200

@app.route('/category/list', methods=['GET'])
@login_required
def list_categories():
    categories = Category.query.filter_by(user_id=current_user.id).all()
    category_list = [{'id': cat.id, 'name': cat.name} for cat in categories]
    return jsonify({'categories': category_list})


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email') or None  # 空の場合は None を設定
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        # ユーザー名の重複を確認
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('そのユーザー名は既に使用されています。', 'danger')
            return render_template('register.html')

        if password != password_confirm:
            # パスワードが一致しない場合のメッセージ
            flash('パスワードが一致しません!', 'danger')
            return render_template('register.html')

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        # 新しいユーザーのデフォルトカテゴリを作成
        create_default_categories(new_user)

        # 登録完了メッセージ
        flash('登録が完了しました!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

def create_default_categories(user):
    default_categories = ['仕事', '私用']
    for category_name in default_categories:
        category = Category(name=category_name, user=user)
        db.session.add(category)
    db.session.commit()




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))

        flash('ユーザー名またはパスワードが間違っています。', 'danger')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました。', 'success')
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    email = current_user.email if current_user.email else "未登録"
    
    if request.method == 'POST':
        if 'photo' in request.files:
            try:
                old_filename = current_user.profile_image  
                filename = photos.save(request.files['photo'], name=secure_filename(request.files['photo'].filename))
                current_user.profile_image = filename
                db.session.commit()
                delete_old_image(old_filename)
                flash('画像が正常に更新されました', 'success')
                return redirect(url_for('profile'))
            except UploadNotAllowed:
                flash('アップロードされたファイルのタイプは許可されていません', 'danger')
                return redirect(url_for('profile'))

    image_file = url_for('static', filename='uploads/photos/' + current_user.profile_image) if current_user.profile_image and current_user.profile_image != "default_image.png" else url_for('static', filename='images/default_image.png')
    return render_template('profile.html', user=current_user, email=email, image_file=image_file)



@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        # None または 'None' の場合は None を設定
        email = None if email == '' or email.lower() == 'none' else email

        # ユーザー名の重複チェック
        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != current_user.id:
            flash('このユーザー名は既に使用されています。別のユーザー名を選択してください。', 'danger')
            return redirect(url_for('edit_profile'))

        current_user.username = username
        current_user.email = email
        db.session.commit()
        flash('プロフィールを更新しました。', 'success')
        return redirect(url_for('profile'))
    
    return render_template('edit_profile.html', user=current_user)


@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    # ユーザーに関連するタスクを削除
    Task.query.filter_by(user_id=current_user.id).delete()
    # ユーザーに紐づくカテゴリを削除
    Category.query.filter_by(user_id=current_user.id).delete()

    # ユーザーを削除
    db.session.delete(current_user)
    db.session.commit()

    flash('アカウントを削除しました。')
    return redirect(url_for('logout'))

@app.route('/delete_image')
@login_required
def delete_image():
    delete_old_image(current_user.profile_image)
    current_user.profile_image = 'default_image.png'
    db.session.commit()
    return redirect(url_for('profile'))

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    # 権限チェック: 管理者のみが他のユーザーを削除できる
    if not current_user.is_admin:
        flash('この操作を行う権限がありません。', 'danger')
        return redirect(url_for('index'))

    # 削除するユーザーを取得
    user_to_delete = User.query.get_or_404(user_id)
    if user_to_delete == current_user:
        flash('自分自身のアカウントはこの方法では削除できません。', 'danger')
        return redirect(url_for('index'))

    # ユーザーに関連するタスクとカテゴリを削除
    Task.query.filter_by(user_id=user_to_delete.id).delete()
    Category.query.filter_by(user_id=user_to_delete.id).delete()

    # ユーザーを削除
    db.session.delete(user_to_delete)
    db.session.commit()

    flash('ユーザーが削除されました。', 'success')
    return redirect(url_for('logout'))


@app.route('/change_password', methods=['POST'])
@login_required  # このデコレータは、ログインユーザーのみがアクセスできることを確保するためのものです。
def change_password():
    # フォームから送信されたデータを取得
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    # 現在のパスワードが正しいか確認
    if not current_user.check_password(current_password):
        flash('現在のパスワードが間違っています。', 'danger')
        return redirect(url_for('profile'))

    # 新しいパスワードと確認用のパスワードが一致しているか確認
    if new_password != confirm_password:
        flash('新しいパスワードと確認用のパスワードが一致しません。', 'danger')
        return redirect(url_for('profile'))

    # パスワードを更新
    current_user.set_password(new_password)
    db.session.commit()

    flash('パスワードが変更されました。', 'success')
    return redirect(url_for('profile'))

@app.route('/update_order', methods=['POST'])
@login_required
def update_order():
    data = request.get_json()
    task_order = data['order']

    # タスクの新しい順序に基づいて更新
    for i, task_id in enumerate(task_order):
        task = Task.query.get(int(task_id))
        if task and task.user_id == current_user.id:  # 現在のユーザーに属するタスクのみを更新
            task.order = i
            db.session.commit()

    return jsonify({'status': 'success'})

