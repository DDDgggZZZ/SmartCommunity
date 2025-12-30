from flask import Flask
from flask_cors import CORS

# 引入我们写好的路由蓝图
from routes.user_routes import user_bp
from routes.building_routes import building_bp

app = Flask(__name__)

# ★关键：解决跨域问题
CORS(app) 

# ★注册蓝图 (Register Blueprint)
# url_prefix 的意思是：这个蓝图下的所有接口，前面都自动加上 /api/users
# 所以访问地址依然是: http://127.0.0.1:5000/api/users/
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(building_bp, url_prefix="/api/buildings")

# 你以后如果有新的模块，比如账单模块，就这样加：
# from routes.fee_routes import fee_bp
# app.register_blueprint(fee_bp, url_prefix='/api/fees')

if __name__ == '__main__':
    print("Backend running at http://127.0.0.1:5000")
    # 打印一下当前的路由映射，方便调试，看看接口有没有注册成功
    print(app.url_map) 
    app.run(debug=True, port=5000)