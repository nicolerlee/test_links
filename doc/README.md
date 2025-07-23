# 测试管理系统

这是一个用于管理和分发不同版本小程序链接的系统。

## 功能特性

- �� 小程序分类管理
- 🔗 多域名类型配置（默认、订购、领取等）
- 📊 链接管理和展示
- 🎨 现代化响应式UI
- 🚀 前后端分离架构

## 技术栈

### 前端
- Vue 3 + Composition API
- Element Plus UI组件库
- Vite 构建工具
- Pinia 状态管理
- Vue Router 路由管理

### 后端
- FastAPI Python框架
- SQLAlchemy ORM
- MySQL 数据库
- Pydantic 数据验证

### 部署
- Docker 容器化
- Nginx 反向代理

## 项目结构

```
test_links/
├── frontend/          # Vue3前端应用
├── backend/           # FastAPI后端应用
├── database/          # 数据库相关文件
├── deployment/        # Docker部署配置
└── doc/              # 项目文档
```

## 快速开始

### 环境要求
- Node.js 18+
- Python 3.9+
- MySQL 8.0+
- Docker (可选)

### 后端启动

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

### 使用Docker

```bash
docker-compose up -d
```

## 数据库访问

### 访问Docker容器内部数据库

如果应用数据存储在Docker容器内部，可以通过以下方式访问：

#### 方法1：进入容器并连接MySQL
```bash
# 进入Docker容器并连接MySQL
docker exec -it miniprogram_mysql mysql -u root -ppassword

# 在容器内查看数据库
mysql> SHOW DATABASES;
mysql> USE miniprogram_manager;
mysql> SHOW TABLES;
mysql> SELECT * FROM miniprograms;
mysql> SELECT * FROM links;
```

#### 方法2：直接执行SQL命令
```bash
# 查看所有数据库
docker exec miniprogram_mysql mysql -u root -ppassword -e "SHOW DATABASES;"

# 查看特定数据库的表
docker exec miniprogram_mysql mysql -u root -ppassword -e "USE miniprogram_manager; SHOW TABLES;"

# 查询数据
docker exec miniprogram_mysql mysql -u root -ppassword -e "USE miniprogram_manager; SELECT * FROM miniprograms;"
```

#### 方法3：进入容器shell
```bash
# 进入容器shell
docker exec -it miniprogram_mysql bash

# 在容器内连接MySQL
mysql -u root -ppassword
```

#### 方法4：查看容器日志
```bash
# 查看MySQL容器日志
docker logs miniprogram_mysql
```

### 常用数据库查询

```sql
-- 查看所有小程序
SELECT * FROM miniprograms;

-- 查看特定小程序及其链接
SELECT m.name, c.name as category, l.title, l.url 
FROM miniprograms m 
LEFT JOIN categories c ON m.category_id = c.id 
LEFT JOIN links l ON m.id = l.miniprogram_id 
WHERE m.id = 'your_miniprogram_id';

-- 查看启用状态的链接
SELECT * FROM links WHERE status = 1;

-- 查看域名配置
SELECT * FROM domain_configs;
```

## API文档

启动后端服务后，访问 http://localhost:8000/docs 查看自动生成的API文档。

## 页面说明

- `/manage` - 主管理页面，展示所有小程序
- `/edit/:id` - 编辑小程序页面
- `/view/:id` - 查看小程序详情页面

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License 