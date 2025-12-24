-- =========================
-- Smart Community Database Init Script (Schema + Minimal Seed)
-- =========================

DROP DATABASE IF EXISTS smart_community;
CREATE DATABASE smart_community DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE smart_community;

-- =========================
-- 1. 基础资源类 (4张)
-- =========================

CREATE TABLE community_building (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    building_no VARCHAR(20) NOT NULL UNIQUE COMMENT '楼号，如 1栋',
    total_floors INT NOT NULL COMMENT '总层数',
    description VARCHAR(255) DEFAULT NULL COMMENT '描述',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='楼栋表';

CREATE TABLE community_unit (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    building_id BIGINT NOT NULL COMMENT '楼栋ID',
    unit_no VARCHAR(20) NOT NULL COMMENT '单元号，如 1单元',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_unit_building FOREIGN KEY (building_id) REFERENCES community_building(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY uk_building_unit (building_id, unit_no)
) ENGINE=InnoDB COMMENT='单元表';

CREATE TABLE community_room (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    unit_id BIGINT NOT NULL COMMENT '单元ID',
    room_no VARCHAR(20) NOT NULL COMMENT '房号，如 301',
    area DECIMAL(10,2) NOT NULL COMMENT '面积',
    layout VARCHAR(50) DEFAULT NULL COMMENT '户型，如 2室1厅',
    status ENUM('已售','未售') DEFAULT '未售' COMMENT '状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_room_unit FOREIGN KEY (unit_id) REFERENCES community_unit(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY uk_unit_room (unit_id, room_no)
) ENGINE=InnoDB COMMENT='房屋表';

CREATE TABLE parking_space (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    space_no VARCHAR(30) NOT NULL UNIQUE COMMENT '车位号',
    status ENUM('闲置','已租','已售') DEFAULT '闲置' COMMENT '状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='车位表';

-- =========================
-- 2. 人员与资产类 (3张)
-- =========================

CREATE TABLE owner_info (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    phone VARCHAR(20) NOT NULL UNIQUE COMMENT '电话',
    id_card VARCHAR(30) NOT NULL UNIQUE COMMENT '身份证号',
    move_in_date DATE DEFAULT NULL COMMENT '入住时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='业主信息表';

CREATE TABLE owner_room_rel (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    owner_id BIGINT NOT NULL COMMENT '业主ID',
    room_id BIGINT NOT NULL COMMENT '房屋ID',
    rel_type ENUM('户主','租客') DEFAULT '户主' COMMENT '关系类型',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_rel_owner FOREIGN KEY (owner_id) REFERENCES owner_info(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_rel_room FOREIGN KEY (room_id) REFERENCES community_room(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY uk_owner_room (owner_id, room_id)
) ENGINE=InnoDB COMMENT='业主-房屋关联表';

CREATE TABLE parking_usage (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    space_id BIGINT NOT NULL COMMENT '车位ID',
    owner_id BIGINT NOT NULL COMMENT '业主ID',
    plate_no VARCHAR(20) NOT NULL COMMENT '车牌号',
    expire_date DATE DEFAULT NULL COMMENT '到期时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_usage_space FOREIGN KEY (space_id) REFERENCES parking_space(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_usage_owner FOREIGN KEY (owner_id) REFERENCES owner_info(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_plate_no (plate_no)
) ENGINE=InnoDB COMMENT='车位使用表';

-- =========================
-- 3. 核心业务类 (3张)
-- =========================

CREATE TABLE fee_type (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE COMMENT '名称：物业费/水费/停车费',
    unit_price DECIMAL(10,2) NOT NULL COMMENT '单价',
    unit VARCHAR(20) NOT NULL COMMENT '单位，如 元/㎡、元/吨',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='费用类型表';

CREATE TABLE fee_bill (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    owner_id BIGINT NOT NULL COMMENT '业主ID',
    fee_type_id BIGINT NOT NULL COMMENT '费用类型ID',
    amount DECIMAL(10,2) NOT NULL COMMENT '金额',
    bill_month CHAR(7) NOT NULL COMMENT '账单月份，如 2025-12',
    status ENUM('未缴','已缴') DEFAULT '未缴' COMMENT '状态',
    pay_time DATETIME DEFAULT NULL COMMENT '支付时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_bill_owner FOREIGN KEY (owner_id) REFERENCES owner_info(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_bill_feetype FOREIGN KEY (fee_type_id) REFERENCES fee_type(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_owner_month (owner_id, bill_month),
    INDEX idx_status (status)
) ENGINE=InnoDB COMMENT='账单表';

CREATE TABLE repair_request (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    owner_id BIGINT NOT NULL COMMENT '业主ID',
    content TEXT NOT NULL COMMENT '报修内容',
    submit_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
    status ENUM('待处理','处理中','完成') DEFAULT '待处理' COMMENT '状态',
    feedback TEXT DEFAULT NULL COMMENT '维修反馈',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_repair_owner FOREIGN KEY (owner_id) REFERENCES owner_info(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_repair_status (status)
) ENGINE=InnoDB COMMENT='报修工单表';

-- =========================
-- 4. 系统管理类 (2张)
-- =========================

CREATE TABLE sys_user (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    password VARCHAR(255) NOT NULL COMMENT '密码（建议存 hash）',
    role ENUM('admin','staff') DEFAULT 'admin' COMMENT '角色',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='系统用户表';

CREATE TABLE sys_notice (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL COMMENT '标题',
    content TEXT NOT NULL COMMENT '内容',
    publish_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '发布时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_publish_time (publish_time)
) ENGINE=InnoDB COMMENT='公告表';

-- =========================
-- Minimal Seed Data (必须)
-- =========================

INSERT INTO sys_user (username, password, role) VALUES
('admin', '123456', 'admin');

INSERT INTO fee_type (name, unit_price, unit) VALUES
('物业费', 2.50, '元/㎡'),
('水费', 3.00, '元/吨'),
('停车费', 300.00, '元/月');

-- =========================
-- END
-- =========================
