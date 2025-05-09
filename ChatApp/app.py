from flask import Flask, request, redirect, render_template, session, flash, abort, url_for
from datetime import timedelta
import hashlib
import uuid
import re
import os

from models import User

# 定数定義
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
SESSION_DAYS = 30

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days = SESSION_DAYS)


@app.route('/')
def hello():
    return 'こんにちは！'

# 新規登録画面の表示
@app.route('/signup', methods=['GET'])
def signup_view():
    return render_template('signup.html')

# 新規登録
@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    password_second = request.form.get('password_second')
    nickname = request.form.get('nickname')
    icon = request.form.get('icon')
    if email == '' or password == '' or password_second == '' or nickname == "":
        flash('空のフォームがあるようです')
    elif password != password_second:
        flash('二つのパスワードの値が間違っています')
    elif re.match(EMAIL_PATTERN, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
       user_id = uuid.uuid4() 
       password = hashlib.sha256(password.encode('utf-8')).hexdigest()
       registered_user = User.find_by_email(email)
       if registered_user != None:
           flash('既に登録されているようです')
       else:
            User.create(user_id, email, password, nickname, icon)
            UserId = str(user_id)
            session['user_id'] = UserId
            return redirect(url_for('login_view'))
    return redirect(url_for('signup'))





# ログインページの表示
@app.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')

# ログイン処理
@app.route('/login', methods=['POST'])
def login_process():
    email = request.form.get('email')
    password = request.form.get('password')

    if email == '' or password == '':
        flash('空のフォームがあるようです')
    else:
        user= User.find_by_email(email)
        if user is None:
            flash('このユーザーは存在しません')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user['password']:
                flash('パスワードが間違っています')
            else:
                session['uid'] = user['uid']
                return redirect(url_for('channels_view'))
    return redirect(url_for('login_view'))

# ログアウト
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('login_view'))



if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(host='0.0.0.0', port=5000, debug=True)