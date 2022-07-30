from main import app
from flask import render_template, redirect, url_for, request, session
import auth
from decorators import login_required
from asm import enable_registration

@app.route('/login', methods=['post', 'get'])
def login():
    session.pop('session', default=None)
    if request.method=='GET':
        return render_template('login.html')
    elif request.method=='POST':
        user = request.form['user'].lower().strip()
        password = request.form['password'].strip()
        verified = auth.verify_user(user, password)
        if verified:
            session['session']=verified
            return redirect(url_for('home'))
        elif verified == False:
            return render_template('login.html', err="pass", user = user)
        else:
            return render_template('login.html', err="user", user = user)

@app.route('/register', methods=['get','post'])
def register():
    session.pop('session', default=None)
    if not enable_registration():
        return redirect(url_for('home'))

    if request.method=='GET':
        return render_template(
            'register.html', 
            user='', 
            name='', 
            err='')
    elif request.method=='POST':
        resp, msg = auth.create_user(
            user = request.form['username'].lower().strip(),
            password = request.form['password'].strip(),
            name = request.form['name'].strip())
        if not resp:
            return render_template(
                'register.html', 
                user=request.form['username'].strip(), 
                name=request.form['name'].strip(), 
                err=msg)
        session['session']=resp
        return redirect(url_for('home'))
    

@app.route('/logout')
@login_required
def logout():
    session.pop('session', default=None)
    return redirect(url_for('home'))