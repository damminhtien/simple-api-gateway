from flask import Blueprint

from flaskr.controllers.api import get_api

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route('/', defaults={'route': ''})
@bp.route('/<string:route>')
def index(route):
    return get_api(route)
