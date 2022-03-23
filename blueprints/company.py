from flask import Blueprint

bp = Blueprint("company", __name__)


@bp.route("/company/<int:comp_id>", methods=["get", "patch"])
def company_info(comp_id):
    pass