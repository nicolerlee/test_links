from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

from database import engine
import models
from routers import categories_router, miniprograms_router, domain_configs_router, links_router

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(
    title="测试管理系统 API",
    description="一个用于管理小程序链接和分类的API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(categories_router)
app.include_router(miniprograms_router)
app.include_router(domain_configs_router)
app.include_router(links_router)

# 根路径
@app.get("/", summary="API Root", tags=["Default"])
async def root():
    """
    API的根节点，返回一个欢迎信息。
    """
    return {"message": "测试管理系统 API"}

# 健康检查
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 启动服务器
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 