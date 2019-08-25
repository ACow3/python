from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello_world():
    return "Hello World"

@app.route('/dojo')
def dojo():
    return "Dojo!"

@app.route('/say/<name>')
def hi(name):
    print(name)
    return "Hi " + name

@app.route('/repeat/<integer>/<name>')
def repeat(integer, name):
    return (name + ' ')*int(integer)

if __name__=="__main__":
    app.run(debug=True)


    