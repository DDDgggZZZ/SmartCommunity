from flask import Blueprint, jsonify, request
from services.room_service import (
    unit_exists,
    unit_in_building,
    get_all_rooms,
    get_room_by_id,
    create_room,
    update_room,
    delete_room
)


room_bp = Blueprint("room_bp", __name__)

def ok(data=None, msg="success"):
    return jsonify({"code": 200, "msg": msg, "data": data})

def fail(msg="error", code=500, data=None):
    return jsonify({"code": code, "msg": msg, "data": data})

@room_bp.route("/", methods=["GET"])
def get_rooms_api():
    building_id = request.args.get("building_id", default=None, type=int)
    unit_id = request.args.get("unit_id", default=None, type=int)

    if building_id is not None and unit_id is not None:
        rel = unit_in_building(building_id, unit_id)
        if not rel:
            return fail("Unit Not In Building", 400, [])

    data = get_all_rooms(building_id, unit_id)
    if data is None:
        return fail("Database Error", 500, [])
    return ok(data)


@room_bp.route("/<int:room_id>", methods=["GET"])
def get_room_detail_api(room_id):
    data = get_room_by_id(room_id)
    if not data:
        return fail("Room Not Found", 404, {})
    return ok(data)

@room_bp.route("/", methods=["POST"])
def create_room_api():
    body = request.get_json() or {}
    unit_id = body.get("unit_id")
    room_no = body.get("room_no")
    area = body.get("area")
    layout = body.get("layout")
    status = body.get("status")

    if unit_id is None or not room_no or area is None:
        return fail("unit_id, room_no, area are required", 400, {})

    ex = unit_exists(unit_id)
    if not ex:
        return fail("Unit Not Found", 404, {})

    res = create_room(unit_id, room_no, area, layout, status)
    if res is None:
        return fail("Create Failed", 500, {})

    return ok({"inserted": res}, "created")

@room_bp.route("/<int:room_id>", methods=["PUT"])
def update_room_api(room_id):
    body = request.get_json() or {}
    unit_id = body.get("unit_id")
    room_no = body.get("room_no")
    area = body.get("area")
    layout = body.get("layout")
    status = body.get("status")

    if unit_id is None or not room_no or area is None or status is None:
        return fail("unit_id, room_no, area, status are required", 400, {})

    old = get_room_by_id(room_id)
    if not old:
        return fail("Room Not Found", 404, {})

    ex = unit_exists(unit_id)
    if not ex:
        return fail("Unit Not Found", 404, {})

    res = update_room(room_id, unit_id, room_no, area, layout, status)
    if res is None:
        return fail("Update Failed", 500, {})

    return ok({"updated": res}, "updated")

@room_bp.route("/<int:room_id>", methods=["DELETE"])
def delete_room_api(room_id):
    old = get_room_by_id(room_id)
    if not old:
        return fail("Room Not Found", 404, {})

    res = delete_room(room_id)
    if res is None:
        return fail("Delete Failed", 500, {})

    return ok({"deleted": res}, "deleted")
