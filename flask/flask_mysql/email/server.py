from flask import Flask, redirect, request, render_template, session, flash
from mysqlconn import connectToMySQL
import re

app = Flask(__name__)
app.secret_key = 'Secret mfn key'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def root():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():

    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email address!")

        return redirect('/')
    else:
        mysql = connectToMySQL('email')
        query = "INSERT INTO users (email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW());"
        data = {
            'email': request.form['email']
        }
        users=mysql.query_db(query, data)
        print(users)
        return redirect('/success')
    

@app.route('/success')
def success():
    mysql = connectToMySQL("email")
    query = "SELECT * FROM users;"
    email = mysql.query_db(query)
    flash("You've registered!")
    return render_template('success.html', email=email)


if __name__=="__main__":
    app.run(debug=True)