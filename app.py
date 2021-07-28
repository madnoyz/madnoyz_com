import os
from flask import Flask, render_template, flash, session, request, redirect
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import yaml


app = Flask(__name__)
Bootstrap(app)

#configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blogs/<int:id>/')
def blogs(id):
    return render_template('blogs.html', blog_id=id)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        userDetails = request.form
        if(userDetails['password']) != userDetails['confirm_password']:
            flash("Passwords do not match! Try again.", 'danger')
            return render_template('register.html')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user(first_name, last_name, username, email, password)"
                    "VALUES(%s,%s,%s,%s,%s)", (userDetails['first_name'], userDetails['last_name'],
                    userDetails['username'], userDetails['email'], generate_password_hash(userDetails['password'])))
        mysql.connection.commit()
        cur.close()
        flash('Registration successful! Please login.', 'success')
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM user WHERE username = %s", ([username]))
        if resultValue > 0:
            user = cur.fetchone()
            if check_password_hash(user['password'], userDetails['password']):
                session['login'] = True
                session['firstName'] = user['first_name']
                session['lastName'] = user['last_name']
                flash("Welcome " + session['firstName'] + '! You have successfully logged in.', 'success')
            else:
                cur.close()
                flash("Password does not match.", 'danger')
                return render_template('login.html')
        else:
            cur.close()
            flash('User not found', 'danger')
            return render_template('login.html')
        cur.close()
        return redirect('/')
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/my-blogs')
def my_blogs():
    return render_template('my-blogs.html')

@app.route('/write-blog/', methods=['GET','POST'])
def write_blog():
    return render_template('write-blog.html')

@app.route('/edit-blog/<int:id>/', methods=['GET', 'POST'])
def edit_blog():
    return render_template('edit-blog.html', blog_id=id)

@app.route('/delete-blog/<int:id>/', methods=['POST'])
def delete_blog():
    return 'success'

if __name__ == '__main__':
    app.run()
