from flask import Blueprint, jsonify, request
from services.building_service import (
    get_all_buildings,
    get_building_by_id,
    create_building,
    update_building,
    delete_building
)

building_bp = Blueprint("building_bp", __name__)

#  统一返回工具（可复用）
def ok(data=None, msg="success"):
    return jsonify({"code": 200, "msg": msg, "data": data})

def fail(msg="error", code=500, data=None):
    return jsonify({"code": code, "msg": msg, "data": data})


#  1) 获取楼栋列表
@building_bp.route("/", methods=["GET"])
def get_buildings_api():
    data = get_all_buildings()
    if data is None:
        return fail("Database Error", 500, [])
    return ok(data)


#  2) 获取楼栋详情
@building_bp.route("/<int:building_id>", methods=["GET"])
def get_building_detail_api(building_id):
    data = get_building_by_id(building_id)
    if not data:
        return fail("Building Not Found", 404, {})
    return ok(data)


#  3) 新增楼栋
@building_bp.route("/", methods=["POST"])
def create_building_api():
    body = request.get_json() or {}
    building_no = body.get("building_no")
    total_floors = body.get("total_floors")
    description = body.get("description")

    if not building_no or total_floors is None:
        return fail("building_no and total_floors are required", 400, {})

    res = create_building(building_no, total_floors, description)
    if res is None:
        return fail("Create Failed", 500, {})

    return ok({"inserted": res}, "created")


#  4) 更新楼栋
@building_bp.route("/<int:building_id>", methods=["PUT"])
def update_building_api(building_id):
    body = request.get_json() or {}
    building_no = body.get("building_no")
    total_floors = body.get("total_floors")
    description = body.get("description")

    if not building_no or total_floors is None:
        return fail("building_no and total_floors are required", 400, {})

    # 先检查是否存在
    old = get_building_by_id(building_id)
    if not old:
        return fail("Building Not Found", 404, {})

    res = update_building(building_id, building_no, total_floors, description)
    if res is None:
        return fail("Update Failed", 500, {})

    return ok({"updated": res}, "updated")


#  5) 删除楼栋
@building_bp.route("/<int:building_id>", methods=["DELETE"])
def delete_building_api(building_id):
    # 先检查是否存在
    old = get_building_by_id(building_id)
    if not old:
        return fail("Building Not Found", 404, {})

    res = delete_building(building_id)
    if res is None:
        return fail("Delete Failed", 500, {})

    return ok({"deleted": res}, "deleted")
