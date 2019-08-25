from flask import Flask, render_template, request, redirect, session, flash
from mysqlconn import connectToMySQL

app = Flask(__name__)
app.secret_key = 'Secret ass key'

@app.route('/')
def submission():
    return render_template("survey.html")


@app.route("/process", methods=["POST"]) #INSERTS everything into database
def process_form():


    is_valid = True
    if len(request.form['name']) < 1:
        is_valid = False
        flash("Oops! Looks like you forgot to enter your name.")
    if len(request.form['email']) < 1:
        is_valid = False
        flash("Uh oh! What's your email?")
    if not is_valid:
        return redirect('/')
    else:
        mysql = connectToMySQL('survey')
        query = "INSERT INTO users (name, email, location, language, created_at, updated_at)    VALUES (%(name)s, %(email)s, %(location)s, %(language)s, NOW(), NOW());"
        data = {
            'name' : request.form['name'],
            'email' : request.form['email'],
            'location' : request.form['location'],
            'language' : request.form['language']
        }

        id = mysql.query_db(query, data)
        flash("Survey Completed!")
        return redirect('/show/' + str(id))


@app.route('/show/<id>') #Displays info on show page
def show(id):
    mysql = connectToMySQL("survey")
    query = "SELECT * FROM users WHERE id =" + str(id)
    user = mysql.query_db(query)
    return render_template('show.html', user=user)

if __name__ == "__main__":
    app.run(debug=True)