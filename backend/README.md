# SmartCommunity Backend (Flask)

## 环境
Python 3.9+ / MySQL 8.x

## 初始化数据库 建库建表（在 backend 目录执行）
```bash
mysql -u root -p < scripts/init.sql
```

## 初始化演示/联调数据（可选）

```bash
python -m scripts.init_data
```

## 启动后端

```bash
pip install -r requirements.txt
python app.py
```
