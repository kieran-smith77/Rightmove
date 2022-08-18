from main import app
from flask import render_template, redirect, url_for, request, session
import auth
from decorators import login_required
from asm import enable_registration


@app.route("/login", methods=["post", "get"])
def login():
    session.pop("session", default=None)
    if request.method == "GET":
        registration = False
        if enable_registration():
            registration = True
        return render_template("user/login.html", registration=registration)
    elif request.method == "POST":
        user = request.form["user"].lower().strip()
        password = request.form["password"].strip()
        verified = auth.verify_user(user, password)
        if verified:
            session["session"] = verified
            return redirect(url_for("home"))
        elif verified is False:
            return render_template("user/login.html", err="pass", user=user)
        else:
            return render_template("user/login.html", err="user", user=user)


@app.route("/register", methods=["get", "post"])
def register():
    session.pop("session", default=None)
    if not enable_registration():
        return redirect(url_for("home"))

    if request.method == "GET":
        return render_template("user/register.html", user="", name="", err="")
    elif request.method == "POST":
        resp, msg = auth.create_user(
            user=request.form["username"].lower().strip(),
            password=request.form["password"].strip(),
            name=request.form["name"].strip(),
        )
        if not resp:
            return render_template(
                "user/register.html",
                user=request.form["username"].strip(),
                name=request.form["name"].strip(),
                err=msg,
            )
        session["session"] = resp
        return redirect(url_for("home"))


@app.route("/logout")
@login_required
def logout():
    session.pop("session", default=None)
    return redirect(url_for("home"))


@app.route("/settings", methods=["get", "post", "delete"])
@login_required
def settings():
    if request.method == "GET":
        registration = None
        err = None
        admin = False
        user_id = session.get("session")
        user = auth.get_user(user_id)
        if "admin" in user and user["admin"] == "True":
            admin = True
            registration = enable_registration()
        return render_template(
            "user/settings.html",
            err=err,
            user=user,
            admin=admin,
            registration=registration,
        )

    if request.method == "POST":
        if "type" in request.form.keys():
            if request.form["type"] == "search":
                # Update Search
                auth.update_search(data=request.form, user_id=session.get("session"))
            elif request.form["type"] == "webhook":
                # Update Webhook
                auth.update_webhook(data=request.form, user_id=session.get("session"))
            elif request.form["type"] == "newSearch":
                # Create search
                auth.new_search(data=request.form, user_id=session.get("session"))
            elif request.form["type"] == "newWebhook":
                # Create webhook
                auth.new_webhook(data=request.form, user_id=session.get("session"))
            elif request.form["type"] == "deleteSearch":
                # Delete search
                auth.remove_search(data=request.form, user_id=session.get("session"))
            elif request.form["type"] == "deleteWebhook":
                # Delete webhook
                auth.remove_webhook(data=request.form, user_id=session.get("session"))
            elif request.form["type"] == "registration":
                auth.toggle_registration(user_id=session.get("session"))
        return redirect(url_for("settings"))
