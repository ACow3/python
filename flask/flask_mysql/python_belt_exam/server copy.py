from flask import Flask, request, redirect, render_template, session, flash
from mysqlconn import connectToMySQL
import re
from flask_bcrypt import Bcrypt

app = Flask(__name__)
# we are creating an object called bcrypt, # which is made by invoking the function Bcrypt with our app as an argument
bcrypt = Bcrypt(app)
app.secret_key = 'This is a secret key'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# render login page
@app.route('/')
def root():
    return render_template('index.html')



# process new registration
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
    mysql = connectToMySQL('wish')
    results = mysql.query_db(query, data)
    print(results)
    


#email validations
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
        mysql = connectToMySQL('wish')
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash
        }
        id = mysql.query_db(query, data)
        print(id)
        session['userid'] = id
        return redirect('/show')



# login route for returning members
@app.route('/member', methods=['POST'])
def member():

    mysql = connectToMySQL('wish')
    query = "SELECT password, id FROM users WHERE email = %(email)s;"
    data = {
        'email': request.form['email'],
    }
    mysql = connectToMySQL('wish')
    results = mysql.query_db(query, data)

    if len(results) > 0:   
        if bcrypt.check_password_hash(results[0]['password'], request.form['password']):
            session['userid'] = results[0]['id']
            return redirect('/wishes')
        else:
            flash("Invalid email or password", 'member')
            return redirect('/')
    else:
        flash("Invalid email or password", 'member')
        return redirect('/')

# route to render first page upon logging in aka the "show" page
@app.route('/wishes')
def show():

    userid = session['userid']
    mysql = connectToMySQL('wish')
    users_query = "SELECT first_name FROM users WHERE id=" +str(userid)
    first_name = mysql.query_db(users_query)


    mysql = connectToMySQL('wish')
    query = "SELECT * FROM wishes WHERE user_id=" +str(session['userid'])
    wishes = mysql.query_db(query)


    # QUERY FOR ITEM_NAMES CURRENT USER WISHED FOR
    userid = session['userid']
    mysql = connectToMySQL('wish')
    wish_list_query = "SELECT item_name FROM wishes WHERE user_id=" +str(userid)
    item_name = mysql.query_db(wish_list_query)


    return render_template('wishes.html', first_name=first_name, item_name=item_name, wishes=wishes)


# route to render page to make new wish
@app.route('/wishes/new')
def wishes_new():

    userid = session['userid']
    mysql = connectToMySQL('wish')
    users_query = "SELECT first_name FROM users WHERE id=" +str(userid)
    first_name = mysql.query_db(users_query)


    return render_template('new.html', first_name=first_name)

# item_name=item_name

# route to send new wish to database
@app.route('/create_process', methods=['POST'])
def make_wish():

    if len(request.form['wish']) < 3:
        flash("A wish must consist of at least 3 characters!", 'wish')

    if len(request.form['description']) < 3:
        flash("A description must be provided!", 'description')
        return redirect('/wishes/new')
    else:
        # Submit new wish
        mysql = connectToMySQL('wish')
        query = "INSERT INTO wishes (item_name, description, user_id, created_at, updated_at) VALUES (%(item_name)s, %(description)s, %(user_id)s, NOW(), NOW());"
        data = {
            'item_name': request.form['wish'],
            'description': request.form['description'],
            'user_id': session['userid']
        }
        mysql.query_db(query, data)
        return redirect('/wishes')



@app.route('/wishes/edit')
def edit():

    userid = session['userid']
    mysql = connectToMySQL('wish')
    users_query = "SELECT first_name FROM users WHERE id=" +str(userid)
    first_name = mysql.query_db(users_query)
    
    mysql = connectToMySQL('wish')
    query = "SELECT * FROM wishes WHERE user_id=" +str(session['userid'])
    wishes = mysql.query_db(query)

    return render_template('edit.html', first_name=first_name, wishes=wishes)


#POST route to update wish
@app.route('/update/<id>', methods=['POST'])
def update(id):

    if len(request.form['wish']) < 3:
        flash("A wish must consist of at least 3 characters!", 'wish')

    if len(request.form['description']) < 3:
        flash("A description must be provided!", 'description')
        return redirect('/wishes/new')
    else:
        mysql = connectToMySQL('wish')
        query = "SET wish.wishes SET item_name = %(item_name)s , description = %(description)s ,created_at = NOW() , updated_at = NOW() WHERE id= %(id)s"
        data = {
            'item_name': request.form['item_name'],
            'description': request.form['description'],
            'id': id
        }
        mysql.query_db(query, data)
        return redirect('/wishes')


@app.route('/delete/<wish_id>')
def remove(wish_id):
    
    mysql = connectToMySQL('wish')
    query = "DELETE FROM wishes WHERE wish_id="+wish_id
    mysql.query_db(query)
    return redirect('/wishes')

    

# logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
