#!/bin/bash

echo "🚀 启动小程序管理系统（本地模式）..."

# 确保MySQL容器运行
echo "📦 启动MySQL数据库..."
docker-compose up -d mysql

# 等待数据库启动
echo "⏳ 等待数据库启动..."
sleep 10

# 检查Python环境
if command -v python3 &> /dev/null; then
    echo "✅ Python3 已安装"
else
    echo "❌ 请先安装 Python3"
    exit 1
fi

# 检查Node.js环境
if command -v node &> /dev/null; then
    echo "✅ Node.js 已安装"
else
    echo "❌ 请先安装 Node.js"
    exit 1
fi

echo ""
echo "📋 启动说明："
echo "1. 数据库已启动在端口 3307"
echo "2. 手动启动后端：cd backend && source venv/bin/activate && python main.py"
echo "3. 手动启动前端：cd .. && cd frontend && npm install && npm run dev"
echo ""
echo "🔗 访问地址："
echo "   前端: http://localhost:3000"  
echo "   后端: http://localhost:8000"
echo "   数据库: localhost:3307"
echo ""
echo "💡 提示：在两个终端窗口中分别运行后端和前端命令" 