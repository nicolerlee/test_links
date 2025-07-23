# 测试link系统

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

### 安装Docker (Ubuntu)

如果系统未安装Docker，请按以下步骤安装：

```bash
# 1. 更新系统包
sudo apt update

# 2. 安装必要的依赖包
sudo apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# 3. 添加阿里云Docker GPG密钥
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring-aliyun.gpg

# 4. 添加阿里云Docker软件源
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring-aliyun.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. 安装Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 5.1 安装docker-compose
sudo apt install docker-compose

# 6. 启动Docker服务
sudo systemctl start docker
sudo systemctl enable docker

# 7. 配置用户权限（可选）
sudo usermod -aG docker $USER
newgrp docker

# 8. 验证安装
docker --version
docker-compose --version
```

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
# 启动所有服务
docker-compose up -d
# 停止所有服务
docker-compose stop
# 停止并删除容器
docker-compose down
# 查看服务状态
docker-compose ps
# 查看服务日志
docker-compose logs
# 重新构建并启动
docker-compose up --build -d
```

## API文档

启动后端服务后，访问 http://localhost:8000/docs 查看自动生成的API文档。

## 页面说明

- `/manage` - 主管理页面，展示所有小程序
- `/edit/:id` - 编辑小程序页面
- `/view/:id` - 查看小程序详情页面