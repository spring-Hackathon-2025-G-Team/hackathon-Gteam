import pymysql




from util.DB import DB


db_use = DB.init_pool()






class User:
     @classmethod
     def create(cls, user_id, email, password, nickname, icon_image_url):
          conn = db_use.get_conn()
          try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO users (user_id, email, password, nickname,  icon_image_url) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (user_id, email, password, nickname, icon_image_url))
                conn.commit()
          finally:
               conn.close()
                    
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
               conn.close()
     
     @classmethod
     def update_password(cls, uid, new_hashPassword):
         conn = db_use.get_conn()
         try:
           with conn.cursor() as cursor:
                 sql = "UPDATE users SET password = %s WHERE uid = %s"
                 cursor.execute(sql, (new_hashPassword, uid))
                 conn.commit()
         finally:
               db_use.release(conn)
