from flask import Blueprint, jsonify
from services.user_service import get_all_users # 导入上面的 Service

# 创建一个蓝图对象
user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['GET'])
def get_users_api():
    # 1. 调用 Service 层获取数据
    data = get_all_users()
    
    # 2. 统一返回格式 (Member A 的工作)
    if data is not None:
        return jsonify({
            "code": 200, 
            "msg": "success", 
            "data": data
        })
    else:
        return jsonify({
            "code": 500, 
            "msg": "Database Error", 
            "data": []
        })