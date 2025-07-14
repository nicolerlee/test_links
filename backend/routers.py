from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import schemas
import crud
from database import get_db

# 创建路由器
categories_router = APIRouter(prefix="/api/categories", tags=["categories"])
miniprograms_router = APIRouter(prefix="/api/miniprograms", tags=["miniprograms"])
domain_configs_router = APIRouter(prefix="/api/domain-configs", tags=["domain-configs"])
links_router = APIRouter(prefix="/api/links", tags=["links"])

# 分类路由
@categories_router.get("/", response_model=List[schemas.Category])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取所有分类"""
    categories = crud.CategoryCRUD.get_categories(db, skip=skip, limit=limit)
    return categories

@categories_router.get("/{category_id}", response_model=schemas.CategoryWithMiniprograms)
def get_category(category_id: str, db: Session = Depends(get_db)):
    """获取单个分类及其小程序"""
    category = crud.CategoryCRUD.get_category_with_miniprograms(db, category_id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="分类不存在")
    return category

@categories_router.post("/", response_model=schemas.Category, status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """创建新分类"""
    # 检查分类ID是否已存在
    db_category = crud.CategoryCRUD.get_category(db, category_id=category.id)
    if db_category:
        raise HTTPException(status_code=400, detail="分类ID已存在")
    return crud.CategoryCRUD.create_category(db=db, category=category)

@categories_router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: str, category_update: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    """更新分类"""
    db_category = crud.CategoryCRUD.update_category(db, category_id=category_id, category_update=category_update)
    if db_category is None:
        raise HTTPException(status_code=404, detail="分类不存在")
    return db_category

@categories_router.delete("/{category_id}")
def delete_category(category_id: str, db: Session = Depends(get_db)):
    """删除分类"""
    success = crud.CategoryCRUD.delete_category(db, category_id=category_id)
    if not success:
        raise HTTPException(status_code=404, detail="分类不存在")
    return {"message": "分类删除成功"}

# 小程序路由
@miniprograms_router.get("/", response_model=List[schemas.Miniprogram])
def get_miniprograms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取所有小程序"""
    miniprograms = crud.MiniprogramCRUD.get_miniprograms(db, skip=skip, limit=limit)
    return miniprograms

@miniprograms_router.get("/{miniprogram_id}", response_model=schemas.Miniprogram)
def get_miniprogram(miniprogram_id: str, db: Session = Depends(get_db)):
    """获取单个小程序"""
    miniprogram = crud.MiniprogramCRUD.get_miniprogram(db, miniprogram_id=miniprogram_id)
    if miniprogram is None:
        raise HTTPException(status_code=404, detail="小程序不存在")
    return miniprogram

@miniprograms_router.get("/category/{category_id}", response_model=List[schemas.Miniprogram])
def get_miniprograms_by_category(category_id: str, db: Session = Depends(get_db)):
    """根据分类获取小程序"""
    miniprograms = crud.MiniprogramCRUD.get_miniprograms_by_category(db, category_id=category_id)
    return miniprograms

@miniprograms_router.post("/", response_model=schemas.Miniprogram, status_code=status.HTTP_201_CREATED)
def create_miniprogram(miniprogram: schemas.MiniprogramCreate, db: Session = Depends(get_db)):
    """创建新小程序"""
    # 检查小程序ID是否已存在
    db_miniprogram = crud.MiniprogramCRUD.get_miniprogram(db, miniprogram_id=miniprogram.id)
    if db_miniprogram:
        raise HTTPException(status_code=400, detail="小程序ID已存在")
    
    # 检查分类是否存在
    db_category = crud.CategoryCRUD.get_category(db, category_id=miniprogram.category_id)
    if not db_category:
        raise HTTPException(status_code=400, detail="分类不存在")
    
    return crud.MiniprogramCRUD.create_miniprogram(db=db, miniprogram=miniprogram)

@miniprograms_router.put("/{miniprogram_id}", response_model=schemas.Miniprogram)
def update_miniprogram(miniprogram_id: str, miniprogram_update: schemas.MiniprogramUpdate, db: Session = Depends(get_db)):
    """更新小程序"""
    # 如果要更新分类，检查分类是否存在
    if miniprogram_update.category_id:
        db_category = crud.CategoryCRUD.get_category(db, category_id=miniprogram_update.category_id)
        if not db_category:
            raise HTTPException(status_code=400, detail="分类不存在")
    
    db_miniprogram = crud.MiniprogramCRUD.update_miniprogram(db, miniprogram_id=miniprogram_id, miniprogram_update=miniprogram_update)
    if db_miniprogram is None:
        raise HTTPException(status_code=404, detail="小程序不存在")
    return db_miniprogram

