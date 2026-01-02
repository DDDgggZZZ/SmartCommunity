# SmartCommunity Backend (Flask)

## 环境

Python 3.9+ / MySQL 8.x

## 初始化数据库 建库建表（在 backend 目录执行）

```
mysql -u root -p --default-character-set=utf8mb4 < scripts/init.sql
```

## 初始化演示/联调数据（可选）

```
python -m scripts.init_data
```

**先复制 backend/config.example.py 为 backend/config.py 并修改数据库配置。**

## 启动后端

```
pip install -r requirements.txt
python app.py
```

## 权限控制说明

后端登录接口会返回用户 role 字段（admin 或 staff）。
 权限控制由前端实现，前端根据 role 控制页面和按钮的显示。

建议规则：

- admin 可访问所有页面和操作
- staff 不可访问管理员管理，不可执行敏感操作（如新增管理员、删除公告等）

后端暂不做强制鉴权拦截，满足课程作业联调需求。

## 后端开发顺序（强一致依赖）

1. buildings
2. units
3. rooms
4. parkings/spaces
5. owners
6. owners bind room（owner_room_rel）
7. fee types
8. fee bills list/detail
9. generate bills
10. pay bill
11. repairs list/detail
12. submit repair
13. update repair status / finish
14. notices
15. auth login
16. dashboard stats

## 1.Building 楼栋模块

Base：`/api/buildings`

list：GET `/`
 data：`[{id, building_no, total_floors, description, created_at, updated_at}]`

detail：GET `/<id>`
 data：`{id, building_no, total_floors, description, created_at, updated_at}`

create：POST `/`
 body：`{building_no, total_floors, description}`
 data：`{inserted}`

update：PUT `/<id>`
 body：`{building_no, total_floors, description}`
 data：`{updated}`

delete：DELETE `/<id>`
 data：`{deleted}`

------

## 2.Unit 单元模块

Base：`/api/units`

list：GET `/`
 支持参数：`building_id`
 示例：GET `/?building_id=1`
 data：`[{id, building_id, unit_no, created_at, updated_at}]`

detail：GET `/<id>`
 data：`{id, building_id, unit_no, created_at, updated_at}`

create：POST `/`
 body：`{building_id, unit_no}`
 data：`{inserted}`

update：PUT `/<id>`
 body：`{building_id, unit_no}`
 data：`{updated}`

delete：DELETE `/<id>`
 data：`{deleted}`

------

## 3.Room 房屋模块

Base：`/api/rooms`

list：GET `/`
 支持参数：`unit_id`, `building_id`
 示例：

- GET `/`
- GET `/?unit_id=1`
- GET `/?building_id=1`
- GET `/?building_id=1&unit_id=2`

当同时传入 `building_id` 和 `unit_id` 时，后端会校验该 unit 是否属于该 building：
 若不属于返回：

```
{"code":400,"msg":"Unit Not In Building","data":[]}
```

data：`[{id, unit_id, room_no, area, layout, status, created_at, updated_at}]`

detail：GET `/<id>`
 data：`{id, unit_id, room_no, area, layout, status, created_at, updated_at}`

create：POST `/`
 body：`{unit_id, room_no, area, layout}`
 可选字段：`status`
 data：`{inserted}`

update：PUT `/<id>`
 body：`{unit_id, room_no, area, layout, status}`
 status 必须是 "已售" 或 "未售"
 data：`{updated}`

delete：DELETE `/<id>`
 data：`{deleted}`

------

## 4.Parking Space 车位模块

Base：`/api/parkings/spaces`

list：GET `/`
 支持参数：`status`
 示例：

- GET `/`
- GET `/?status=闲置`
- GET `/?status=已租`
- GET `/?status=已售`
   data：`[{id, space_no, status, created_at, updated_at}]`

detail：GET `/<id>`
 data：`{id, space_no, status, created_at, updated_at}`

create：POST `/`
 body：`{space_no, status}`
 status 可选，不传默认 "闲置"
 data：`{inserted}`

update：PUT `/<id>`
 body：`{space_no, status}`
 status 必须是 "闲置" 或 "已租" 或 "已售"
 data：`{updated}`

delete：DELETE `/<id>`
 data：`{deleted}`

------

## 5.Owners 业主模块

Base：`/api/owners`

list：GET `/`
 data：`[{id, name, phone, id_card, move_in_date, created_at, updated_at}]`

detail：GET `/<id>`
 data：`{id, name, phone, id_card, move_in_date, created_at, updated_at}`

create：POST `/`
 body：`{name, phone, id_card, move_in_date}`
 move_in_date 可选，格式 "YYYY-MM-DD"
 data：`{inserted}`

update：PUT `/<id>`
 body：`{name, phone, id_card, move_in_date}`
 move_in_date 可选，格式 "YYYY-MM-DD"
 data：`{updated}`

delete：DELETE `/<id>`
 data：`{deleted}`

------

## 6.Owners bind room 业主绑定房屋模块 (owner_room_rel)

Base：`/api/owners/bindings`

