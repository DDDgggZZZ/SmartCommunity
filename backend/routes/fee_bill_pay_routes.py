from flask import Blueprint, jsonify, request
from services.fee_bill_pay_service import (
    get_bill_by_id,
    pay_bill_now,
    pay_bill_with_time
)

pay_bp = Blueprint("pay_bp", __name__)

def ok(data=None, msg="success"):
    return jsonify({"code": 200, "msg": msg, "data": data})

def fail(msg="error", code=500, data=None):
    return jsonify({"code": code, "msg": msg, "data": data})

@pay_bp.route("/<int:bill_id>/pay", methods=["PUT"])
def pay_bill_api(bill_id):
    bill = get_bill_by_id(bill_id)
    if not bill:
        return fail("Bill Not Found", 404, {})

    if bill.get("status") == "已缴":
        return fail("Already Paid", 400, {})

    body = request.get_json(silent=True) or {}
    pay_time = body.get("pay_time")

    if pay_time is None or pay_time == "":
        res = pay_bill_now(bill_id)
    else:
        res = pay_bill_with_time(bill_id, pay_time)

    if res is None:
        return fail("Pay Failed", 500, {})

    return ok({"paid": res}, "paid")
