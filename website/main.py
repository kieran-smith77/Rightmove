from flask import Flask, render_template, redirect, url_for, session
import db
import asm
from decorators import login_required

app = Flask(__name__, static_folder='static')
app.secret_key = asm.get_secret_key()

import auth_paths

@app.route('/')
@login_required
def home():
    data = db.get_new_item()
    if isinstance(data, str):
        return 'Currently out'
    return render_template('index.html', item=data, good=None)

@app.route('/specific/<id>')
@login_required
def specific(id):
    data = db.get_item(id)
    if isinstance(data, str):
        return 'Error retrieving home'
    return render_template('index.html', item=data, good=None)


@app.route('/Good/<id>')
@login_required
def set_good_review(id):
    db.set_review(id, review='Good')
    return redirect(url_for('home'))

@app.route('/Bad/<id>')
@login_required
def set_bad_review(id):
    db.set_review(id, review='Bad')
    return redirect(url_for('home'))

@app.route('/good-ones')
@login_required
def good_ones():
    data = db.get_old_items(good=True)
    return render_template('listed.html', items=data, good=True)

@app.route('/bad-ones')
@login_required
def bad_ones():
    data = db.get_old_items(good=False)
    return render_template('listed.html', items=data, good=False)

@app.route('/all')
@login_required
def get_all():
    data = db.get_old_items()
    return render_template('listed.html', items=data, good=True)

