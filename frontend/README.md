# frontend

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd) 
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```


# SmartCommunity 智慧社区管理系统

基于 **Flask (Python)** 和 **Vue.js** 开发的智慧社区管理系统。

## 环境要求

* **后端**: Python 3.9+
* **数据库**: MySQL 8.x
* **前端**: Node.js 16+, npm/yarn


## 快速启动

请打开两个终端窗口，分别启动后端和前端。

### 1. 数据库初始化

请确保 MySQL 服务已开启。在项目根目录（或 `backend` 目录）下执行：

```bash
# 1. 导入数据库结构
mysql -u root -p --default-character-set=utf8mb4 < backend/scripts/init.sql

# 2. (可选) 初始化演示/联调数据
# 注意：需确保处于后端虚拟环境中
python -m backend.scripts.init_data

```

### 2. 启动后端

在 **终端 1** 中操作：

```bash
cd backend

# 1. 配置数据库
# 复制 config.example.py 为 config.py，并修改其中的 DB_USER, DB_PASSWORD 等配置
cp config.example.py config.py

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动 Flask 服务
python app.py

```

> 后端默认运行在: `http://127.0.0.1:5000`

### 3. 启动前端

在 **终端 2** 中操作：

```bash
cd frontend

# 1. 安装依赖
npm install

# 2. 启动开发服务器
npm run dev

```

> 前端通常运行在: `http://localhost:5173` (具体见终端输出)

---

## 权限说明

后端登录接口会返回用户 `role` 字段（`admin` 或 `staff`）。权限控制主要由前端实现：

* **admin**: 可访问所有页面和操作。
* **staff**: 不可访问管理员管理，不可执行敏感操作（如新增管理员、删除公告等）。

> **注意**: 后端暂不做强制鉴权拦截，以满足课程作业联调需求