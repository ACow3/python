from flask import Flask, request, redirect, render_template, session, flash
from mysqlconn import connectToMySQL
import re


app = Flask(__name__)
app.secret_key = 'Secret Key'

@app.route('/shows')
def root():
    mysql = connectToMySQL('shows')
    query = "SELECT * FROM shows"
    db_shows = mysql.query_db(query)
    return render_template('index.html', shows=db_shows)


@app.route('/shows/new')
def new():
    return render_template('new.html')


@app.route('/create_new', methods=["POST"])
def create_new():

    is_valid = True
    if len(request.form['title']) < 1:
        is_valid = False
        flash("Please add a show title!", 'title')

    if len(request.form['network']) < 1:
        is_valid = False
        flash("Which network can we find this show?", 'network')

    if len(request.form['description']) < 1:
        is_valid = False
        flash("Please add a show description!", 'description')

    if len(request.form['release_date']) < 1:
        is_valid = False
        flash("When did this show debut?", 'release_date')
    
    if not is_valid:
        return redirect('/shows/new')
    
    else:
        mysql = connectToMySQL('shows')
        show_query = "INSERT INTO shows (title, release_date, description, network,     created_at, updated_at) VALUES (%(title)s, %(release_date)s, %(description) s, %(network)s, NOW(), NOW());"
        data = {
            'title': request.form['title'],
            'release_date': request.form['release_date'],
            'description': request.form['description'],
            'network': request.form['network']
        }
        mysql.query_db(show_query, data)


        return redirect('/shows')



@app.route('/shows/show/<id>')
def display_show(id):
    mysql = connectToMySQL('shows')
    query = "SELECT * FROM shows WHERE id =" +id
    show = mysql.query_db(query)
    return render_template('show.html', show=show)


# GET route to render edit.html page
@app.route('/shows/edit/<id>')
def update(id):
    mysql = connectToMySQL('shows')
    query = "SELECT * FROM shows WHERE id =" +id
    show = mysql.query_db(query)
    return render_template('edit.html', show=show)


    
# POST route to handle editing a current show
@app.route('/shows/edit', methods=['POST'])
def edit():
    mysql = connectToMySQL('shows')
    query = "UPDATE shows SET name = %(name)s , release_date = %(release_date)s , description = %(description)s , network = %(network)s"
    mysql.query_db(query)

    return redirect('/shows')







@app.route('/shows/delete/<id>')
def delete(id):
    mysql = connectToMySQL('shows')
    query = "DELETE FROM shows WHERE id = %(id)s"
    data = {
        'id': id
    }
    mysql.query_db(query, data)
    return redirect('/shows')


if __name__ == "__main__":
    app.run(debug=True)