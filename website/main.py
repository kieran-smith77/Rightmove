from flask import Flask, render_template, redirect, url_for
import db
from bcrypt import hashpw

app = Flask(__name__, static_folder='static')

@app.route('/login', methods=['post'])
def login(user=None):
    if request.method=='POST':
        user = request.form['user'].lower()
        password_hash = hashpw(bytes(request.form['password']+email))
        print(user, password_hash)
        db.verify(user, password_hash)
        print(db.verify)

@app.route('/register', methods=['post'])
def register(user=None):
    pass

@app.route('/logout')
def logout():
    pass

@app.route('/')
def home(user=None):
    data = db.get_new_item()
    if isinstance(data, str):
        return 'Currently out'
    return render_template('index.html', item=data, good=None)

@app.route('/specific/<id>')
def specific(id, user=None):
    data = db.get_item(id)
    if isinstance(data, str):
        return 'Error retrieving home'
    return render_template('index.html', item=data, good=None)


@app.route('/Good/<id>')
def set_good_review(id, user=None):
    db.set_review(id, review='Good')
    return redirect(url_for('home'))

@app.route('/Bad/<id>')
def set_bad_review(id, user=None):
    db.set_review(id, review='Bad')
    return redirect(url_for('home'))

@app.route('/good-ones')
def good_ones(user=None):
    data = db.get_old_items(good=True)
    return render_template('listed.html', items=data, good=True)

@app.route('/bad-ones')
def bad_ones(user=None):
    data = db.get_old_items(good=False)
    return render_template('listed.html', items=data, good=False)

@app.route('/all')
def get_all(user=None):
    data = db.get_old_items()
    return render_template('listed.html', items=data, good=True)

