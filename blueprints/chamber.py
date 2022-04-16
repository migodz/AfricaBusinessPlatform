from flask import Blueprint, request, session, jsonify
from models import Chamber, User
from extentions import db
from forms import GetChambersForm, CreateChamberForm

bp = Blueprint("chamber", __name__)


@bp.route("/c-chamber", methods=["post"])
def create_chamber():
    # check if already logged in
    if "username" not in session or session.get('type') != 'cbr':
        return {"code": "0", "msg": "no permission"}

    # check if the chamber info already exists
    user = User.query.filter_by(username=session.get('username')).first()
    if user.cham_id and user.cham_id >= 0:
        return {"code": "0", "msg": "cbr info already exists"}

    form = CreateChamberForm(request.form)
    # check form validation
    if not form.validate():
        return {"code": "0", "msg": "illegal field"}

    # create chamber info
    chamber = Chamber(
        username=user.username,
        name=request.form['name'],
        country=request.form['country'],
        address=request.form['address'],
        telephone=request.form['telephone'],
        email=request.form['email'],
        wechat=request.form['telephone'],
        link=request.form['link'],
        intro=request.form['intro']
    )
    db.session.add(chamber)
    db.session.commit()

    # bind chamber id to user
    user.cham_id = Chamber.query.filter_by(username=user.username).first().cham_id
    db.session.commit()

    return {"code": "1", "msg": "creating succeeded"}


@bp.route("/chamber", methods=["get", "patch"])
def chamber_info():
    # check if already logged in
    if "username" not in session:
        return {"code": "0", "msg": "no permission"}

    # get chamber info
    if request.method == 'GET':
        chamber = None
        if 'cham_id' in request.args:
            cham_id = request.args.get('cham_id')
            chamber = Chamber.query.filter_by(cham_id=cham_id).first()
        elif 'usr' in request.args:
            username = request.args.get('usr')
            user = User.query.filter_by(username=username).first()
            if not user:
                return {"code": "2", "msg": "usr not exist"}
            elif user.type != 'cbr':
                return {"code": "2", "msg": "usr type not cpn"}
            chamber = Chamber.query.filter_by(cham_id=user.cham_id).first()

        if chamber:
            return {"code": "1", "msg": "succeeded", "chamber": chamber.to_dict()}
        else:
            return {"code": "2", "msg": "cbr not exist"}

    # modify chamber info
    elif request.method == 'POST':
        if session.get('type') != 'cpn':
            return {"code": "0", "msg": "no permission"}
        user = User.query.filter_by(username=session.get('username')).first()
        chamber = Chamber.query.filter_by(cham_id=user.cham_id).first()

        # change name
        name = request.form['name']
        if name != '':
            # check name format
            if len(name) > 25 or len(name) < 2:
                return {"code": "0", "msg": "illegal field"}
            chamber.name = name

        # change country
        country = request.form['country']
        if country != '':
            # check country format
            if len(country) != 3:
                return {"code": "0", "msg": "illegal field"}
            chamber.country = country

        # change address
        address = request.form['address']
        if address != '':
            # check address format
            # if False:
            #     return {"code": "0", "msg": "illegal field"}
            chamber.address = address

        # change telephone
        telephone = request.form['telephone']
        if telephone != '':
            # check telephone format
            # if len(country) != 3:
            #     return {"code": "0", "msg": "illegal field"}
            chamber.telephone = telephone

        # change email
        email = request.form['email']
        if email != '':
            # check email format
            # if len(country) != 3:
            #     return {"code": "0", "msg": "illegal field"}
            chamber.email = email

        # change wechat
        wechat = request.form['telephone']
        if wechat != '':
            # check wechat format
            # if len(country) != 3:
            #     return {"code": "0", "msg": "illegal field"}
            chamber.wechat = wechat

        # change link
        link = request.form['link']
        if link != '':
            # check link format
            # if len(country) != 3:
            #     return {"code": "0", "msg": "illegal field"}
            chamber.link = link

        # change intro
        intro = request.form['intro']
        if intro != '':
            # check country format
            # if len(country) != 3:
            #     return {"code": "0", "msg": "illegal field"}
            chamber.intro = intro

        db.session.commit()
        return {"code": "1", "msg": "modification succeeded"}

@bp.route("/get-chambers", methods=["get"])
def get_chambers():
    # check if already logged in
    if "username" not in session:
        return {"code": "0", "msg": "no permission"}

    form = GetChambersForm(request.form)

    # check form validation
    if not form.validate():
        return {"code": "0", "msg": "illegal field"}

    chambers = Chamber.query.offset(form.offset).limit(form.limit)
    return {"code": "1", "chambers": jsonify(chambers)}