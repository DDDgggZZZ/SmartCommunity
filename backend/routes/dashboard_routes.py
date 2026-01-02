from flask import Blueprint, jsonify
from services.dashboard_service import get_dashboard_stats

dashboard_bp = Blueprint("dashboard_bp", __name__)

def ok(data=None, msg="success"):
    return jsonify({"code": 200, "msg": msg, "data": data})

def fail(msg="error", code=500, data=None):
    return jsonify({"code": code, "msg": msg, "data": data})

@dashboard_bp.route("/stats", methods=["GET"])
def dashboard_stats_api():
    data = get_dashboard_stats()
    if data is None:
        return fail("Database Error", 500, {})
    return ok(data)
