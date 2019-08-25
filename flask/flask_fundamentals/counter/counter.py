from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'

@app.route('/')
def visits():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    return render_template('counter.html', total_visits=session['visits'])
 
@app.route('/delete-visits/')
def delete_visits():
    session.clear()
    return redirect('/')

if __name__== "__main__":
    app.run(debug=True)