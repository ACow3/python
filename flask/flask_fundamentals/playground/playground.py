from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/play')
def start():
    return render_template("playground.html",numberoftimes=3)

@app.route('/play/<num>')
def next(num):
    num = int(num)
    return render_template("playground.html",numberoftimes=num)

@app.route('/play/<num>/<color>')
def third(num,color):
    num = int(num)
    return render_template ("playground.html", numberoftimes=num, color=color)

if __name__=="__main__":
    app.run(debug=True)