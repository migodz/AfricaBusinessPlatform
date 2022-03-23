from flask import Blueprint

bp = Blueprint("chamber", __name__)


@bp.route("/chamber/<int:cham_id>", methods=["get", "patch"])
def chamber_info(cham_id):
    pass