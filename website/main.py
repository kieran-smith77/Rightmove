from flask import Flask, render_template, redirect, url_for, session
import db
import asm
from decorators import login_required

app = Flask(__name__, static_folder="static")
app.secret_key = asm.get_secret_key()

import auth_paths  # noqa: F401, E402


@app.route("/")
@login_required
def home():
    user_id = str(session.get("session"))
    data = db.get_new_item(user_id)
    if isinstance(data, str):
        return "Currently out"
    return render_template("index.html", item=data, user=user_id, good=None)


@app.route("/specific/<user>/<id>")
@login_required
def specific(user, id):
    data = db.get_item(id, int(user))
    if isinstance(data, str):
        return "Error retrieving home"
    return render_template("index.html", item=data, user=int(user), good=None)


@app.route("/Good/<user>/<id>")
@login_required
def set_good_review(user, id):
    user_id = session.get("session")
    if int(user) == int(user_id):
        db.set_review(id, user_id, review="Good")
    else:
        db.copy_to_new(id, user, user_id, review="Good")
    return redirect(url_for("home"))


@app.route("/Bad/<user>/<id>")
@login_required
def set_bad_review(user, id):
    user_id = session.get("session")
    if int(user) == int(user_id):
        db.set_review(id, user_id, review="Bad")
    else:
        db.copy_to_new(id, user, user_id, review="Bad")
    return redirect(url_for("home"))


@app.route("/good-ones")
@login_required
def good_ones():
    user_id = session.get("session")
    data = db.get_old_items(user_id, good=True)
    return render_template("listed.html", items=data, user=str(user_id), good=True)


@app.route("/bad-ones")
@login_required
def bad_ones():
    user_id = session.get("session")
    data = db.get_old_items(user_id, good=False)
    return render_template("listed.html", items=data, user=str(user_id), good=False)


@app.route("/all")
@login_required
def get_all():
    user_id = session.get("session")
    data = db.get_old_items(user_id)
    return render_template("listed.html", items=data, user=str(user_id), good=True)
