from flask import Blueprint, request, session
from models import User, Company, Chamber
from forms import SignupForm, LoginForm, EmailForm, NewPasswordForm
from extentions import db
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("user", __name__)


@bp.route("/signup", methods=['post'])
def signup():
    form = SignupForm(request.form)

    # check form validation
    if not form.validate():
        return {"code": "0", "msg": "illegal field"}

    # add new user
    password_md5 = generate_password_hash(form.pwd.data)
    user = User(username=form.usr.data,
                password=password_md5,
                email=form.email.data,
                nickname=form.nknm.data,
                type=form.type.data)
    db.session.add(user)
    db.session.commit()
    return {"code": "1", "msg": "succeeded"}


@bp.route("/login", methods=['post'])
def login():
    # check if already logged in
    if session.get("username"):
        return {"code": "0", "msg": "already logged in"}

    # print(request.form['usr'])
    # print(request.form['pwd'])

    form = LoginForm(request.form)

    # check form validation
    if not form.validate():
        return {"code": "0", "msg": "illegal field"}

    user = User.query.filter_by(username=form.usr.data).first()

    # check if user exist
    if not user:
        return {"code": "2", "msg": "usr not exist"}

    # check password
    if not check_password_hash(user.password, form.pwd.data):
        return {"code": "4", "msg": "pwd not match"}

    # all passed, login
    session['username'] = user.username
    session['type'] = user.type

    # check user type
    nxt = ""
    if user.type == 'usr':
        nxt = 'usr'
    elif user.type == 'cpn':
        if len(Company.query.filter_by(username=user.username).all()) == 0:
            nxt = 'cpn-incomplete'
        else:
            nxt = 'cpn'
    else:
        if len(Chamber.query.filter_by(username=user.username).all()) == 0:
            nxt = 'cbr-incomplete'
        else:
            nxt = 'cbr'

    return {"code": "1", "msg": "login succeeded", "next": nxt}


@bp.route("/logout", methods=['post'])
def logout():
    if "username" in session:
        session.clear()
        return {"code": "1", "msg": "logout succeeded"}
    return {"code": "0", "msg": "logout failed"}


@bp.route("/user", methods=["get", "post"])
def user_info():
    # check if already logged in
    if not "username" in session:
        return {"code": "0", "msg": "no permission"}

    # get user info
    if request.method == 'GET':
        username = request.args.get('usr')
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"code": "2", "msg": "usr not exist"}
        return {"code": "1", "msg": "succeeded", "user": user.to_dict()}

    # modify user info
    elif request.method == 'POST':
        user = User.query.filter_by(username=session['username']).first()

        # change nickname
        nickname = request.form['nknm']
        if nickname != '':
            # check nickname format
            if len(nickname) > 25 or len(nickname) < 5:
                return {"code": "0", "msg": "illegal field"}
            user.nickname = nickname

        # change email
        email = request.form['email']
        if email != '':
            # check email format
            form2 = EmailForm(data={'email': email})
            if not form2.validate():
                return {"code": "0", "msg": "illegal field"}

            # check if email already been used
            if User.query.filter_by(email=email).first():
                return {"code": "3", "msg": "email used"}
            user.email = email

        # change password
        password = request.form['pwd']
        new_password = request.form['new_pwd']

        if new_password != '':
            # check password format
            form3 = NewPasswordForm(data={'pwd': password, 'new_pwd': new_password})
            if not form3.validate():
                return {"code": "0", "msg": "illegal field"}

            # check if password matches
            if not check_password_hash(user.password, password):
                return {"code": "4", "msg": "pwd not match"}
            password_md5 = generate_password_hash(new_password)
            user.password = password_md5

        db.session.commit()
        return {"code": "1", "msg": "modification succeeded"}