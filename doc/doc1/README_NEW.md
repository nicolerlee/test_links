# 页面
## manage.html: 
展示所有小程序，可以查看，新建，删除，编辑小程序


### 总体展示，
1. 按category分tab展示，比如影视，小说。 每个tab下展示对应的小程序列表
2. 每条小程序，都有两个按钮：查看，删除，编辑。
   
### 编辑   
1. 点击编辑，跳转到对应的edit.html页面
2. 点击查看，点击跳转到对应view.html页面
3. 点击删除，删除掉该小程序

### 新建
1. 右上角有设置按钮
1. 设置按钮展开，有一个新建项； 点击新建会弹出新建一个小程序，如果分类不存在，可以新增一个；如果存在，则直接选中一个


## edit.html页面
1. 单个域名类型，参考 "编辑.png", 
2. 但是要把小程序的名称展示在页面顶部
3. 同时考虑下，如果有2个域名类型，这个页面要怎么展示
4. 可以允许新增一个域名类型


## view.html页面
1. 参考“查看.png”
2. 同时考虑下，如果有多个域名类型，这个页面要怎么展示


# 技术选型
方案一：现代化前后端分离（推荐）
Apply to db.svg
前端: Vue 3 + Element Plus + Vite
后端: FastAPI (Python) + SQLAlchemy + MySQL
部署: Docker + Nginx
优势：
Vue 3组合式API，开发效率高
Element Plus组件丰富，UI美观
FastAPI自动生成API文档，调试方便
类型安全，代码质量高
热重载，开发体验好


# 数据库设计

## 当前数据结构分析

### 现有文件结构：
- `config/category.json`: 分类配置
- `config/{category_id}.json`: 各分类下的小程序列表
- `data/{miniprogram_id}_domain.json`: 小程序域名配置
- `data/{miniprogram_id}_links.json`: 小程序链接数据

## 建议的数据库表结构

### 1. categories 分类表

```sql
CREATE TABLE categories (
    id VARCHAR(50) PRIMARY KEY COMMENT '分类ID',
    name VARCHAR(100) NOT NULL COMMENT '分类显示名称',
    description TEXT COMMENT '分类描述',
    sort_order INT DEFAULT 0 COMMENT '排序权重',
    status TINYINT DEFAULT 1 COMMENT '状态：1启用，0禁用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
);

-- 示例数据
INSERT INTO categories (id, name, description) VALUES 
('novel', '小说', '小说类小程序'),
('yingshi', '影视', '影视类小程序');
```

### 2. miniprograms 小程序表

```sql
CREATE TABLE miniprograms (
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
);

-- 示例数据
INSERT INTO miniprograms (id, name, category_id) VALUES
('novel_kuaishou', 'H5小说-快手', 'novel'),
('novel_douyin_qudu', 'H5小说-抖音-趣读', 'novel'),
('video_kuaishou', 'H5影视-快手', 'yingshi');
```

### 3. domain_configs 域名配置表

```sql
CREATE TABLE domain_configs (
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
);

-- 示例数据
INSERT INTO domain_configs (miniprogram_id, domain_type, test_domain, prod_domain, first_level, second_level, third_level, description) VALUES
('novel_douyin_qudu', 'default', 'https://noveltestqd.funshion.tv', 'https://novelqd.funshion.tv', 'tt', 'qudu', '', '默认访问域名'),
('novel_douyin_qudu', 'order', 'https://ordertest.funshion.tv', 'https://order.funshion.tv', 'tt', 'qudu', 'order', '订购页面域名'),
('novel_douyin_qudu', 'receive', 'https://receivetest.funshion.tv', 'https://receive.funshion.tv', 'tt', 'qudu', 'get', '领取页面域名');
```

**域名类型说明:**
- `default`: 默认访问域名，用于常规页面访问
- `order`: 订购页面域名，用于付费订购流程
- `receive`: 领取页面域名，用于免费领取流程  
- `pay`: 付费页面域名，用于支付相关页面
- `share`: 分享页面域名，用于分享传播
- `custom`: 自定义域名，用于特殊业务场景

### 4. links 链接表

```sql
CREATE TABLE links (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    miniprogram_id VARCHAR(100) NOT NULL COMMENT '小程序ID',
    title VARCHAR(500) NOT NULL COMMENT '链接标题',
    url TEXT NOT NULL COMMENT '链接URL',
    sort_order INT DEFAULT 0 COMMENT '排序权重',
    status TINYINT DEFAULT 1 COMMENT '状态：1启用，0禁用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    FOREIGN KEY (miniprogram_id) REFERENCES miniprograms(id) ON DELETE CASCADE,
    INDEX idx_miniprogram (miniprogram_id),
    INDEX idx_status (status),
    INDEX idx_sort (sort_order)
);

-- 示例数据
INSERT INTO links (miniprogram_id, title, url, sort_order) VALUES
('novel_douyin_qudu', '投流', '/pages/readerPage/readerPage?cartoon_id=1289686&coopCode=ad&microapp_id=awvsp11da3ibbszd&popularizeId=funtv&si=13023728&promotion_code=jlgg&promotion_ad_id=220480807&num=1', 1),
('video_kuaishou', '退出登录', '/pages/mine/mine', 1);
```

## 数据库关系说明

1. **categories → miniprograms**: 一对多关系
   - 一个分类可以包含多个小程序
   - 删除分类时级联删除相关小程序

2. **miniprograms → domain_configs**: 一对多关系
   - 每个小程序可以配置多种类型的域名（默认、订购、领取等）
   - 通过 miniprogram_id + domain_type 保证唯一性
   - 支持业务场景分离：订购流程用专用域名，提升转化率
   - 删除小程序时级联删除所有域名配置

3. **miniprograms → links**: 一对多关系
   - 每个小程序可以有多个链接
   - 删除小程序时级联删除所有链接

## 迁移建议

### 数据迁移步骤：
1. 创建数据库表结构
2. 读取现有JSON文件数据
3. 按照关系将数据插入到对应表中：
   - 分类数据：从 `config/category.json` 迁移到 `categories` 表
   - 小程序数据：从 `config/{category_id}.json` 迁移到 `miniprograms` 表
   - 域名数据：从 `data/{miniprogram_id}_domain.json` 迁移到 `domain_configs` 表（默认类型为 'default'）
   - 链接数据：从 `data/{miniprogram_id}_links.json` 迁移到 `links` 表
4. 验证数据完整性
5. 更新应用程序代码以使用数据库
6. 后续可根据业务需要为小程序添加其他类型域名配置

### 技术选型建议：
- **数据库**: MySQL 8.0+ 或 PostgreSQL 12+
- **ORM**: SQLAlchemy (Python) 或 直接使用原生SQL
- **连接池**: 使用数据库连接池提高性能
- **备份策略**: 定期数据备份和恢复测试