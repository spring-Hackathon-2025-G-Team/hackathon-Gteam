from flask import Flask, request, redirect, render_template, session, flash, abort, url_for
from datetime import timedelta
import hashlib
import uuid
import re
import os
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
from flask_paginate import Pagination, get_page_parameter

from models import User, Login, Genre, Search, Rank, Message






# 定数定義
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
PASSWORDS_PATTERN = r"^.{8,16}$"
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
    current_user = Login.get_users(user_id)
    if current_user :
        return  Login(current_user["user_id"])


##ログインしている時だけは入れるページにはこれを書いてください--->@login_required





# 新規登録画面の表示
@app.route('/signup', methods=['GET'])
def signup_view():
    return render_template('signup.html')

# 新規登録
@app.route('/signup', methods=['POST'])
def signup_process():
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
    elif re.match(PASSWORDS_PATTERN, password) is None:
        flash("パスワードは8文字以上16文字以内で入力してください。")
    else:
       user_id = uuid.uuid4() 
       password = hashlib.sha256(password.encode('utf-8')).hexdigest()
       registered_user = User.find_by_email(email)
       if registered_user != None:
           flash('既に登録されているようです')
       else:
            User.create(user_id, email, password, nickname)
            UserId = str(user_id)
            # session['user_id'] = UserId
            return redirect(url_for('login_view'))
    return redirect(url_for('signup_view'))




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
                user_dic = Login.get_users(user_id)
                user_instans = Login(**user_dic)
                login_user(user_instans)               
                return redirect(url_for('index_view'))
    return redirect(url_for('login_view'))


# ログアウト
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    # session.pop('user_id', None)
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
    elif len(new_password) < 8 or len(new_password) > 16:
        flash('パスワードは8～16文字で入力してください')
    elif re.match(EMAIL_PATTERN, email) is None:
        flash('正しいメールアドレスの形式で入力してください')
    else:
        user = User.find_by_email(email)
        if user is None:
            flash('このメールアドレスは登録されていません')
        else:
            new_hashPassword = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
            User.update_password(user['user_id'], new_hashPassword)
            flash('パスワードをリセットしました。ログインしてください')
            return redirect(url_for('login_view'))

    return redirect(url_for('password_reset_view'))


# チャットルーム一覧の表示
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index_view():
    channels = Genre.get_all()
    return render_template('index.html', channels=channels)

# チャット画面の表示
@app.route('/chatroom_screen/<channel_id>', methods=['GET'])
@login_required
def chatroom_screen(channel_id):
    user_id = current_user.id
    messages = Message.get_all(channel_id)
    return render_template('chatroom_screen.html', user_id=user_id, messages=messages, channel_id=channel_id)

# チャット送信
@app.route('/chatroom_screen/<channel_id>', methods=['POST'])
@login_required
def send_message(channel_id):
    message_content = request.form.get('message')
    user_id = current_user.id
    if message_content:
        message_id = str(uuid.uuid4())
        Message.create(message_id, message_content, channel_id, user_id)
    return redirect(url_for('chatroom_screen', channel_id = channel_id))

# チャット削除
@app.route('/chatroom_screen/<channel_id>/<message_id>/delete', methods=['POST'])
@login_required
def delete_message(channel_id, message_id):
    user_id = current_user.id
    if message_id:
        Message.delete(message_id, user_id)
    return redirect(url_for('chatroom_screen', channel_id = channel_id))

# チャット編集
@app.route('/chatroom_screen/<channel_id>/<message_id>/edit', methods=['POST'])
@login_required
def update_message(channel_id, message_id):
    new_content = request.form.get('message')
    if message_id and new_content:
        Message.update_message_content(message_id, new_content)
    return redirect(url_for('chatroom_screen', channel_id = channel_id))

#room作成画面
@app.route('/room_create', methods=['GET'])
@login_required
def room_create_view():

    return render_template('room_create.html')


