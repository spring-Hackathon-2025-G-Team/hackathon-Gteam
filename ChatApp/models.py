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
                sql = "INSERT INTO users (user_id, email, password, nickname, icon_image_url, favorite, bio) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (user_id, email, password, nickname, '/static/image/icon', '未登録', ''))
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

     @classmethod
     def update_password(cls, user_id, new_hashpassword):
          conn = db_use.get_conn()
          try:
            with conn.cursor() as cursor:
                sql = "UPDATE users SET password = %s WHERE user_id = %s"
                cursor.execute(sql,(new_hashpassword, user_id))
                conn.commit()
          finally:
              db_use.release(conn)

     
     @classmethod
     def get_user_by_id(cls, user_id):
         conn = db_use.get_conn()
         try:
             with conn.cursor() as cursor:
                 sql = "SELECT nickname, icon_image_url, favorite, bio FROM users WHERE user_id = %s"
                 cursor.execute(sql, (user_id,))
                 result = cursor.fetchone()
                 if result is not None:
                     if isinstance(result, dict):
                         return{
                             'nickname': result.get('nickname', ''),
                             'icon_image_url': result.get('icon_image_url', ''),
                             'favorite': result.get('favorite', ''),
                             'bio': result.get('bio', '')
                             }
                     else:
                         return {
                             'nickname': result[0],
                             'icon_image_url': result[1],
                             'favorite': result[2],
                             'bio': result[3]
                         }
                 return None
         finally:
             db_use.release(conn)
 


     @classmethod
     def update_profile(cls, user_id, nickname, icon_image_url, favorite, bio):
         conn = db_use.get_conn()
         try:
            with conn.cursor() as cursor:
                sql = "UPDATE users SET nickname = %s, icon_image_url = %s, favorite = %s, bio = %s WHERE user_id = %s"
                cursor.execute(sql, (nickname, icon_image_url, favorite, bio, user_id))
                conn.commit()
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
                cursor.execute(sql, (channel_id, channel_name, user_id , hobby_genre_id))
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

    @classmethod
    def get_all(cls):
        conn = db_use.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM channels ORDER BY created_at DESC"
                cur.execute(sql)
                channels_list = cur.fetchall()
                return channels_list
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_use.release(conn)

class Search:
     def search_id(self,name):
         conn = db_use.get_conn()
         try:
            with conn.cursor() as cursor:
                sql = "SELECT hobby_genre_id FROM hobby_genres WHERE hobby_genre_name =%s"
                cursor.execute(sql, (name,))
                channel_name = cursor.fetchone()
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
                return  channels
          finally:
              db_use.release(conn)


class  Rank:
    @classmethod
    def channel_name_find(cls,channel_id_dic):
        channel_ids = [item['channel_id'] for item in channel_id_dic]
        conn = db_use.get_conn()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT channel_name FROM channels WHERE channel_id=%s"
                genre_rank_name=[]
                for item in channel_ids:
                    cursor.execute(sql, (item,))
                    genre_rank_name.append(cursor.fetchall())  
                conn.commit()
                return  genre_rank_name
        finally:
              db_use.release(conn)

    @classmethod
    def ranking(cls, rank_genre_id):
        conn = db_use.get_conn()
        channel_id_list =[]
        try:
            with conn.cursor() as cursor:
                sql = "SELECT m.channel_id,COUNT(DISTINCT CONCAT(m.user_id, '-', m.channel_id)) AS genre_count FROM messages m INNER JOIN  channels c ON m.channel_id = c.channel_id INNER JOIN hobby_genres h ON c.hobby_genre_id = h.hobby_genre_id  WHERE h.hobby_genre_id=%s   GROUP BY channel_id ORDER BY genre_count DESC LIMIT 3"
                cursor.execute(sql,(rank_genre_id,))
                channel_id_list = cursor.fetchall() 
                conn.commit()
                return  channel_id_list
        finally:
              db_use.release(conn)

    @classmethod
    def rank_serch_id(cls,name):
         conn = db_use.get_conn()
         try:
            with conn.cursor() as cursor:
                sql = "SELECT hobby_genre_id FROM hobby_genres WHERE hobby_genre_name =%s"
                cursor.execute(sql, (name,))
                channel_name = cursor.fetchone()
                hobby_genre_name = channel_name["hobby_genre_id"]
                conn.commit()
                return hobby_genre_name
         finally:
              db_use.release(conn)


    @classmethod
    def ranking_all(cls):
            conn = db_use.get_conn()
            channel_id_list =[]
            try:
                with conn.cursor() as cursor:
                    sql = "SELECT channel_id,COUNT(DISTINCT CONCAT(user_id, '-', channel_id))  FROM messages GROUP BY channel_id LIMIT 3"
                    cursor.execute(sql)
                    channel_id_list = cursor.fetchall() 
                    conn.commit()
                    return  channel_id_list
            finally:
                db_use.release(conn)

# メッセージクラス（作成、削除、編集、全取得）
class Message:
    @classmethod
    def create(cls, message_id, message_content, channel_id, user_id):
        conn = db_use.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO messages(message_id, message_content, channel_id, user_id) VALUES(%s, %s, %s, %s)"
                cur.execute(sql, (message_id, message_content, channel_id, user_id))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_use.release(conn)

    @classmethod
    def delete(cls, message_id, user_id):
        conn = db_use.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM messages WHERE message_id=%s AND user_id=%s"
                cur.execute(sql, (message_id, user_id))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_use.release(conn)

    @classmethod
    def update_message_content(cls, message_id, new_content):
        try:
            conn = db_use.get_conn()
            with conn.cursor() as cur:
                sql = "UPDATE messages SET message_content=%s WHERE message_id=%s"
                cur.execute(sql, (new_content,message_id))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_use.release(conn)

    @classmethod
    def get_all(cls, channel_id):
        conn = db_use.get_conn()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:
                sql = """
                SELECT messages.message_id, messages.message_content, messages.created_at, messages.channel_id, messages.user_id, users.nickname, users.icon_image_url
                FROM messages
                JOIN users ON messages.user_id = users.user_id
                WHERE messages.channel_id=%s
                ORDER BY created_at ASC
                """
                cur.execute(sql, (channel_id,))
                messages_list = cur.fetchall()
                return messages_list
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_use.release(conn)