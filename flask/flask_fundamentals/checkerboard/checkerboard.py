from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def start():
    return render_template("checkerboard.html")

@app.route('/<num>')
def next(num):
    num = int(num)
    return render_template("checkerboard.html",numberoftimes=num)
    
if __name__=="__main__":
    app.run(debug=True)