from flask import Flask, render_template, request, session, flash
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import yaml
import os

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            form = request.form
            name = form['name']
            age = form['age']
            cur = mysql.connection.cursor()
            name = generate_password_hash(name)
            cur.execute("INSERT INTO employee(name, age) VALUES(%s, %s)", (name, age))
            mysql.connection.commit()
            flash('Successfully inserted data', 'success')
        except:
            flash('Failed to insert data', 'danger')
    return render_template('index.html')

@app.route('/employees')
def employees():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * from employee")
    if result_value > 0:
        all_employees = cur.fetchall()
        return str(check_password_hash(all_employees[3]['name'], 'sunday'))
        #return render_template('employees.html', employees=all_employees)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()
