from flask import Blueprint

from flaskr.controllers.route import get_all_route, create_route

bp = Blueprint("route", __name__, url_prefix="/route")


@bp.route("/")
def index():
    return get_all_route()


@bp.route("/create", methods=["POST"])
def create():
    return create_route()
