from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models import Task
from datetime import datetime
from flask import abort


@app.route('/')
@app.route('/index')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    description = request.form.get('description')
    due_date_str = request.form.get('due_date')
    priority = request.form.get('priority')
    category = request.form.get('category')

    due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None

    task = Task(title=title, description=description, due_date=due_date, priority=priority, category=category)
    db.session.add(task)
    db.session.commit()

    flash('タスクを追加しました。')
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        flash('タスクを削除しました。')
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
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
def toggle_status(task_id):
    task = Task.query.get(task_id)
    if task:
        task.status = '完了' if task.status == '未完了' else '未完了'
        db.session.commit()
        flash('タスクのステータスを更新しました。')
    return redirect(url_for('index'))

@app.route('/task/<int:task_id>')
def task_detail(task_id):
    task = Task.query.get(task_id)
    if not task:
        abort(404)  # Not Found
    return render_template('task_detail.html', task=task)
