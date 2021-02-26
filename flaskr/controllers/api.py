from flask import request
from flask import make_response
import requests

from flaskr.db import get_db

session = requests.Session()
session.trust_env = False


def get_api(route):
    try:
        db = get_db()
        route_mapping = (
            db.execute(
                "SELECT * FROM routemapping WHERE routemap = ?",
                (route,),
            ).fetchone()
        )
        if route_mapping:
            route_mapping = dict(route_mapping)
        resp = []
        if request.method == "GET":
            resp = session.get(
                route_mapping['destination'], headers=request.headers, data=request.data)
        elif request.method == "POST":
            resp = session.post(route_mapping['destination'], data=request.data, json=request.get_json())
        print(f"Mapping: {route} ---> {route_mapping['destination']}")
        return make_response(resp.content, resp.status_code)
    except:
        pass
    return make_response({'message': 'Cannot resolve host'}, 404)

