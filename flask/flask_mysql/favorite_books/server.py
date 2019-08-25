from flask import Flask, request, redirect, render_template, session, flash
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
    mysql = connectToMySQL('books_schema')
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
        mysql = connectToMySQL('books_schema')
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


@app.route('/show')
def success():
    
    if 'userid' not in session:
        return redirect('/')
    # QUERY FOR ALL USERS
    userid = session['userid']
    mysql = connectToMySQL('books_schema')
    users_query = "SELECT first_name FROM users WHERE id="+str(userid)
    first_name = mysql.query_db(users_query)
    print(first_name)

    # QUERY FOR ALL BOOKS
    mysql = connectToMySQL('books_schema')
    books_query = "SELECT * FROM books"
    books = mysql.query_db(books_query)

    return render_template('success.html', first_name=first_name, books=books)



@app.route('/member', methods=['POST'])
def member():

    mysql = connectToMySQL('books_schema')
    query = "SELECT password, id FROM users WHERE email = %(email)s;"
    data = {
        'email': request.form['email'],
    }
    mysql = connectToMySQL('books_schema')
    results = mysql.query_db(query, data)

    if len(results) > 0:   
        if bcrypt.check_password_hash(results[0]['password'], request.form['password']):
            session['userid'] = results[0]['id']
            return redirect('/show')
        else:
            flash("Invalid email or password", 'member')
            return redirect('/')
    else:
        flash("Invalid email or password", 'member')
        return redirect('/')




@app.route('/create_process', methods=['POST'])
def create_process():
    print(request.form, "NEW FORM DATA")
    if len(request.form['title']) < 1:
        flash("What's the title of your favorite book?", "title_error")
    if len(request.form['description']) < 5:
        flash("Tell us a little bit about it.", "description_error")
    
        return redirect('/show') # <--- redirect to same page with jinja
        
    else:
        #Create a new book
        mysql = connectToMySQL('books_schema')
        query = "INSERT INTO books (title, description, user_id, created_at, updated_at) VALUES (%(title)s, %(description)s, %(user_id)s, NOW(), NOW());"
        data = {
            'title':request.form['title'],
            'description':request.form['description'],
            'user_id': session['userid']
        }
        mysql.query_db(query, data)
        return redirect('/show') my_wishes1



@app.route('/learn_more/<id>')
def learn_more(id):

    mysql = connectToMySQL('books_schema')
    book_query = "SELECT * FROM books WHERE id=" +str(id) 
    book = mysql.query_db(book_query)

    mysql = connectToMySQL('books_schema')
    query = "SELECT first_name FROM users WHERE id=" +str(book[0]['user_id'])
    addby = mysql.query_db(query)

    # QUERY TO LIST USERS WHO LIKED PARTICULAR BOOKS
    mysql = connectToMySQL('books_schema')
    books_query = """SELECT first_name FROM users
                    LEFT JOIN favorites
                    ON user_liked_id = users.id
                    WHERE book_liked_id = %(book_id)s"""
    data = {
        'book_id': id
    }   
    fans = mysql.query_db(books_query, data)

    return render_template('learn_more.html', book=book, addby=addby, fans=fans)



@app.route('/learn_more/like/<book_id>')
def like(book_id):
    mysql = connectToMySQL('books_schema')
    query = "INSERT INTO favorites (book_liked_id, user_liked_id) VALUES (%(book_id)s, %(user_id)s);"
    data = {
        'book_id': book_id,
        'user_id': session['userid']
    }
    mysql.query_db(query, data)
    return redirect('/show')



@app.route('/learn_more/edit/<id>')
def edit(id):

    mysql = connectToMySQL('books_schema')
    book_query = "SELECT * FROM books WHERE id=" +str(id) 
    mysql.query_db(book_query)
    return redirect('/learn_more/'+str(id))


# POST route to handle editing a current book
@app.route('/learn_more/update/<id>', methods=['POST'])
def update_book(id):

    mysql = connectToMySQL('books_schema')
    query = "UPDATE books_schema.books SET title = %(title)s , description = %(description)s, updated_at = NOW() WHERE id= %(id)s"
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'id': id
    }
    mysql.query_db(query, data)
    print('BOOK UPDATED')

    return redirect('/show')



@app.route('/learn_more/delete/<id>')
def delete_book(id):
    mysql = connectToMySQL('books_schema')
    query = "DELETE FROM books WHERE id = %(id)s"
    data = {
        'id': id
    }
    mysql.query_db(query, data)
    return redirect('/show')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)