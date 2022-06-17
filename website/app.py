from flask import Flask, render_template, redirect, url_for
import db

app = Flask(__name__, static_folder='static')


@app.route('/')
def home():
    data = db.get_new_item()
    return render_template('home.html', item=data, good=None)

@app.route('/specific/<id>')
def specific(id):
    data = db.get_item(id)
    if isinstance(data, str):
        return 'Go scrape some more'
    return render_template('home.html', item=data, good=None)


@app.route('/Good/<id>')
def set_good_review(id):
    db.set_review(id, review='Good')
    return redirect(url_for('home'))

@app.route('/Bad/<id>')
def set_bad_review(id):
    db.set_review(id, review='Bad')
    return redirect(url_for('home'))

@app.route('/good-ones')
def good_ones():
    data = db.get_old_items(good=True)
    return render_template('listed.html', items=data, good=True)

@app.route('/bad-ones')
def bad_ones():
    data = db.get_old_items(good=False)
    return render_template('listed.html', items=data, good=False)
