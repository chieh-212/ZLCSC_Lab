from flask import Flask, render_template, request, redirect
import os
import pymysql

db_settings ={
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'your_password',
    'db': 'login',
    'charset': 'utf8'
}

def connect_db():
    connection = pymysql.connect(**db_settings)
    return connection

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    username = None
    password = None
    message = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'")
            result = cursor.fetchone()
            connection.close()
            if username == 'admin' and result:
                    message = "ZLCSC{????h0w_u_Log1n_As_Adm1nistrAt0r????}"
            elif result:
                    message = "Login Successful!! But U R Not Admin..."
            else:
                message = "fail."
    return render_template('index.html', username=username, password=password, message=message)

if __name__ == '__main__':
    app.run(debug=True)