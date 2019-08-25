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
    mysql = connectToMySQL('trips')
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
        mysql = connectToMySQL('trips')
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
        return redirect('/dashboard')


# login route for returning members
@app.route('/member', methods=['POST'])
def member():

    mysql = connectToMySQL('trips')
    query = "SELECT password, id FROM users WHERE email = %(email)s;"
    data = {
        'email': request.form['email'],
    }
    mysql = connectToMySQL('trips')
    results = mysql.query_db(query, data)

    if len(results) > 0:   
        if bcrypt.check_password_hash(results[0]['password'], request.form['password']):
            session['userid'] = results[0]['id']
            return redirect('/dashboard')
        else:
            flash("Invalid email or password", 'member')
            return redirect('/')
    else:
        flash("Invalid email or password", 'member')
        return redirect('/')

# route to render first page upon logging in "show" page / "dashboard" page
@app.route('/dashboard')
def show():

    userid = session['userid']
    mysql = connectToMySQL('trips')
    query = "SELECT first_name FROM users WHERE id=" +str(userid)
    first_name = mysql.query_db(query)
    
    mysql = connectToMySQL('trips')
    trips_query = "SELECT * FROM trips WHERE users_id=" +str(session['userid'])
    trips = mysql.query_db(trips_query)

    return render_template('show.html', first_name=first_name, trips=trips)

# route to render new page to create new trips
@app.route('/trips/new')
def new_trips():

    userid = session['userid']
    mysql = connectToMySQL('trips')
    users_query = "SELECT first_name FROM users WHERE id=" +str(userid)
    first_name = mysql.query_db(users_query)
    
    return render_template('new.html', first_name=first_name)

# post route to insert new trip details into database
@app.route('/trips/new', methods=['POST'])
def create_new():

    if len(request.form['destination']) < 3:
        flash("A trip destination must consist of at least 3 characters.", 'destination')
        
    if len(request.form['plan']) < 1:
        flash("A plan must be provided!", 'plan')
        return redirect('/trips/new')
    else:
        #Submit new trip
        mysql = connectToMySQL('trips')
        query = "INSERT INTO trips (destination, start_date, end_date, plan, users_id, created_at, updated_at) VALUES (%(destination)s, %(start_date)s, %(end_date)s, %(plan)s, %(users_id)s, NOW(), NOW());"
        data = {
            'destination': request.form['destination'],
            'start_date': request.form['start_date'],
            'end_date': request.form['end_date'],
            'plan': request.form['plan'],
            'users_id': session['userid']
        }
        mysql.query_db(query, data)
        return redirect('/dashboard')

# route to render edit.html
@app.route('/trips/edit/<id>')
def edit(id):
    
    userid = session['userid']
    mysql = connectToMySQL('trips')
    users_query = "SELECT first_name FROM users WHERE id=" +str(userid)
    first_name = mysql.query_db(users_query)
    
    mysql = connectToMySQL('trips')
    trips_query = "SELECT * FROM trips WHERE id=" +id
    trip = mysql.query_db(trips_query)
    return render_template('edit.html', first_name=first_name, trip=trip)

# POST route to handle editing a current trip
@app.route('/edit_process', methods=['POST'])
def update():

    if len(request.form['destination']) < 3:
        flash("A trip destination must consist of at least 3 characters.", 'destination')
        
    if len(request.form['plan']) < 1:
        flash("A plan must be provided!", 'plan')
        return redirect('/trips/edit/'+request.form['id'])
    else:
        mysql = connectToMySQL('trips')
        trips_query = "UPDATE trips SET destination=%(destination)s, start_date=%(start_date)s, end_date=%(end_date)s, plan=%(plan)s, updated_at = NOW() WHERE id = " + request.form['id']
        data = {
            'destination': request.form['destination'],
            'start_date': request.form['start_date'],
            'end_date': request.form['end_date'],
            'plan': request.form['plan']
        }
        mysql.query_db(trips_query, data)
        return redirect('/dashboard')


# route to render detail page about trip
@app.route('/trips/<id>')
def details(id):

    userid = session['userid']
    mysql = connectToMySQL('trips')
    users_query = "SELECT first_name FROM users WHERE id=" +str(userid)
    first_name = mysql.query_db(users_query)

    mysql = connectToMySQL('trips')
    query = "SELECT * FROM trips WHERE id =" +id
    trip = mysql.query_db(query)

    return render_template('details.html', first_name=first_name, trip=trip)



@app.route('/trips/delete/<id>')
def delete(id):
    mysql = connectToMySQL('trips')
    query = "DELETE FROM trips WHERE id = %(id)s"
    data = {
        'id': id
    }
    mysql.query_db(query, data)
    return redirect('/dashboard')


# logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)