from flask import Flask
app = Flask(__name__)

@app.route('/')          
def hello_world():
    return 'Hello World!'
    return render_template('index.html')

@app.route('/dojo')
def dojo():
  return "Dojo!"
  

@app.route('/say/<name>/<times>')
def hi(name,times):
    print(name)
    return render_template("index.html", some_name=name, nun_times=int(times))

@app.route('repeat/<integer>/<name>')
def repeat(integer,name):
    return(name + ' ')*int(integer)

if __name__=="__main__": 
    app.run(debug=True)