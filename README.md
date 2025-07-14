# 小程序管理系统

一个现代化的小程序链接管理系统，支持小程序的分类管理、域名配置和链接管理。

## 功能特性

- 📱 小程序分类管理
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