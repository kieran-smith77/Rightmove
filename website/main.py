from flask import Flask, render_template, redirect, url_for, request, session
import db
import asm

app = Flask(__name__, static_folder='static')

app.secret_key = asm.get_secret_key()

@app.route('/login', methods=['post', 'get'])
def login(user=None):
    session.pop('session', default=None)
    if request.method=='GET':
        return render_template('login.html')
    elif request.method=='POST':
        user = request.form['user'].lower()
        password = request.form['password']
        verified = db.verify_user(user, password)
        if verified:
            session['session']='123'
            return redirect(url_for('home'))
        elif verified == False:
            return "Password does not match"
        else:
            return "User not found"

@app.route('/register', methods=['post'])
def register(user=None):
    return redirect(url_for('home'))
    

@app.route('/logout')
def logout():
    session.pop('user', default=None)
    return redirect(url_for('home'))

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

