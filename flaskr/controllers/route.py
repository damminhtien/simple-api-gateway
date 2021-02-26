from flask import jsonify
from flask import request
from flask import make_response

from flaskr.db import get_db


def get_all_route():
    try:
        db = get_db()
        routemapping = db.execute(
            "SELECT * FROM routemapping"
        ).fetchall()
        return make_response(jsonify([dict(ix) for ix in routemapping]), 200)
    except:
        pass
    return make_response(jsonify([]), 200)


def create_route():
    routemap = request.form["routemap"]
    destination = request.form["destination"]
    try:
        db = get_db()
        db.execute(
            "INSERT INTO routemapping (routemap, destination) VALUES (?, ?)",
            (routemap, destination),
        )
        db.commit()
        return make_response(jsonify({'message': 'Create routemapping successfully'}), 200)
    except:
        pass
    return make_response(jsonify({'message': 'Cannot create routemapping'}), 400)
