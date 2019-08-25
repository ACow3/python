from flask import Flask, request, redirect, render_template, session, flash
from mysqlconn import connectToMySQL
import re

app = Flask(__name__)
app.secret_key = "It's a secret"

@app.route('/')
def root():
    mysql = connectToMySQL('amadon')
    query = "SELECT * FROM items"
    items = mysql.query_db(query)
    print('WHATEVER')
    return render_template('index.html', items=items)

@app.route('/buy')
def purchase():
    mysql = connectToMySQL('amadon')
    query = "SELECT price FROM items WHERE id=" +id
    data = {
        'price': request.form['price']
    }
    mysql.query_db(query, data)
    print('price')
    return redirect('/checkout/' +str(id))

@app.route('/checkout/<id>')
def checkout(id):
    mysql = connectToMySQL('amadon')
    query = "SELECT price FROM items WHERE id=" +str(id)
    mysql.query_db(query)
    return render_template('checkout.html')

if __name__ == "__main__":
    app.run(debug=True)