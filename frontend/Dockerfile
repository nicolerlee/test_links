# 构建阶段
FROM node:18-alpine as build-stage

WORKDIR /app

# 复制包文件（放在代码复制之前，利用缓存）
COPY package*.json ./

# 安装依赖（构建阶段需要所有依赖，包括开发依赖）
RUN npm ci

# 复制源代码
COPY . .

# 构建应用
RUN npm run build

# 生产阶段
FROM nginx:alpine as production-stage

# 复制构建结果
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 复制nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 启动nginx
CMD ["nginx", "-g", "daemon off;"] 