from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import jsonify
from flask import request
from flask import url_for
from flask import make_response

from werkzeug.exceptions import abort

import requests

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("limiter", __name__, url_prefix="/limiter")

session = requests.Session()
session.trust_env = False


@bp.route("/")
def index():
    db = get_db()
    routemapping = db.execute(
        "SELECT * FROM routemapping"
    ).fetchall()
    return make_response(jsonify([dict(ix) for ix in routemapping]), 200)


@bp.route('/api', defaults={'path': ''})
@bp.route('/api/<path:path>')
def api(path):
    db = get_db()
    routemapped = (
        db.execute(
            "SELECT * FROM routemapping WHERE routemap = ?",
            (path,),
        )
        .fetchone()
    )
    routemapped = dict(routemapped)
    print(f"Mapping: {path} ---> {routemapped['destination']}")
    resp = session.get(routemapped['destination'], headers=request.headers, data=request.data)
    return make_response(resp.content, resp.status_code)


@bp.route("/create", methods=("GET", "POST"))
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        routemap = request.form["routemap"]
        destination = request.form["destination"]
        print(routemap, destination)
        db = get_db()
        db.execute(
            "INSERT INTO routemapping (routemap, destination) VALUES (?, ?)",
            (routemap, destination),
        )
        db.commit()
    return make_response(jsonify({'message': "Create routemapping sucessfully"}), 200)
