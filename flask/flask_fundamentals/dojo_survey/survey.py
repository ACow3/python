from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def submission():
    return render_template("survey.html")


@app.route('/users', methods=['POST'])
def create_users():
    print("Got Post Info")
    print(request.form)
    name_from_form = request.form['name']
    email_from_form = request.form['email']
    language_from_form = request.form['language']
    location_from_form = request.form['location']
    text_from_form = request.form['textarea']
    return render_template("show.html", name_on_template=name_from_form, email_on_template=email_from_form, language_on_template=language_from_form, location_on_template=location_from_form, text_on_template=text_from_form)


@app.route("/process", methods=["POST"])
def process_form():
    print("in the process_form function")
    print(request.form)
    print(f"name submitted: {request.form['name submitted']}")
    print(f"email submitted: {request.form['email']}")
    return render_template("survey.html", name=request.form["name"], email=request.form["email "])

if __name__ == "__main__":
    app.run(debug=True)