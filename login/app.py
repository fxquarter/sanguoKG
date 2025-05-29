from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import MySQLdb
import hashlib
import traceback
import time
from collections import defaultdict

app = Flask(__name__)

# 配置数据库连接信息
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'cancanword'
app.config['MYSQL_PASSWORD'] = '114514'
app.config['MYSQL_DB'] = 'testdb'

mysql = MySQL(app)

# 用于记录每个用户名的登录失败次数及最后一次失败时间
login_failures = defaultdict(lambda: {"count": 0, "last_failed_time": 0})

# 定义最大失败次数和锁定时间（单位：秒）
MAX_FAILURES = 5
LOCK_TIME = 600  # 10分钟


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # 使用单纯的MD5加密输入的密码
    encrypted_password = hashlib.md5(password.encode()).hexdigest()

    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # 检查是否达到失败次数限制且仍在锁定时间内
        if login_failures[username]["count"] >= MAX_FAILURES and \
                time.time() - login_failures[username]["last_failed_time"] < LOCK_TIME:
            return f"尝试过多次数,过段时间再试."

        # 使用参数化查询防止SQL注入，同时直接在查询中比对加密后的密码
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cur.execute(query, (username, encrypted_password))
        user = cur.fetchone()
        if user:
            # 登录成功，重置失败次数记录
            login_failures[username]["count"] = 0
            #成功跳转到目标页面
            return redirect("localhost:5000")
        else:
            # 登录失败，增加失败次数记录并更新最后一次失败时间
            login_failures[username]["count"] += 1
            login_failures[username]["last_failed_time"] = time.time()
            return "Invalid password"
    except Exception as e:
        print("Exception occurred:", traceback.format_exc())
        return "Error during login"
    finally:
        cur.close()


if __name__ == '__main__':
    app.run(debug=True,port=5001)