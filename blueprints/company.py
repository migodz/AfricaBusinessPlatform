from flask import Blueprint, session, request, jsonify
from models import User, Company
from extentions import db
from forms import GetCompaniesForm, CreateCompanyForm

bp = Blueprint("company", __name__)


@bp.route("/c-company", methods=["post"])
def create_company():
    # check if already logged in
    if "username" not in session or session.get('type') != 'cpn':
        return {"code": "0", "msg": "no permission"}

    # check if the company info already exists
    user = User.query.filter_by(username=session.get('username')).first()
    if user.comp_id and user.comp_id >= 0:
        return {"code": "0", "msg": "cpn info already exists"}

    form = CreateCompanyForm(request.form)
    # check form validation
    if not form.validate():
        return {"code": "0", "msg": "illegal field"}

    # create company info
    company = Company(
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
    db.session.add(company)
    db.session.commit()

    # bind company id to user
    user.comp_id = Company.query.filter_by(username=user.username).first().comp_id
    db.session.commit()

    return {"code": "1", "msg": "creating succeeded"}


@bp.route("/company", methods=["get", "post"])
def company_info():
    # check if already logged in
    if "username" not in session:
        return {"code": "0", "msg": "no permission"}

    # get company info
    company = None
    if request.method == 'GET':
        if 'comp_id' in request.args:
            comp_id = request.args.get('comp_id')
            company = Company.query.filter_by(comp_id=comp_id).first()
        elif 'usr' in request.args:
            username = request.args.get('usr')
            user = User.query.filter_by(username=username).first()
            if not user:
                return {"code": "2", "msg": "usr not exist"}
            elif user.type != 'cpn':
                return {"code": "2", "msg": "usr type not cpn"}
            company = Company.query.filter_by(comp_id=user.comp_id).first()

        if company:
            return {"code": "1", "msg": "succeeded", "company": company.as_dict()}
        else:
            return {"code": "2", "msg": "cpn not exist"}

    # modify company info
    elif request.method == 'POST':
        if session.get('type') != 'cpn':
            return {"code": "0", "msg": "no permission"}
        user = User.query.filter_by(username=session.get('username')).first()
        company = Company.query.filter_by(comp_id=user.comp_id).first()

        # change name
        name = request.form['name']
        if name != '':
            # check name format
            if len(name) > 25 or len(name) < 2:
                return {"code": "0", "msg": "illegal field"}
            company.name = name

        # change country
        country = request.form['country']
        if country != '':
            # check country format
            if len(country) != 3:
                return {"code": "0", "msg": "illegal field"}
            company.country = country

        # change address
        address = request.form['address']
        if address != '':
            # check address format
            # if False:
            #     return {"code": "0", "msg": "illegal field"}
            company.address = address

        # change telephone
        telephone = request.form['telephone']
        if telephone != '':
            # check telephone format
            # if len(country) != 3:
            #     return {"code": "0", "msg": "illegal field"}
            company.telephone = telephone

        # change email
        email = request.form['email']
        if email != '':
            # check email format
            # if len(country) != 3:
            #     return {"code": "0", "msg": "illegal field"}
            company.email = email

        # change wechat
        wechat = request.form['telephone']
        if wechat != '':
            # check wechat format
            # if len(country) != 3:
            #     return {"code": "0", "msg": "illegal field"}
            company.wechat = wechat

        # change link
        link = request.form['link']
        if link != '':
            # check link format
            # if len(country) != 3:
            #     return {"code": "0", "msg": "illegal field"}
            company.link = link

        # change intro
        intro = request.form['intro']
        if intro != '':
            # check country format
            # if len(country) != 3:
            #     return {"code": "0", "msg": "illegal field"}
            company.intro = intro

        db.session.commit()
        return {"code": "1", "msg": "modification succeeded"}


@bp.route("/get-companies", methods=["get"])
def get_companies():
    # check if already logged in
    if "username" not in session:
        return {"code": "0", "msg": "no permission"}

    form = GetCompaniesForm(request.form)

    # check form validation
    if not form.validate():
        return {"code": "0", "msg": "illegal field"}

    companies = Company.query.offset(form.offset).limit(form.limit).all()
    return {"code": "0", "companies": jsonify(companies)}