list：GET `/`
 支持参数：`owner_id`, `room_id`
 示例：

- GET `/`
- GET `/?owner_id=1`
- GET `/?room_id=3`
- GET `/?owner_id=1&room_id=3`
   data：`[{id, owner_id, room_id, rel_type, created_at, updated_at}]`

detail：GET `/<id>`
 data：`{id, owner_id, room_id, rel_type, created_at, updated_at}`

create：POST `/`
 body：`{owner_id, room_id, rel_type}`
 rel_type 必须是 "户主" 或 "租客"
 data：`{inserted}`

update：PUT `/<id>`
 body：`{rel_type}`
 update 仅修改 rel_type，不修改 owner_id 和 room_id
 rel_type 必须是 "户主" 或 "租客"
 data：`{updated}`

delete：DELETE `/<id>`
 data：`{deleted}`

------

## 7.Fee Types 费用类型模块

Base：`/api/fees/types`

list：GET `/`
 data：`[{id, name, unit_price, unit, created_at, updated_at}]`

detail：GET `/<id>`
 data：`{id, name, unit_price, unit, created_at, updated_at}`

create：POST `/`
 body：`{name, unit_price, unit}`
 data：`{inserted}`

update：PUT `/<id>`
 body：`{name, unit_price, unit}`
 data：`{updated}`

delete：DELETE `/<id>`
 data：`{deleted}`

------

## 8.Fee Bills List/Detail 账单查询模块

Base：`/api/fees/bills`

list：GET `/`
 支持参数：`owner_id`, `status`, `bill_month`
 示例：

- GET `/`
- GET `/?owner_id=1`
- GET `/?status=未缴`
- GET `/?bill_month=2026-01`
- GET `/?owner_id=1&status=未缴&bill_month=2026-01`

data：`[{id, owner_id, owner_name, owner_phone, fee_type_id, fee_type_name, amount, bill_month, status, pay_time, created_at, updated_at}]`

detail：GET `/<id>`
 data：`{id, owner_id, owner_name, owner_phone, fee_type_id, fee_type_name, amount, bill_month, status, pay_time, created_at, updated_at}`

------

## 9.Generate Bills 生成账单模块

Base：`/api/fees/bills/generate`

generate：POST `/`
 body：`{fee_type_id, bill_month}`
 bill_month 格式必须是 "YYYY-MM"
 data：`{created, skipped}`

------

## 10.Pay Bill 缴费模块

Base：`/api/fees/bills`

pay：PUT `/<id>/pay`
 body：`{pay_time}`
 pay_time 可选，不传则使用当前时间
 data：`{paid}`

------

## 11.Repairs List/Detail 报修查询模块

Base：`/api/repairs`

list：GET `/`
 支持参数：`owner_id`, `status`
 示例：

- GET `/`
- GET `/?status=待处理`
- GET `/?status=处理中`
- GET `/?status=完成`
- GET `/?owner_id=1`

data：`[{id, owner_id, owner_name, owner_phone, content, submit_time, status, feedback, updated_at}]`

detail：GET `/<id>`
 data：`{id, owner_id, owner_name, owner_phone, content, submit_time, status, feedback, updated_at}`

------

## 12.Submit Repair 业主提交报修模块

Base：`/api/repairs`

submit：POST `/`
 body：`{owner_id, content}`
 data：`{inserted}`

------

## 13.Update Repair Status / Finish 报修处理模块

Base：`/api/repairs`

update status：PUT `/<id>/status`
 body：`{status, feedback}`
 status 必须是 "待处理" 或 "处理中" 或 "完成"
 当 status="完成" 时 feedback 必填
 data：`{updated}`

------

## 14.Notices 公告模块

Base：`/api/notices`

list：GET `/`
 data：`[{id, title, content, publish_time, created_at, updated_at}]`

detail：GET `/<id>`
 data：`{id, title, content, publish_time, created_at, updated_at}`

create：POST `/`
 body：`{title, content, publish_time}`
 publish_time 可选，不传默认当前时间
 data：`{inserted}`

update：PUT `/<id>`
 body：`{title, content, publish_time}`
 data：`{updated}`

delete：DELETE `/<id>`
 data：`{deleted}`

------

## 15.Auth Login 管理员登录模块

Base：`/api/auth`

login：POST `/login`
 body：`{username, password}`
 data：`{id, username, role}`

users list：GET `/users`
 data：`[{id, username, role, created_at, updated_at}]`

users detail：GET `/users/<id>`
 data：`{id, username, role, created_at, updated_at}`

users create：POST `/users`
 body：`{username, password, role}`
 role 必须是 "admin" 或 "staff"
 data：`{inserted}`

users update：PUT `/users/<id>`
 body：`{password, role}`
 data：`{updated}`

users delete：DELETE `/users/<id>`
 data：`{deleted}`

------

## 16.Dashboard Stats 仪表盘统计模块

Base：`/api/dashboard`

stats：GET `/stats`
 data：`{buildings, units, rooms, owners, parking_spaces, fee_types, bills_total, bills_unpaid, repairs_total, repairs_pending, notices, sys_users}`