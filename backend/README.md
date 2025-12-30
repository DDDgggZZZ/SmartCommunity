# SmartCommunity Backend (Flask)

## 环境
Python 3.9+ / MySQL 8.x

## 初始化数据库 建库建表（在 backend 目录执行）
```bash
mysql -u root -p --default-character-set=utf8mb4 < scripts/init.sql
```

## 初始化演示/联调数据（可选）

```bash
## 执行下面这条命令如果提示没有安装某个库，就进行安装
python -m scripts.init_data
```

**先复制 backend/config.example.py 为 backend/config.py 并修改数据库配置。**
## 启动后端

```bash
pip install -r requirements.txt
python app.py
```
## Building 楼栋模块

Base：`/api/buildings`  
统一返回：`{"code":200,"msg":"success","data":...}`

list：GET `/` → data: `[{id, building_no, total_floors, description, created_at, updated_at}]`  
detail：GET `/<id>` → data: `{id, building_no, total_floors, description, created_at, updated_at}`  
create：POST `/` body `{building_no, total_floors, description}` → data: `{inserted}`  
update：PUT `/<id>` body `{building_no, total_floors, description}` → data: `{updated}`  
delete：DELETE `/<id>` → data: `{deleted}`
