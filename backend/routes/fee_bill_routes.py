from flask import Blueprint, jsonify, request
from services.fee_bill_service import (
    get_all_fee_bills,
    get_fee_bill_by_id
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
