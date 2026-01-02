from flask import Blueprint, jsonify, request
from services.auth_service import (
    login,
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user
)

auth_bp = Blueprint("auth_bp", __name__)

def ok(data=None, msg="success"):
    return jsonify({"code": 200, "msg": msg, "data": data})

def fail(msg="error", code=500, data=None):
    return jsonify({"code": code, "msg": msg, "data": data})

def valid_role(role):
    return role in ["admin", "staff"]

@auth_bp.route("/login", methods=["POST"])
def login_api():
    body = request.get_json() or {}
    username = body.get("username")
    password = body.get("password")

    if not username or not password:
        return fail("username and password are required", 400, {})

    user = login(username, password)
    if not user:
        return fail("Invalid Credentials", 401, {})

    return ok(user, "login success")

@auth_bp.route("/users", methods=["GET"])
def get_users_api():
    data = get_all_users()
    if data is None:
        return fail("Database Error", 500, [])
    return ok(data)

@auth_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_detail_api(user_id):
    data = get_user_by_id(user_id)
    if not data:
        return fail("User Not Found", 404, {})
    return ok(data)

@auth_bp.route("/users", methods=["POST"])
def create_user_api():
    body = request.get_json() or {}
    username = body.get("username")
    password = body.get("password")
    role = body.get("role")

    if not username or not password or not role:
        return fail("username, password, role are required", 400, {})

    if not valid_role(role):
        return fail("Invalid Role", 400, {})

    res = create_user(username, password, role)
    if res is None:
        return fail("Create Failed", 500, {})

    return ok({"inserted": res}, "created")

@auth_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user_api(user_id):
    body = request.get_json() or {}
    password = body.get("password")
    role = body.get("role")

    if not password or not role:
        return fail("password and role are required", 400, {})

    if not valid_role(role):
        return fail("Invalid Role", 400, {})

    old = get_user_by_id(user_id)
    if not old:
        return fail("User Not Found", 404, {})

    res = update_user(user_id, password, role)
    if res is None:
        return fail("Update Failed", 500, {})

    return ok({"updated": res}, "updated")

@auth_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user_api(user_id):
    old = get_user_by_id(user_id)
    if not old:
        return fail("User Not Found", 404, {})

    res = delete_user(user_id)
    if res is None:
        return fail("Delete Failed", 500, {})

    return ok({"deleted": res}, "deleted")
