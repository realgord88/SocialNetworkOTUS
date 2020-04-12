import pymysql.cursors
import config


class Database:
    def __init__(self):
        host = config.mysql_host
        user = config.mysql_user
        password = config.mysql_password
        db = config.mysql_db
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    def add_user(self, username, firstname, lastname, email, gender, city, age, interest, password):
        sql = "INSERT INTO `users` (`username`, `firstname`, `lastname`, `email`, `gender`, `city`, `age`, `interest`, `password`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        self.cur.execute(sql, (username, firstname, lastname, email, gender, city, age, interest, password))
        self.con.commit()

    def check_user_exist(self, username, email):
        sql = "SELECT user_id FROM users WHERE username=%s OR email=%s;"
        self.cur.execute(sql, (username, email))
        return self.cur.fetchone()

    def get_password_hash(self, username):
        sql = "SELECT password FROM users WHERE username=%s;"
        self.cur.execute(sql, username)
        return self.cur.fetchone()

    def get_user(self, username):
        sql = "SELECT username, firstname, lastname, age, city, interest FROM users WHERE username=%s;"
        self.cur.execute(sql, username)
        return self.cur.fetchone()

    def friend_status(self, user_one, user_two):
        sql = "SELECT status, user_one FROM friends WHERE (user_one=%s AND user_two=%s) OR (user_two=%s AND user_one=%s);"
        self.cur.execute(sql, (user_one, user_two, user_one, user_two))
        return self.cur.fetchone()

    def friend_request(self, user_one, user_two):
        sql = "INSERT INTO `friends` (`user_one`, `user_two`, `status`) VALUES (%s, %s, %s);"
        self.cur.execute(sql, (user_one, user_two, 0))
        self.con.commit()

    def get_friend_requests(self, username):
        sql = "SELECT user_one FROM friends WHERE user_two=%s and status=0;"
        self.cur.execute(sql, username)
        return self.cur.fetchall()

    def approved_friend_request(self, user_one, user_two):
        sql = "UPDATE `friends` SET `status`=1 WHERE user_one=%s and user_two=%s;"
        self.cur.execute(sql, (user_one, user_two))
        self.con.commit()

    def skip_friend_request(self, user_one, user_two):
        sql = "DELETE FROM friends WHERE (user_one=%s AND user_two=%s) OR (user_two=%s AND user_one=%s);"
        self.cur.execute(sql, (user_one, user_two, user_one, user_two))
        self.con.commit()

    def get_friend_list(self, username):
        sql = "SELECT REPLACE(CONCAT(user_one,user_two),%s , '') FROM friends WHERE (user_one=%s or user_two=%s) and status=1;"
        self.cur.execute(sql, (username, username, username))
        return self.cur.fetchall()

    def friend_delete(self, user_one, user_two):
        sql = "DELETE FROM friends WHERE (user_one=%s AND user_two=%s) OR (user_two=%s AND user_one=%s);"
        self.cur.execute(sql, (user_one, user_two, user_one, user_two))
        self.con.commit()

    def search_user(self, search_data):
        sql = "SELECT * FROM users WHERE username LIKE %s or firstname LIKE %s or lastname LIKE %s or email LIKE %s or city LIKE %s or interest LIKE %s;"
        self.cur.execute(sql, ("%" + search_data + "%", "%" + search_data + "%", "%" + search_data + "%", "%" + search_data + "%", "%" + search_data + "%", "%" + search_data + "%"))
        return self.cur.fetchall()