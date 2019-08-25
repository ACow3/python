from flask import Flask, request, redirect, render_template
from mysqlconn import connectToMySQL
app = Flask(__name__)

@app.route("/")
def pets():
    mysql = connectToMySQL('pets')
    pets = mysql.query_db('SELECT * FROM pets;')
    print(pets)
    return render_template("index.html", all_pets=pets)

@app.route("/create_new_pet", methods=['POST'])
def create_new_pet():
    print('hit /create_new_pet POST route')
    query = "INSERT INTO pets (name, type, created_at, updated_at) VALUES (%(name)s, %(type)s, NOW(), NOW());"
    data = {
        'name': request.form['name'],
        'type': request.form['type']
    }

    db = connectToMySQL('pets')
    id = db.query_db(query, data)
    print('id:', id)
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)