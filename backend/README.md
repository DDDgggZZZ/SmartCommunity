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