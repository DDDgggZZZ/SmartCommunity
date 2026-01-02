from flask import Flask
from flask_cors import CORS

# 引入我们写好的路由蓝图
from routes.user_routes import user_bp
from routes.building_routes import building_bp
from routes.unit_routes import unit_bp

app = Flask(__name__)

# ★关键：解决跨域问题
CORS(app) 

# ★注册蓝图 (Register Blueprint)
# url_prefix 的意思是：这个蓝图下的所有接口，前面都自动加上 /api/users
# 所以访问地址依然是: http://127.0.0.1:5000/api/users/
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(building_bp, url_prefix="/api/buildings")
app.register_blueprint(unit_bp, url_prefix="/api/units")
from routes.room_routes import room_bp
app.register_blueprint(room_bp, url_prefix="/api/rooms")
from routes.parking_space_routes import parking_bp
app.register_blueprint(parking_bp, url_prefix="/api/parkings/spaces")
from routes.owner_routes import owner_bp
app.register_blueprint(owner_bp, url_prefix="/api/owners")
from routes.owner_room_rel_routes import binding_bp
app.register_blueprint(binding_bp, url_prefix="/api/owners/bindings")
from routes.fee_type_routes import fee_type_bp
app.register_blueprint(fee_type_bp, url_prefix="/api/fees/types")
from routes.fee_bill_routes import fee_bill_bp
app.register_blueprint(fee_bill_bp, url_prefix="/api/fees/bills")
from routes.fee_bill_generate_routes import generate_bp
app.register_blueprint(generate_bp, url_prefix="/api/fees/bills/generate")
from routes.fee_bill_pay_routes import pay_bp
app.register_blueprint(pay_bp, url_prefix="/api/fees/bills")
from routes.repair_routes import repair_bp
app.register_blueprint(repair_bp, url_prefix="/api/repairs")
from routes.repair_submit_routes import repair_submit_bp
app.register_blueprint(repair_submit_bp, url_prefix="/api/repairs")
from routes.repair_update_routes import repair_update_bp
app.register_blueprint(repair_update_bp, url_prefix="/api/repairs")
from routes.notice_routes import notice_bp
app.register_blueprint(notice_bp, url_prefix="/api/notices")
from routes.auth_routes import auth_bp
app.register_blueprint(auth_bp, url_prefix="/api/auth")
from routes.dashboard_routes import dashboard_bp
app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")



# 你以后如果有新的模块，比如账单模块，就这样加：
# from routes.fee_routes import fee_bp
# app.register_blueprint(fee_bp, url_prefix='/api/fees')

if __name__ == '__main__':
    print("Backend running at http://127.0.0.1:5000")
    # 打印一下当前的路由映射，方便调试，看看接口有没有注册成功
    print(app.url_map) 
    app.run(debug=True, port=5000)