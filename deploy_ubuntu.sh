#!/bin/bash

# 测试管理系统部署脚本

set -e

# 变量定义
DOCKER_COMPOSE_FILE="docker-compose.yml"

# 开始
echo "�� 开始部署测试管理系统..."

# 配置Docker镜像源
echo "🔧 配置Docker镜像源..."
if [ -f "docker_env/daemon.json" ]; then
    echo "📁 创建Docker配置目录..."
    sudo mkdir -p /etc/docker
    
    if [ ! -f "/etc/docker/daemon.json" ]; then
        echo "📋 复制Docker配置文件..."
        sudo cp -f docker_env/daemon.json /etc/docker/daemon.json
        
        echo "✅ Docker镜像源配置完成"
        echo "🔄 重启Docker服务以应用新配置..."
        sudo systemctl restart docker
        echo "⏳ 等待Docker服务重启..."
        sleep 5
    else
        echo "ℹ️ /etc/docker/daemon.json 已存在，跳过配置"
    fi
else
    echo "⚠️ 未找到 docker_env/daemon.json 文件，使用默认配置"
fi

# 检查Docker和Docker Compose是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi


# 确保Docker运行
echo "📦 检查并启动Docker..."
if ! docker info &> /dev/null; then
    echo "🔄 Docker 未运行，正在启动..."
    open -a Docker
    echo "⏳ 等待Docker启动..."
    sleep 15
    
    # 等待Docker完全启动
    max_attempts=30
    attempt=1
    while [ $attempt -le $max_attempts ]; do
        if docker info &> /dev/null; then
            echo "✅ Docker 已启动"
            break
        else
            echo "⏳ 等待Docker启动... (${attempt}/${max_attempts})"
            sleep 2
            ((attempt++))
        fi
    done
    
    if [ $attempt -gt $max_attempts ]; then
        echo "❌ Docker 启动失败，请手动启动 Docker Desktop"
        exit 1
    fi
else
    echo "✅ Docker 已在运行"
fi

# 预拉取基础镜像
echo "📥 检查并拉取基础镜像..."

# 检查并拉取 python 镜像（Alpine 版本）
if docker images python:3.9-alpine | grep -q "python"; then
    echo "✅ python:3.9-alpine 已存在"
else
    echo "⏳ 拉取 python:3.9-alpine..."
    docker pull python:3.9-alpine || echo "⚠️ python镜像拉取失败，将使用本地镜像"
fi

# 检查并拉取 node 镜像
if docker images node:18-alpine | grep -q "node"; then
    echo "✅ node:18-alpine 已存在"
else
    echo "⏳ 拉取 node:18-alpine..."
    docker pull node:18-alpine || echo "⚠️ node镜像拉取失败，将使用本地镜像"
fi

# 检查并拉取 nginx 镜像
if docker images nginx:alpine | grep -q "nginx"; then
    echo "✅ nginx:alpine 已存在"
else
    echo "⏳ 拉取 nginx:alpine..."
    docker pull nginx:alpine || echo "⚠️ nginx镜像拉取失败，将使用本地镜像"
fi

# 检查并拉取 mysql 镜像
if docker images mysql:8.0 | grep -q "mysql"; then
    echo "✅ mysql:8.0 已存在"
else
    echo "⏳ 拉取 mysql:8.0..."
    docker pull mysql:8.0 || echo "⚠️ mysql镜像拉取失败，将使用本地镜像"
fi

echo "✅ 基础镜像检查完成"

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p deployment/ssl
mkdir -p logs

# 停止现有容器（如果存在）
echo "🛑 停止现有容器..."
docker-compose down --remove-orphans || true

# 清理悬挂的镜像和容器
echo "🧹 清理无用的Docker资源..."
docker system prune -f

# 构建并启动服务
echo "🔨 构建并启动服务..."
docker-compose up --build -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 30

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose ps

# 等待数据库初始化
echo "⏳ 等待数据库初始化..."
sleep 10

# 获取本机IP地址
LOCAL_IP=$(hostname -I | awk '{print $1}')

# 检查后端健康状态
echo "🏥 检查后端健康状态..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if curl -f http://localhost:8000/health &> /dev/null; then
        echo "✅ 后端服务健康检查通过"
        break
    else
        echo "⏳ 等待后端服务启动... (${attempt}/${max_attempts})"
        sleep 5
        ((attempt++))
    fi
done

if [ $attempt -gt $max_attempts ]; then
    echo "❌ 后端服务启动失败"
    echo "📝 查看后端日志:"
    docker-compose logs backend
    exit 1
fi

# 检查前端是否可访问
echo "🌐 检查前端服务..."
if curl -f http://localhost:80 &> /dev/null; then
    echo "✅ 前端服务可访问"
else
    echo "⚠️ 前端服务可能还在启动中"
fi

echo ""
echo "🎉 部署完成！"
echo ""
echo "�� 访问地址:"
echo "   前端:"
echo "     本地访问: http://localhost:80"
echo "     网络访问: http://${LOCAL_IP}:80"
echo "   后端API:"
echo "     本地访问: http://localhost:8000"
echo "     网络访问: http://${LOCAL_IP}:8000"
echo "   API文档:"
echo "     本地访问: http://localhost:8000/docs"
echo "     网络访问: http://${LOCAL_IP}:8000/docs"
echo ""
echo "🗄️ 数据库信息:"
echo "   主机:"
echo "     本地访问: localhost:3306"
echo "     网络访问: ${LOCAL_IP}:3306"
echo "   数据库: miniprogram_manager"
echo "   用户名: app_user"
echo "   密码: app_password"
echo ""
echo "🔧 管理命令:"
echo "   查看日志: docker-compose logs"
echo "   停止服务: docker-compose down"
echo "   重启服务: docker-compose restart"
echo "   进入后端容器: docker-compose exec backend bash"
echo "   进入数据库: docker-compose exec mysql mysql -u app_user -p miniprogram_manager"
echo ""
echo "📊 监控命令:"
echo "   查看服务状态: docker-compose ps"
echo "   查看资源使用: docker stats"
echo "" 