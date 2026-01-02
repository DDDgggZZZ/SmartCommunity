from flask import Blueprint, jsonify, request
from services.fee_bill_generate_service import generate_bills_for_month, fee_type_exists

generate_bp = Blueprint("generate_bp", __name__)

def ok(data=None, msg="success"):
    return jsonify({"code": 200, "msg": msg, "data": data})

def fail(msg="error", code=500, data=None):
    return jsonify({"code": code, "msg": msg, "data": data})

def valid_month(s):
    if not s or len(s) != 7:
        return False
    if s[4] != "-":
        return False
    y = s[:4]
    m = s[5:]
    if not y.isdigit() or not m.isdigit():
        return False
    mm = int(m)
    return 1 <= mm <= 12

@generate_bp.route("/", methods=["POST"])
def generate_bills_api():
    body = request.get_json() or {}
    fee_type_id = body.get("fee_type_id")
    bill_month = body.get("bill_month")

    if fee_type_id is None or not bill_month:
        return fail("fee_type_id and bill_month are required", 400, {})

    try:
        fee_type_id = int(fee_type_id)
    except Exception:
        return fail("fee_type_id must be int", 400, {})

    if not valid_month(bill_month):
        return fail("bill_month format must be YYYY-MM", 400, {})

    ft = fee_type_exists(fee_type_id)
    if not ft:
        return fail("Fee Type Not Found", 404, {})

    res = generate_bills_for_month(fee_type_id, bill_month)
    if res is None:
        return fail("Generate Failed", 500, {})

    return ok(res, "generated")
