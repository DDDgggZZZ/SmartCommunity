from flask import Blueprint, jsonify, request
from services.fee_type_service import (
    get_all_fee_types,
    get_fee_type_by_id,
    create_fee_type,
    update_fee_type,
    delete_fee_type
)

fee_type_bp = Blueprint("fee_type_bp", __name__)

def ok(data=None, msg="success"):
    return jsonify({"code": 200, "msg": msg, "data": data})

def fail(msg="error", code=500, data=None):
    return jsonify({"code": code, "msg": msg, "data": data})

@fee_type_bp.route("/", methods=["GET"])
def get_fee_types_api():
    data = get_all_fee_types()
    if data is None:
        return fail("Database Error", 500, [])
    return ok(data)

@fee_type_bp.route("/<int:fee_type_id>", methods=["GET"])
def get_fee_type_detail_api(fee_type_id):
    data = get_fee_type_by_id(fee_type_id)
    if not data:
        return fail("Fee Type Not Found", 404, {})
    return ok(data)

@fee_type_bp.route("/", methods=["POST"])
def create_fee_type_api():
    body = request.get_json() or {}
    name = body.get("name")
    unit_price = body.get("unit_price")
    unit = body.get("unit")

    if not name or unit_price is None or not unit:
        return fail("name, unit_price, unit are required", 400, {})

    res = create_fee_type(name, unit_price, unit)
    if res is None:
        return fail("Create Failed", 500, {})

    return ok({"inserted": res}, "created")

@fee_type_bp.route("/<int:fee_type_id>", methods=["PUT"])
def update_fee_type_api(fee_type_id):
    body = request.get_json() or {}
    name = body.get("name")
    unit_price = body.get("unit_price")
    unit = body.get("unit")

    if not name or unit_price is None or not unit:
        return fail("name, unit_price, unit are required", 400, {})

    old = get_fee_type_by_id(fee_type_id)
    if not old:
        return fail("Fee Type Not Found", 404, {})

    res = update_fee_type(fee_type_id, name, unit_price, unit)
    if res is None:
        return fail("Update Failed", 500, {})

    return ok({"updated": res}, "updated")

@fee_type_bp.route("/<int:fee_type_id>", methods=["DELETE"])
def delete_fee_type_api(fee_type_id):
    old = get_fee_type_by_id(fee_type_id)
    if not old:
        return fail("Fee Type Not Found", 404, {})

    res = delete_fee_type(fee_type_id)
    if res is None:
        return fail("Delete Failed", 500, {})

    return ok({"deleted": res}, "deleted")
