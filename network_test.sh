#!/bin/bash

echo "🔍 网络诊断工具"
echo "=================="

echo ""
echo "1. 检查网络接口..."
ifconfig | grep -A 3 "inet " | grep -E "(192\.168|en0|en1)"

echo ""
echo "2. 检查服务端口..."
echo "前端服务 (3000):"
lsof -i :3000
echo ""
echo "后端服务 (8000):"
lsof -i :8000

echo ""
echo "3. 测试本地连接..."
echo "测试前端:"
curl -s -o /dev/null -w "HTTP状态码: %{http_code}\n" http://localhost:3000
echo "测试后端:"
curl -s -o /dev/null -w "HTTP状态码: %{http_code}\n" http://localhost:8000/health

echo ""
echo "4. 测试IP连接..."
echo "测试前端 (IP):"
curl -s -o /dev/null -w "HTTP状态码: %{http_code}\n" http://192.168.0.183:3000
echo "测试后端 (IP):"
curl -s -o /dev/null -w "HTTP状态码: %{http_code}\n" http://192.168.0.183:8000/health

echo ""
echo "5. 检查防火墙状态..."
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

echo ""
echo "6. 网络连接测试..."
ping -c 3 192.168.0.183

echo ""
echo "✅ 诊断完成！"
echo ""
echo "💡 如果移动端仍然无法访问，请尝试："
echo "1. 确保移动端和PC在同一WiFi网络"
echo "2. 检查路由器设置，确保没有阻止设备间通信"
echo "3. 尝试重启路由器"
echo "4. 检查移动端是否有网络限制" 