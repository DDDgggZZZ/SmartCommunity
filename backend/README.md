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

## 启动后端

```bash
pip install -r requirements.txt
python app.py
```
