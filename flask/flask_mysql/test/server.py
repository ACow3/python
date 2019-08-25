from flask import Flask, request, redirect, render_template, session, flash, jsonify
from mysqlconn import connectToMySQL
import re
from flask_bcrypt import Bcrypt


app = Flask(__name__)
# we are creating an object called bcrypt, # which is made by invoking the function Bcrypt with our app as an argument
bcrypt = Bcrypt(app)
app.secret_key = 'Shhhhhhhhhh'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():

    is_valid = True
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid email address!", 'email')

    query = "SELECT * FROM users WHERE email = %(email)s"
    data = {
        'email': request.form['email']
    }
    mysql = connectToMySQL('ajax_test')
    results = mysql.query_db(query, data)
    print(results)

    if len(results) > 0:
        is_valid = False
        flash("Email already registered", 'email')

    if len(request.form['first_name']) < 1:
        is_valid = False
        flash("Hey! What's your name?", 'first_name')

    if len(request.form['last_name']) < 1:
        is_valid = False
        flash("But we don't even know your last name.", 'last_name')

    if len(request.form['password']) < 8:
        is_valid = False
        flash("Whoa! You can do better than that. Your password needs to be a bit longer.", 'password')

    if not request.form['password'] == request.form['password_confirmation']:
        is_valid = False
        flash("Those don't match bud.", 'password')

    if not is_valid:
        return redirect('/')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        mysql = connectToMySQL('ajax_test')
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash
        }
        id = mysql.query_db(query, data)
        print(id)
        session['id'] = id
        return redirect('/success/' + str(id))


@app.route('/success/<id>')
def success(id):
    mysql = connectToMySQL('ajax_test')
    query = "SELECT * FROM users"
    first_name = mysql.query_db(query)
    flash("You've registered!")
    return render_template('success.html', first_name=first_name)

@app.route('/email', methods=['POST'])
def email():
    print("In email ajax post route.."*80)
    found = False
    mysql = connectToMySQL('ajax_test')
    query = "SELECT email from users WHERE users.email = %(email)s;"
    data = { 'email': request.form['email'] }
    result = mysql.query_db(query, data)
    print('ajax process working')
    if result:
        found = True
    return render_template("email.html", found = found)


@app.route('/member', methods=['POST'])
def member():

    mysql = connectToMySQL('ajax_test')
    query = "SELECT password, id FROM users WHERE email = %(email)s;"
    data = {
        'email': request.form['email'],
    }
    mysql = connectToMySQL('ajax_test')
    results = mysql.query_db(query, data)

    if len(results) > 0:   
        if bcrypt.check_password_hash(results[0]['password'], request.form['password']):
            session['id'] = results[0]['id']
            return redirect('/success/' + str(session['id']))
        else:
            flash("Invalid email or password", 'member')
            return redirect('/')
    else:
        flash("Invalid email or password", 'member')
        return redirect('/')
        


if __name__ == "__main__":
    app.run(debug=True)
