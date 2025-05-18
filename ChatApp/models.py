from flask import abort
import pymysql
from flask_login import UserMixin, LoginManager
from util.DB import DB


db_use = DB.init_pool()






class User:
     @classmethod
     def create(cls, user_id, email, password, nickname):
          conn = db_use.get_conn()
          try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO users (user_id, email, password, nickname) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (user_id, email, password, nickname))
                conn.commit()
          finally:
              db_use.release(conn)
               
                    
     @classmethod
     def find_by_email(cls, email):
          conn = db_use.get_conn()
          try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM users WHERE email=%s"
                cursor.execute(sql, (email,))
                user = cursor.fetchone()
                return user
          finally:
                db_use.release(conn)
                        

class Login(UserMixin):
    def __init__(self, user_id):
        self.user_id = user_id
        conn = db_use.get_conn()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM users WHERE user_id = %s"
                cursor.execute(sql, (user_id,))
                user = cursor.fetchone()

                if user:
                    self.email = user['email']
                else:
                    self.email = None
        finally:
            db_use.release(conn)

    def get_id(self):
        return str(self.user_id)

   

class Genre:
     @classmethod
     def create(cls, channel_id, channel_name, user_id , hobby_genre_id):
          conn = db_use.get_conn()
          try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO channels (channel_id, channel_name, user_id , hobby_genre_id) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (user_id, channel_id, channel_name, user_id , hobby_genre_id))
                conn.commit()
          finally:
              db_use.release(conn)
               
     @classmethod
     def create_comment(cls, channel_id, channel_name, channel_comment, user_id , hobby_genre_id):
          conn = db_use.get_conn()
          try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO channels (channel_id, channel_name, channel_comment, user_id , hobby_genre_id) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (channel_id, channel_name, channel_comment, user_id , hobby_genre_id))
                conn.commit()
          finally:
              db_use.release(conn)

    # チャットルームの全取得
    @classmethod
    def get_all(cls):
        conn = db_use.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM channels ORDER BY created_at DESC;"
                cur.execute(sql)
                channels_list = cur.fetchall()
                return channels_list
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_use.release(conn)


# sql = "SELECT user_id FROM user WHERE username = ?"
#     cursor.execute(sql, (username,))

     def name():
        return ""
    
     @classmethod
     def find_by_genre_id(cls,genrename):
          conn = db_use.get_conn()
          try:
            with conn.cursor() as cursor:
                sql = "SELECT hobby_genre_id FROM hobby_genres WHERE hobby_genre_name = %s"
                cursor.execute(sql, (genrename,))
                hobby_genre_id = cursor.fetchone()
                print(hobby_genre_id)
                return hobby_genre_id
          finally:
                db_use.release(conn)

     @classmethod
     def find_by_channel_name(cls, channel_name):
          conn = db_use.get_conn()
          try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM channels WHERE channel_name=%s"
                cursor.execute(sql, (channel_name,))
                channel_name = cursor.fetchone()
                return channel_name
          finally:
                db_use.release(conn)

