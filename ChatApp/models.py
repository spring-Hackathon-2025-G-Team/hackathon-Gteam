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

   

   



   
    

#chnnel
# class Channel:
#     @classmethod
#     def create():
#         return

  




 