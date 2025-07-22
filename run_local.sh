#!/bin/bash

# 测试链接系统 - 本地启动脚本
# 由于 Docker 下载依赖较慢，采用折衷方案：
# 1. backend 和 frontend 运行在本地
# 2. mysql 运行在 Docker 上

echo "🚀 测试管理系统 - 本地启动脚本"
echo ""

# 检查是否为首次安装
if [ ! -d "backend/venv" ] || [ ! -d "frontend/node_modules" ]; then
    echo "📦 检测到首次安装，开始环境配置..."
    echo ""
    
    # ==================== 首次安装部分 ====================
    
    # 确保Docker运行
    echo "📦 启动Docker..."
    open -a Docker
    echo "⏳ 等待Docker启动..."
    sleep 10
    
    # 检查Python环境（后端使用）
    if command -v python3 &> /dev/null; then
        echo "✅ Python3 已安装"
    else
        echo "❌ 请先安装 Python3"
        echo "   推荐使用 Homebrew: brew install python3"
        exit 1
    fi
    
    # 检查Node.js环境（前端使用）
    if command -v node &> /dev/null; then
        echo "✅ Node.js 已安装"
    else
        echo "❌ 请先安装 Node.js"
        echo "   推荐使用 Homebrew: brew install node"
        exit 1
    fi
    
    # 启动数据库
    echo "🚀 启动数据库..."
    docker-compose up -d mysql
    echo "⏳ 等待数据库启动..."
    sleep 10
    
    # 创建后端虚拟环境
    echo "🐍 配置后端环境..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    
    # 安装前端依赖
    echo "📦 配置前端环境..."
    cd frontend
    npm install
    cd ..
    
    echo ""
    echo "✅ 首次安装完成！"
    echo ""
    
else
    echo "✅ 检测到已安装环境，直接启动服务..."
    echo ""
    
    # ==================== 后续运行部分 ====================
    
    # 确保Docker运行
    echo "📦 启动Docker..."
    open -a Docker
    echo "⏳ 等待Docker启动..."
    sleep 10
    
    # 启动数据库
    echo "🚀 启动数据库..."
    docker-compose up -d mysql
    echo "⏳ 等待数据库启动..."
    sleep 10
fi

# ==================== 启动服务部分 ====================

echo ""
echo "📋 启动说明："
echo "1. 数据库已启动在端口 3307"
echo ""
echo "2. 手动启动后端（新终端窗口）："
echo "   cd backend && source venv/bin/activate && python main.py"
echo ""
echo "3. 手动启动前端（新终端窗口）："
echo "   cd frontend && npm run dev"
echo ""
echo "🔗 访问地址："
echo "   前端: http://localhost:3000"  
echo "   后端: http://localhost:8000"
echo "   数据库: localhost:3307"
echo ""
echo "💡 提示："
echo "   - 需要在两个终端窗口中分别运行后端和前端命令"
echo "   - 如果遇到依赖问题，请重新运行此脚本"
echo ""
echo "🔧 管理命令："
echo "   停止数据库: docker-compose down"
echo "   查看数据库日志: docker-compose logs mysql"
echo "   进入数据库: docker-compose exec mysql mysql -u app_user -p miniprogram_manager"
echo "   重新安装环境: rm -rf backend/venv frontend/node_modules && ./run_local.sh" 