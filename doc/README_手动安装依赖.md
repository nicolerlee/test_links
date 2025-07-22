# 镜像源配置说明

## 概述

本项目配置了两层镜像源来加速依赖安装和镜像拉取：

1. **Docker镜像源** - 加速Docker镜像拉取
2. **Debian系统镜像源** - 加速容器内系统包安装

## 1. Docker镜像源配置

### 配置文件位置
`~/.docker/daemon.json`

### 配置内容
```json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com"
  ],
  "insecure-registries": [],
  "debug": false,
  "experimental": false
}
```

### 作用说明
- 加速Docker镜像的拉取速度
- 当你执行 `docker pull python:3.9-slim` 时生效
- 当你执行 `docker-compose up` 拉取基础镜像时生效
- 影响所有Docker镜像的下载速度

### 配置的镜像源
- **中科大镜像源**: `https://docker.mirrors.ustc.edu.cn`
- **网易镜像源**: `https://hub-mirror.c.163.com`
- **百度云镜像源**: `https://mirror.baidubce.com`

## 2. Debian系统镜像源配置

### 配置文件位置
`backend/Dockerfile`

### 配置内容
```dockerfile
# 配置apt镜像源（使用阿里云镜像源）
RUN echo "deb https://mirrors.aliyun.com/debian/ bookworm main" > /etc/apt/sources.list \
    && echo "deb https://mirrors.aliyun.com/debian/ bookworm-updates main" >> /etc/apt/sources.list \
    && echo "deb https://mirrors.aliyun.com/debian-security bookworm-security main" >> /etc/apt/sources.list \
    && echo "deb https://mirrors.aliyun.com/debian/ bookworm-backports main" >> /etc/apt/sources.list
```

### 作用说明
- 加速容器内Debian系统包的安装
- 当你执行 `apt-get install gcc` 时生效
- 当你执行 `apt-get update` 时生效
- 影响容器内Debian系统的包管理

### 配置的镜像源
- **阿里云Debian镜像源**: `https://mirrors.aliyun.com/debian/`

## 两种镜像源的区别

| 方面 | Docker镜像源 | Debian系统镜像源 |
|------|-------------|-----------------|
| **作用对象** | Docker镜像拉取 | 系统包安装 |
| **配置位置** | Docker daemon配置 | 容器内部配置 |
| **影响时机** | 构建时拉取基础镜像 | 构建时安装系统依赖 |
| **配置方式** | 全局配置 | 每个容器单独配置 |
| **示例场景** | `docker pull nginx` | `apt-get install curl` |

## 实际使用场景

### Docker镜像源使用场景
```bash
# 当执行这些命令时，会从配置的Docker镜像源拉取
docker pull python:3.9-slim
docker-compose up
docker build -t myapp .
```

### Debian镜像源使用场景
```dockerfile
# 在Dockerfile中执行这些命令时，会从配置的Debian镜像源下载包
RUN apt-get update
RUN apt-get install -y gcc default-libmysqlclient-dev pkg-config curl
```

## 配置验证

### 验证Docker镜像源
```bash
# 查看Docker daemon配置
docker info | grep -A 10 "Registry Mirrors"
```

### 验证Debian镜像源
```bash
# 进入容器查看镜像源配置
docker exec -it <container_name> cat /etc/apt/sources.list
```

## 注意事项

1. **Docker镜像源**是全局配置，影响所有Docker操作
2. **Debian镜像源**是容器内配置，只影响当前容器
3. 两者配合使用可以显著提升容器构建速度
4. 如果某个镜像源不可用，系统会自动回退到默认源
