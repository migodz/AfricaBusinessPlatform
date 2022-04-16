from flask import Blueprint, session, request
from models import User, Company
from extentions import db

bp = Blueprint("service", __name__)

# randomly get entities
@bp.route("/rget")
def get_entities():
    pass