# room作成
@app.route('/room_create', methods=['POST'])
@login_required
def room_create_process():
    channel_name = request.form.get('channel_name')
    hobby_genre_name = request.form.get('hobby_genre_name')
    channel_comment = request.form.get('comment')
    if channel_name == '' or hobby_genre_name == None :
        flash('空のフォームがあるようです')
        return redirect(url_for('room_create_view'))
    else:
       registered_channel_name = Genre.find_by_channel_name(channel_name)
       if registered_channel_name != None:
           flash('既に登録されているようです')
           return redirect(url_for('room_create_view'))
       else:
           if channel_comment == "":
            channel_id = uuid.uuid4() 
            user_id = current_user.id
            genre_id_dic = Genre.find_by_genre_id(hobby_genre_name)
            hobby_genre_id = genre_id_dic["hobby_genre_id"]
            Genre.create(channel_id, channel_name, user_id , hobby_genre_id)
           else:
            channel_id = uuid.uuid4() 
            user_id = current_user.id
            genre_id_dic = Genre.find_by_genre_id(hobby_genre_name)
            hobby_genre_id = genre_id_dic["hobby_genre_id"]
            Genre.create_comment(channel_id, channel_name, channel_comment, user_id , hobby_genre_id)
    return redirect(url_for('index_view'))

# ジャンル検索画面の表示、ランキング表示画面ランキング表示画面表示
@app.route('/room_search')
@login_required
def room_search_view():
    return render_template('room_search.html')

#ジャンル検索画面,ランキング表示画面
@app.route('/room_search', methods=['POST'])
@login_required
def room_search_process():
    search_genre_name= request.form.get('search_genre_name')
    genre = {
    "all": "すべて",
    "travel": "旅行",
    "eat": "飲食",
    "art": "芸術",
    "study": "学習",
    "movie": "映画",
    "comic": "漫画・アニメ・ゲーム",
    "music": "音楽",
    "idol": "アイドル",
    "muscle": "筋トレ",
    "sports": "スポーツ",
    "sauna": "サウナ",
    "relax": "リラックス",
    "fashion": "ファッション",
    "cosme": "コスメ",
    "pet": "ペット",
    "another": "その他"
}
    genre = genre[search_genre_name]
    if  search_genre_name == None:
        flash('ジャンルを選択してください')
        return render_template('room_search.html')
    elif search_genre_name == "all":
        channels = Search.find_all()
        if channels == ():
            flash("該当するルームがまだありません")
            return render_template('room_search.html')
        else:
             channel_id = Rank.ranking_all()
             genre_rank = Rank.channel_name_find(channel_id)
             return render_template('room_search_result.html', 
                                    channels = channels, 
                                    genre =genre , 
                                    content_type='text/html; charset=utf-8', 
                                    genre_rank = genre_rank)

    else:
            channels = Search.find_by_search(search_genre_name)
            if channels == ():
                flash("該当するルームがまだありません")
                return render_template('room_search.html')
            else: 
                rank_genre_id_dic = Rank.rank_serch_id(search_genre_name)
                channel_id = Rank.ranking(rank_genre_id_dic)
                genre_rank = Rank.channel_name_find(channel_id)
                return render_template('room_search_result.html', 
                                        channels = channels, 
                                        genre =genre , 
                                        content_type='text/html; charset=utf-8', 
                                       genre_rank = genre_rank)

# ジャンル検索結果画面の表示
@app.route('/room_search_result', methods=['GET'])
@login_required
def room_search_result():
    genre = request.args.get('genre')
    return render_template('room_search_result.html', genre=genre)

# プロフィール画面の表示

@app.route('/profile')
@login_required
def profile_view():
    user_id = current_user.id
    return render_template('profile.html', user_id=user_id)


# プロフィール編集画面の表示

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile_view():
    user_id = current_user.id

    if not user_id:
            flash('ログインしてください')
            return redirect(url_for('login_view'))

    if request.method == 'POST':
        nickname = request.form.get('nickname')
        icon_image_url = request.form.get('icon_image_url')
        favorite = request.form.get('favorite')
        bio = request.form.get('bio')

        if not favorite:
            flash('趣味を入力してください')
            return redirect(url_for('edit_profile_view'))
        
        elif len(bio) > 200:
            flash('ひとことコメントは200字以内で入力してください')
            return redirect(url_for('edit_profile_view'))
        
        User.update_profile(user_id, nickname, icon_image_url, favorite, bio)
        flash('プロフィールを更新しました')
        return redirect(url_for('profile_view'))
    return render_template('edit_profile.html', user_id=user_id)




if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(host='0.0.0.0', debug=True)