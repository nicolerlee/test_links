#!/bin/bash

# 小程序管理系统部署脚本

set -e

echo "🚀 开始部署小程序管理系统..."

# 检查Docker和Docker Compose是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

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
echo "📱 访问地址:"
echo "   前端: http://localhost:80"
echo "   后端API: http://localhost:8000"
echo "   API文档: http://localhost:8000/docs"
echo ""
echo "🗄️ 数据库信息:"
echo "   主机: localhost:3306"
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