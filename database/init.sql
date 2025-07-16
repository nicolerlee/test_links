-- 创建数据库
CREATE DATABASE IF NOT EXISTS miniprogram_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE miniprogram_manager;

-- 分类表
CREATE TABLE IF NOT EXISTS categories (
    id VARCHAR(50) PRIMARY KEY COMMENT '分类ID',
    name VARCHAR(100) NOT NULL COMMENT '分类显示名称',
    description TEXT COMMENT '分类描述',
    sort_order INT DEFAULT 0 COMMENT '排序权重',
    status TINYINT DEFAULT 1 COMMENT '状态：1启用，0禁用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='分类表';

-- 小程序表
CREATE TABLE IF NOT EXISTS miniprograms (
    id VARCHAR(100) PRIMARY KEY COMMENT '小程序ID',
    name VARCHAR(200) NOT NULL COMMENT '小程序显示名称',
    category_id VARCHAR(50) NOT NULL COMMENT '分类ID',
    description TEXT COMMENT '小程序描述',
    status TINYINT DEFAULT 1 COMMENT '状态：1启用，0禁用',
    sort_order INT DEFAULT 0 COMMENT '排序权重',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    INDEX idx_category (category_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='小程序表';

-- 域名配置表
CREATE TABLE IF NOT EXISTS domain_configs (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    miniprogram_id VARCHAR(100) NOT NULL COMMENT '小程序ID',
    domain_type VARCHAR(50) NOT NULL COMMENT '域名类型：default(默认), order(订购), receive(领取), pay(付费)等',
    test_domain VARCHAR(500) COMMENT '测试环境域名',
    prod_domain VARCHAR(500) COMMENT '正式环境域名',
    first_level VARCHAR(100) COMMENT '一级目录',
    second_level VARCHAR(100) COMMENT '二级目录',
    third_level VARCHAR(100) COMMENT '三级目录',
    description VARCHAR(200) COMMENT '域名用途描述',
    status TINYINT DEFAULT 1 COMMENT '状态：1启用，0禁用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    FOREIGN KEY (miniprogram_id) REFERENCES miniprograms(id) ON DELETE CASCADE,
    UNIQUE KEY uk_miniprogram_domain_type (miniprogram_id, domain_type),
    INDEX idx_miniprogram (miniprogram_id),
    INDEX idx_domain_type (domain_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='域名配置表';

-- 域名类型表
CREATE TABLE IF NOT EXISTS domain_types (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    miniprogram_id VARCHAR(100) NOT NULL COMMENT '小程序ID',
    domain_type VARCHAR(50) NOT NULL COMMENT '域名类型：default(默认), order(订购), receive(领取), pay(付费)等',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    FOREIGN KEY (miniprogram_id) REFERENCES miniprograms(id) ON DELETE CASCADE,
    UNIQUE KEY uk_miniprogram_domain_type (miniprogram_id, domain_type),
    INDEX idx_miniprogram (miniprogram_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='域名类型表';

-- 链接表
CREATE TABLE IF NOT EXISTS links (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    miniprogram_id VARCHAR(100) NOT NULL COMMENT '小程序ID',
    title VARCHAR(500) NOT NULL COMMENT '链接标题',
    url TEXT NOT NULL COMMENT '链接URL',
    domain_type VARCHAR(50) COMMENT '域名类型',
    sort_order INT DEFAULT 0 COMMENT '排序权重',
    status TINYINT DEFAULT 1 COMMENT '状态：1启用，0禁用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    FOREIGN KEY (miniprogram_id) REFERENCES miniprograms(id) ON DELETE CASCADE,
    INDEX idx_miniprogram (miniprogram_id),
    INDEX idx_status (status),
    INDEX idx_sort (sort_order),
    INDEX idx_domain_type (domain_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='链接表';

-- 插入示例数据
-- 分类数据
INSERT INTO categories (id, name, description) VALUES 
('novel', '小说', '小说类小程序'),
('yingshi', '影视', '影视类小程序');

-- 小程序数据
INSERT INTO miniprograms (id, name, category_id) VALUES
('novel_kuaishou', 'H5小说-快手', 'novel'),
('novel_douyin_qudu', 'H5小说-抖音-趣读', 'novel'),
('video_kuaishou', 'H5影视-快手', 'yingshi');

-- 域名配置数据
INSERT INTO domain_configs (miniprogram_id, domain_type, test_domain, prod_domain, first_level, second_level, third_level, description) VALUES
('novel_douyin_qudu', 'default', 'https://noveltestqd.funshion.tv', 'https://novelqd.funshion.tv', 'tt', 'qudu', '', '默认访问域名'),
('novel_douyin_qudu', 'order', 'https://ordertest.funshion.tv', 'https://order.funshion.tv', 'tt', 'qudu', 'order', '订购页面域名'),
('novel_douyin_qudu', 'receive', 'https://receivetest.funshion.tv', 'https://receive.funshion.tv', 'tt', 'qudu', 'get', '领取页面域名');

-- 域名类型数据
INSERT INTO domain_types (miniprogram_id, domain_type) VALUES
('novel_douyin_qudu', 'default'),
('novel_douyin_qudu', 'order'),
('novel_douyin_qudu', 'receive'),
('novel_kuaishou', 'default'),
('video_kuaishou', 'default');

-- 链接数据
INSERT INTO links (miniprogram_id, title, url, domain_type, sort_order) VALUES
('novel_douyin_qudu', '投流', '/pages/readerPage/readerPage?cartoon_id=1289686&coopCode=ad&microapp_id=awvsp11da3ibbszd&popularizeId=funtv&si=13023728&promotion_code=jlgg&promotion_ad_id=220480807&num=1', 'default', 1),
('video_kuaishou', '退出登录', '/pages/mine/mine', 'default', 1); 