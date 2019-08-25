from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def start():
    return render_template("advgame.html")

@app.route('/drive')
def drive():
    return render_template("advgame1.html")

@app.route('/bart')
def bart():
    return render_template("advgame2.html")

if __name__ =="__main__":
    app.run(debug=True)
