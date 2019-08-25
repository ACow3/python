from flask import Flask, request, redirect, render_template
from mysqlconn import connectToMySQL
app = Flask(__name__)

@app.route('/users')
def root():
    db = connectToMySQL('users')
    users = db.query_db('SELECT * FROM users.users;')
    print(users)
    return render_template('index.html', users=users)


@app.route('/users/new')
def new():
    mysql = connectToMySQL('users')
    users = mysql.query_db('SELECT * FROM users;')
    print(users)
    return render_template('new.html', users=users)


@app.route('/create_new_user', methods=['POST'])
def create_new_user():
    print('hit /create_new_user POST route')
    query = "INSERT INTO users (name, email, created_at, updated_at) VALUES (%(name)s, %(email)s, NOW(), NOW());"
    data = {
        'name': request.form['name'],
        'email': request.form['email']
    }
    db = connectToMySQL('users')
    id = db.query_db(query, data)
    print('id:', id)
    return redirect('/users')

@app.route('/users/show/<id>')
def show(id):
    mysql = connectToMySQL("users")
    query = "SELECT * FROM users WHERE id =" + id
    user = mysql.query_db(query)
    return render_template('show.html', user=user)

# GET route to render edit.html page
@app.route('/users/edit/<id>')
def edit(id):
    mysql = connectToMySQL("users")
    query = "SELECT * FROM users WHERE id =" +id
    user = mysql.query_db(query)
    return render_template('edit.html', user=user)

# POST route to handle editing a current user
@app.route("/users/edit", methods=['POST'])
def update():
    
    db = connectToMySQL('users')
    query = "UPDATE users SET name = %(name)s , email = %(email)s WHERE id = %(id)s"
    data = {
        'name' : request.form['name'],
        'email': request.form['email'],
        'id': request.form['id']
    }
    db.query_db(query, data)
    print('id:', id)
    return redirect('/users')


@app.route("/users/delete/<id>")
def delete(id):
    mysql = connectToMySQL("users")
    query = "DELETE FROM users WHERE id = %(id)s"
    data = {
        'id' : id
    }
    mysql.query_db(query, data)
    return redirect('/users')

if __name__=="__main__":
    app.run(debug=True)