from flask import Blueprint, jsonify, request
from services.unit_service import (
    building_exists,
    get_all_units,
    get_unit_by_id,
    create_unit,
    update_unit,
    delete_unit
)

unit_bp = Blueprint("unit_bp", __name__)

def ok(data=None, msg="success"):
    return jsonify({"code": 200, "msg": msg, "data": data})

def fail(msg="error", code=500, data=None):
    return jsonify({"code": code, "msg": msg, "data": data})

@unit_bp.route("/", methods=["GET"])
def get_units_api():
    building_id = request.args.get("building_id", default=None, type=int)
    data = get_all_units(building_id)
    if data is None:
        return fail("Database Error", 500, [])
    return ok(data)

@unit_bp.route("/<int:unit_id>", methods=["GET"])
def get_unit_detail_api(unit_id):
    data = get_unit_by_id(unit_id)
    if not data:
        return fail("Unit Not Found", 404, {})
    return ok(data)

@unit_bp.route("/", methods=["POST"])
def create_unit_api():
    body = request.get_json() or {}
    building_id = body.get("building_id")
    unit_no = body.get("unit_no")

    if building_id is None or not unit_no:
        return fail("building_id and unit_no are required", 400, {})

    ex = building_exists(building_id)
    if not ex:
        return fail("Building Not Found", 404, {})

    res = create_unit(building_id, unit_no)
    if res is None:
        return fail("Create Failed", 500, {})

    return ok({"inserted": res}, "created")

@unit_bp.route("/<int:unit_id>", methods=["PUT"])
def update_unit_api(unit_id):
    body = request.get_json() or {}
    building_id = body.get("building_id")
    unit_no = body.get("unit_no")

    if building_id is None or not unit_no:
        return fail("building_id and unit_no are required", 400, {})

    old = get_unit_by_id(unit_id)
    if not old:
        return fail("Unit Not Found", 404, {})

    ex = building_exists(building_id)
    if not ex:
        return fail("Building Not Found", 404, {})

    res = update_unit(unit_id, building_id, unit_no)
    if res is None:
        return fail("Update Failed", 500, {})

    return ok({"updated": res}, "updated")

@unit_bp.route("/<int:unit_id>", methods=["DELETE"])
def delete_unit_api(unit_id):
    old = get_unit_by_id(unit_id)
    if not old:
        return fail("Unit Not Found", 404, {})

    res = delete_unit(unit_id)
    if res is None:
        return fail("Delete Failed", 500, {})

    return ok({"deleted": res}, "deleted")
