# 手动在 Docker 中安装依赖

## 背景
`deploy.sh` 是全自动部署脚本，但每次构建时都会重新安装依赖，这个过程很慢（2-3分钟）。为了优化构建速度，可以手动在 Docker 中安装依赖，然后保存为预构建的基础镜像。

## 手动安装依赖流程

### 1. 启动临时容器
```bash
docker run -it --name temp-backend python:3.9-alpine sh
```

### 2. 配置 Alpine 镜像源（加速下载）
在容器内执行以下命令：

**选择其中一个镜像源：**

#### 中科大源（推荐）
```bash
echo "https://mirrors.ustc.edu.cn/alpine/v3.22/main" > /etc/apk/repositories
echo "https://mirrors.ustc.edu.cn/alpine/v3.22/community" >> /etc/apk/repositories
```

#### 阿里云源
```bash
echo "https://mirrors.aliyun.com/alpine/v3.22/main" > /etc/apk/repositories
echo "https://mirrors.aliyun.com/alpine/v3.22/community" >> /etc/apk/repositories
```

#### 清华大学源
```bash
echo "https://mirrors.tuna.tsinghua.edu.cn/alpine/v3.22/main" > /etc/apk/repositories
echo "https://mirrors.tuna.tsinghua.edu.cn/alpine/v3.22/community" >> /etc/apk/repositories
```

### 3. 更新包索引
```bash
apk update
```

### 4. 安装系统依赖
```bash
apk add --no-cache gcc musl-dev mariadb-dev pkgconfig curl
```

### 5. 复制项目文件到容器
在**新的终端窗口**执行：
```bash
docker cp backend/ temp-backend:/app/
```

### 6. 在容器内安装 Python 依赖
```bash
cd /app
pip install -r requirements.txt
```

### 7. 测试运行
```bash
python main.py
```

### 8. 退出容器
```bash
exit
```

### 9. 保存为新的基础镜像
```bash
docker commit temp-backend my-backend-with-deps
```

### 10. 修改 Dockerfile 使用新镜像
将 `backend/Dockerfile` 的第一行改为：
```dockerfile
FROM my-backend-with-deps
```

## 一键配置命令
如果想快速配置，可以复制粘贴这个命令：
```bash
echo "https://mirrors.ustc.edu.cn/alpine/v3.22/main" > /etc/apk/repositories && \
echo "https://mirrors.ustc.edu.cn/alpine/v3.22/community" >> /etc/apk/repositories && \
apk update && \
apk add --no-cache gcc musl-dev mariadb-dev pkgconfig curl
```

## 优势
- ✅ 避免每次构建时重新安装依赖
- ✅ 大幅提升构建速度
- ✅ 可以手动控制依赖安装过程
- ✅ 便于调试依赖问题

## 注意事项
- 确保容器名不冲突（如果已存在同名容器，先删除）
- 配置镜像源可以显著提升下载速度
- 保存的镜像会占用更多磁盘空间
