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
               
    
     @classmethod
     def find_by_genre_id(cls,genrename):
          conn = db_use.get_conn()
          try:
            with conn.cursor() as cursor:
                sql = "SELECT hobby_genre_id FROM hobby_genres WHERE hobby_genre_name = %s"
                cursor.execute(sql, (genrename,))
                hobby_genre_id = cursor.fetchone()
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

class Search:
     def search_id(self,name):
         conn = db_use.get_conn()
         print(name)
         try:
            with conn.cursor() as cursor:
                sql = "SELECT hobby_genre_id FROM hobby_genres WHERE hobby_genre_name =%s"
                cursor.execute(sql, (name,))
                channel_name = cursor.fetchone()
                print(channel_name)
                hobby_genre_name = channel_name["hobby_genre_id"]
                conn.commit()
                return hobby_genre_name
         finally:
              db_use.release(conn)

     @classmethod
     def find_by_search(self, search_genre_name):
          hobby_genre_name = self.search_id(self, search_genre_name)
          conn = db_use.get_conn()
          try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM channels WHERE hobby_genre_id=%s"
                cursor.execute(sql, (hobby_genre_name,))
                channels =cursor.fetchall()
                conn.commit()
                print(channels)
                return channels
          finally:
              db_use.release(conn)

     @classmethod
     def find_all(cls):
          conn = db_use.get_conn()
          try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM channels"
                cursor.execute(sql)
                channels = cursor.fetchall()
                conn.commit()
                print(channels)
                return  channels
          finally:
              db_use.release(conn)