@miniprograms_router.delete("/{miniprogram_id}")
def delete_miniprogram(miniprogram_id: str, db: Session = Depends(get_db)):
    """删除小程序"""
    success = crud.MiniprogramCRUD.delete_miniprogram(db, miniprogram_id=miniprogram_id)
    if not success:
        raise HTTPException(status_code=404, detail="小程序不存在")
    return {"message": "小程序删除成功"}

# 域名配置路由
@domain_configs_router.get("/miniprogram/{miniprogram_id}", response_model=List[schemas.DomainConfig])
def get_domain_configs_by_miniprogram(miniprogram_id: str, db: Session = Depends(get_db)):
    """获取小程序的所有域名配置"""
    configs = crud.DomainConfigCRUD.get_domain_configs_by_miniprogram(db, miniprogram_id=miniprogram_id)
    return configs

@domain_configs_router.get("/{config_id}", response_model=schemas.DomainConfig)
def get_domain_config(config_id: int, db: Session = Depends(get_db)):
    """获取单个域名配置"""
    config = crud.DomainConfigCRUD.get_domain_config(db, config_id=config_id)
    if config is None:
        raise HTTPException(status_code=404, detail="域名配置不存在")
    return config

@domain_configs_router.post("/", response_model=schemas.DomainConfig, status_code=status.HTTP_201_CREATED)
def create_domain_config(domain_config: schemas.DomainConfigCreate, db: Session = Depends(get_db)):
    """创建域名配置"""
    # 检查小程序是否存在
    db_miniprogram = crud.MiniprogramCRUD.get_miniprogram(db, miniprogram_id=domain_config.miniprogram_id)
    if not db_miniprogram:
        raise HTTPException(status_code=400, detail="小程序不存在")
    
    # 检查同一小程序下是否已存在相同类型的域名配置
    existing_config = crud.DomainConfigCRUD.get_domain_config_by_type(
        db, miniprogram_id=domain_config.miniprogram_id, domain_type=domain_config.domain_type
    )
    if existing_config:
        raise HTTPException(status_code=400, detail="该小程序已存在此类型的域名配置")
    
    return crud.DomainConfigCRUD.create_domain_config(db=db, domain_config=domain_config)

@domain_configs_router.put("/{config_id}", response_model=schemas.DomainConfig)
def update_domain_config(config_id: int, config_update: schemas.DomainConfigUpdate, db: Session = Depends(get_db)):
    """更新域名配置"""
    db_config = crud.DomainConfigCRUD.update_domain_config(db, config_id=config_id, config_update=config_update)
    if db_config is None:
        raise HTTPException(status_code=404, detail="域名配置不存在")
    return db_config

@domain_configs_router.delete("/{config_id}")
def delete_domain_config(config_id: int, db: Session = Depends(get_db)):
    """删除域名配置"""
    success = crud.DomainConfigCRUD.delete_domain_config(db, config_id=config_id)
    if not success:
        raise HTTPException(status_code=404, detail="域名配置不存在")
    return {"message": "域名配置删除成功"}

# 链接路由
@links_router.get("/miniprogram/{miniprogram_id}", response_model=List[schemas.Link])
def get_links_by_miniprogram(miniprogram_id: str, db: Session = Depends(get_db)):
    """获取小程序的所有链接"""
    links = crud.LinkCRUD.get_links_by_miniprogram(db, miniprogram_id=miniprogram_id)
    return links

@links_router.get("/{link_id}", response_model=schemas.Link)
def get_link(link_id: int, db: Session = Depends(get_db)):
    """获取单个链接"""
    link = crud.LinkCRUD.get_link(db, link_id=link_id)
    if link is None:
        raise HTTPException(status_code=404, detail="链接不存在")
    return link

@links_router.post("/", response_model=schemas.Link, status_code=status.HTTP_201_CREATED)
def create_link(link: schemas.LinkCreate, db: Session = Depends(get_db)):
    """创建链接"""
    # 检查小程序是否存在
    db_miniprogram = crud.MiniprogramCRUD.get_miniprogram(db, miniprogram_id=link.miniprogram_id)
    if not db_miniprogram:
        raise HTTPException(status_code=400, detail="小程序不存在")
    
    return crud.LinkCRUD.create_link(db=db, link=link)

@links_router.put("/{link_id}", response_model=schemas.Link)
def update_link(link_id: int, link_update: schemas.LinkUpdate, db: Session = Depends(get_db)):
    """更新链接"""
    db_link = crud.LinkCRUD.update_link(db, link_id=link_id, link_update=link_update)
    if db_link is None:
        raise HTTPException(status_code=404, detail="链接不存在")
    return db_link

@links_router.delete("/{link_id}")
def delete_link(link_id: int, db: Session = Depends(get_db)):
    """删除链接"""
    success = crud.LinkCRUD.delete_link(db, link_id=link_id)
    if not success:
        raise HTTPException(status_code=404, detail="链接不存在")
    return {"message": "链接删除成功"} 