from flask import Blueprint, jsonify, request
from services.fee_bill_service import (
    get_all_fee_bills,
    get_fee_bill_by_id,
    create_fee_bill
)

fee_bill_bp = Blueprint("fee_bill_bp", __name__)

def ok(data=None, msg="success"):
    return jsonify({"code": 200, "msg": msg, "data": data})

def fail(msg="error", code=500, data=None):
    return jsonify({"code": code, "msg": msg, "data": data})

def valid_status(s):
    return s in ["未缴", "已缴"]

@fee_bill_bp.route("/", methods=["GET"])
def get_fee_bills_api():
    owner_id = request.args.get("owner_id", default=None, type=int)
    status = request.args.get("status", default=None, type=str)
    bill_month = request.args.get("bill_month", default=None, type=str)

    if status is not None and not valid_status(status):
        return fail("Invalid Status", 400, [])

    data = get_all_fee_bills(owner_id, status, bill_month)
    if data is None:
        return fail("Database Error", 500, [])
    return ok(data)

@fee_bill_bp.route("/<int:bill_id>", methods=["GET"])
def get_fee_bill_detail_api(bill_id):
    data = get_fee_bill_by_id(bill_id)
    if not data:
        return fail("Bill Not Found", 404, {})
    return ok(data)
# [新增] 创建账单接口
@fee_bill_bp.route("/", methods=["POST"])
def create_fee_bill_api():
    body = request.get_json() or {}
    owner_id = body.get("owner_id")
    fee_type_id = body.get("fee_type_id")
    amount = body.get("amount")
    bill_month = body.get("bill_month")
    status = body.get("status", "未缴")

    if not owner_id or not fee_type_id or not amount or not bill_month:
        return fail("Missing required fields (owner_id, fee_type_id, amount, bill_month)", 400)

    res = create_fee_bill(owner_id, fee_type_id, amount, bill_month, status)
    if res is None:
        return fail("Create Failed (Check if Owner/FeeType exists)", 500)
    
    return ok({"id": res}, "Created")