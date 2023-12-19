from flask import Flask, render_template, flash, request, session, send_file
from flask import render_template, redirect, url_for, request

import mysql.connector
import datetime
import webbrowser

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

app.config['DEBUG']


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/Home")
def Home():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/NewQuery")
def NewQuery():
    return render_template('NewQuery.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1govermentchatdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/QueryInfo")
def QueryInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1govermentchatdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM querytb")
    data = cur.fetchall()
    return render_template('QueryInfo.html', data=data)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1govermentchatdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb")
            data = cur.fetchall()
            return render_template('AdminHome.html', data=data)

        else:
            return render_template('index.html', error=error)


@app.route("/newquery", methods=['GET', 'POST'])
def newquery():
    if request.method == 'POST':
        qtype = request.form['qtype']
        Query = request.form['Query']
        answer = request.form['answer']

        file = request.files['file']
        file.save("static/upload/" + file.filename)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1govermentchatdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO querytb VALUES ('','" + qtype + "','" + Query + "','" + answer + "','" + file.filename + "')")
        conn.commit()
        conn.close()
        # return 'file register successfully'

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1govermentchatdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM querytb  ")
    data = cur.fetchall()
    return render_template('QueryInfo.html', data=data)


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name1 = request.form['name']
        gender1 = request.form['gender']
        Age = request.form['age']
        email = request.form['email']
        pnumber = request.form['phone']
        address = request.form['address']

        uname = request.form['uname']
        password = request.form['psw']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1govermentchatdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('" + name1 + "','" + gender1 + "','" + Age + "','" + email + "','" + pnumber + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        # return 'file register successfully'

    return render_template('UserLogin.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1govermentchatdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            alert = 'Username or Password is wrong'
            return render_template('goback.html', data=alert)
        else:
            print(data[0])
            session['uid'] = data[0]
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1govermentchatdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()
            return render_template('UserHome.html', data=data)


@app.route("/UserHome")
def UserHome():
    pid = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1govermentchatdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where username='" + pid + "'")
    data = cur.fetchall()

    return render_template('UserHome.html', data=data)


@app.route("/ARemove")
def ARemove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1govermentchatdb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from querytb where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('Query  info Remove Successfully!')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1govermentchatdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM querytb  ")
    data = cur.fetchall()
    return render_template('QueryInfo.html', data=data)


@app.route("/Search")
def Search():
    return render_template('Search.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        kword = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1govermentchatdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM querytb where QueryType like '%" + kword + "%' or  Query like '%" + kword + "%'")
        data = cur.fetchall()
        return render_template('Search.html', data=data)


@app.route("/down")
def down():
    id = request.args.get('id')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1govermentchatdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * from querytb where id ='" + str(id) + "'   ")
    data = cursor.fetchone()
    if data is None:

        return 'No file Found!'
    else:
        print(data[4])
        filename = data[4]

        return send_file('static/upload/' + filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
