from flask import Flask, request, redirect, render_template, session, flash, abort, url_for
from datetime import timedelta
import hashlib
import uuid
import re
import os
from flask_login import login_user, logout_user, login_required, LoginManager

from models import User, Login, Genre





# 定数定義
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
SESSION_DAYS = 30

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days = SESSION_DAYS)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_view'
login_manager.login_message = "ログインが必要です。先にログインしてください。"
@login_manager.user_loader
def load_user(user_id):
          return  Login(user_id)

##ログインしている時だけは入れるページにはこれを書いてください--->@login_required






@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


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
            User.create(user_id, email, password, nickname)
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
        user = User.find_by_email(email)
        if user is None:
            flash('このユーザーは存在しません')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user['password']:
                flash('パスワードが間違っています')
            else:
                user_id = user['user_id']
                login_user(Login(user_id))
                session["user_id"] = user_id
                
                return redirect(url_for('index'))
    
    return redirect(url_for('login_view'))

# ログアウト
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    session.pop('user', None)
    flash('ログアウトしました。')
    return redirect(url_for('login_view'))


#パスワード再設定画面
@app.route('/password_reset', methods=['GET'])
def password_reset_view():
    return render_template('password_reset.html')

#パスワード再設定
@app.route('/password_reset', methods=['POST'])
def password_reset_process():
    email = request.form.get('email')
    new_password = request.form.get('new_password')
    new_password_second = request.form.get('new_password_second')

    if email == '' or new_password == '':
        flash('空欄を埋めてください')
    elif new_password != new_password_second:
        flash('パスワードが一致しません')
    elif re.match(EMAIL_PATTERN, email) is None:
        flash('正しいメールアドレスの形式で入力してください')
    else:
        user = User.find_by_email(email)
        if user is None:
            flash('このメールアドレスは登録されていません')
        else:
            new_hashPassword = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
            User.update_password(user['uid'], new_hashPassword)
            flash('パスワードをリセットしました。ログインしてください')
            return redirect(url_for('login_view'))

    return redirect(url_for('password_reset_view'))



#room作成画面
@app.route('/room-create', methods=['GET'])
def room_create_view():
    return render_template('room-create.html')


# room作成
@app.route('/room-create', methods=['POST'])
def room_create():
    channel_name = request.form.get('channel_name')
    hobby_genre_name = request.form.get('hobby_genre_name')
    channel_comment = request.form.get('comment')
    if channel_name == '' or hobby_genre_name == None :
        flash('空のフォームがあるようです')
    elif len(channel_comment)>50:
        flash('コメントは50文字以内にしてください。')
    else:
       registered_channel_name = Genre.find_by_channel_name(channel_name)
       if registered_channel_name != None:
           flash('既に登録されているようです')
       else:
           if channel_comment == "":
            channel_id = uuid.uuid4() 
            user_id = session["user_id"]
            hobby_id = Genre.find_by_genre_id(hobby_genre_name)
            hobby_genre_id = hobby_id["hobby_genre_id"]
            Genre.create(channel_id, channel_name, user_id , hobby_genre_id)
            return redirect(url_for('room_create_view'))
           else:
            channel_id = uuid.uuid4() 
            user_id = session["user_id"]
            hobby_id = Genre.find_by_genre_id(hobby_genre_name)
            print(hobby_id)
            hobby_genre_id = hobby_id["hobby_genre_id"]
            Genre.create_comment(channel_id, channel_name, channel_comment, user_id , hobby_genre_id)
            return redirect(url_for('room_create_view'))
               
    return redirect(url_for('room_create'))




if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(host='0.0.0.0', debug=True)