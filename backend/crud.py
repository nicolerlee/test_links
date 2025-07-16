from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from typing import List, Optional
import models
import schemas

# 分类CRUD操作
class CategoryCRUD:
    @staticmethod
    def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[models.Category]:
        return db.query(models.Category).order_by(models.Category.sort_order).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_category(db: Session, category_id: str) -> Optional[models.Category]:
        return db.query(models.Category).filter(models.Category.id == category_id).first()
    
    @staticmethod
    def get_category_with_miniprograms(db: Session, category_id: str) -> Optional[models.Category]:
        return db.query(models.Category).options(
            joinedload(models.Category.miniprograms).joinedload(models.Miniprogram.domain_configs),
            joinedload(models.Category.miniprograms).joinedload(models.Miniprogram.domain_types),
            joinedload(models.Category.miniprograms).joinedload(models.Miniprogram.links)
        ).filter(models.Category.id == category_id).first()
    
    @staticmethod
    def create_category(db: Session, category: schemas.CategoryCreate) -> models.Category:
        db_category = models.Category(**category.dict())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    
    @staticmethod
    def update_category(db: Session, category_id: str, category_update: schemas.CategoryUpdate) -> Optional[models.Category]:
        db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
        if db_category:
            update_data = category_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_category, field, value)
            db.commit()
            db.refresh(db_category)
        return db_category
    
    @staticmethod
    def delete_category(db: Session, category_id: str) -> bool:
        db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
        if db_category:
            db.delete(db_category)
            db.commit()
            return True
        return False

# 小程序CRUD操作
class MiniprogramCRUD:
    @staticmethod
    def get_miniprograms(db: Session, skip: int = 0, limit: int = 100) -> List[models.Miniprogram]:
        return db.query(models.Miniprogram).options(
            joinedload(models.Miniprogram.category),
            joinedload(models.Miniprogram.domain_configs),
            joinedload(models.Miniprogram.domain_types),
            joinedload(models.Miniprogram.links)
        ).order_by(models.Miniprogram.sort_order).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_miniprogram(db: Session, miniprogram_id: str) -> Optional[models.Miniprogram]:
        return db.query(models.Miniprogram).options(
            joinedload(models.Miniprogram.category),
            joinedload(models.Miniprogram.domain_configs),
            joinedload(models.Miniprogram.domain_types),
            joinedload(models.Miniprogram.links)
        ).filter(models.Miniprogram.id == miniprogram_id).first()
    
    @staticmethod
    def get_miniprograms_by_category(db: Session, category_id: str) -> List[models.Miniprogram]:
        return db.query(models.Miniprogram).options(
            joinedload(models.Miniprogram.domain_configs),
            joinedload(models.Miniprogram.domain_types),
            joinedload(models.Miniprogram.links)
        ).filter(models.Miniprogram.category_id == category_id).order_by(models.Miniprogram.sort_order).all()
    
    @staticmethod
    def create_miniprogram(db: Session, miniprogram: schemas.MiniprogramCreate) -> models.Miniprogram:
        db_miniprogram = models.Miniprogram(**miniprogram.dict())
        db.add(db_miniprogram)
        db.commit()
        db.refresh(db_miniprogram)
        return db_miniprogram
    
    @staticmethod
    def update_miniprogram(db: Session, miniprogram_id: str, miniprogram_update: schemas.MiniprogramUpdate) -> Optional[models.Miniprogram]:
        db_miniprogram = db.query(models.Miniprogram).filter(models.Miniprogram.id == miniprogram_id).first()
        if db_miniprogram:
            update_data = miniprogram_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_miniprogram, field, value)
            db.commit()
            db.refresh(db_miniprogram)
        return db_miniprogram
    
    @staticmethod
    def delete_miniprogram(db: Session, miniprogram_id: str) -> bool:
        db_miniprogram = db.query(models.Miniprogram).filter(models.Miniprogram.id == miniprogram_id).first()
        if db_miniprogram:
            db.delete(db_miniprogram)
            db.commit()
            return True
        return False

# 域名配置CRUD操作
class DomainConfigCRUD:
    @staticmethod
    def get_domain_configs_by_miniprogram(db: Session, miniprogram_id: str) -> List[models.DomainConfig]:
        return db.query(models.DomainConfig).filter(
            models.DomainConfig.miniprogram_id == miniprogram_id
        ).all()
    
    @staticmethod
    def get_domain_config(db: Session, config_id: int) -> Optional[models.DomainConfig]:
        return db.query(models.DomainConfig).filter(models.DomainConfig.id == config_id).first()
    
    @staticmethod
    def get_domain_config_by_type(db: Session, miniprogram_id: str, domain_type: str) -> Optional[models.DomainConfig]:
        return db.query(models.DomainConfig).filter(
            and_(
                models.DomainConfig.miniprogram_id == miniprogram_id,
                models.DomainConfig.domain_type == domain_type
            )
        ).first()
    
    @staticmethod
    def create_domain_config(db: Session, domain_config: schemas.DomainConfigCreate) -> models.DomainConfig:
        db_config = models.DomainConfig(**domain_config.dict())
        db.add(db_config)
        db.commit()
        db.refresh(db_config)
        return db_config
    
    @staticmethod
    def update_domain_config(db: Session, config_id: int, config_update: schemas.DomainConfigUpdate) -> Optional[models.DomainConfig]:
        db_config = db.query(models.DomainConfig).filter(models.DomainConfig.id == config_id).first()
        if db_config:
            update_data = config_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_config, field, value)
            db.commit()
            db.refresh(db_config)
        return db_config
    
    @staticmethod
    def delete_domain_config(db: Session, config_id: int) -> bool:
        db_config = db.query(models.DomainConfig).filter(models.DomainConfig.id == config_id).first()
        if db_config:
            db.delete(db_config)
            db.commit()
            return True
        return False

# 域名类型CRUD操作
class DomainTypeCRUD:
    @staticmethod
    def get_domain_types_by_miniprogram(db: Session, miniprogram_id: str) -> List[models.DomainType]:
        return db.query(models.DomainType).filter(
            models.DomainType.miniprogram_id == miniprogram_id
        ).all()
    
    @staticmethod
    def get_domain_type(db: Session, domain_type_id: int) -> Optional[models.DomainType]:
        return db.query(models.DomainType).filter(models.DomainType.id == domain_type_id).first()
    
    @staticmethod
    def get_domain_type_by_type(db: Session, miniprogram_id: str, domain_type: str) -> Optional[models.DomainType]:
        return db.query(models.DomainType).filter(
            and_(
                models.DomainType.miniprogram_id == miniprogram_id,
                models.DomainType.domain_type == domain_type
            )
        ).first()
    
    @staticmethod
    def create_domain_type(db: Session, domain_type: schemas.DomainTypeCreate) -> models.DomainType:
        db_domain_type = models.DomainType(**domain_type.dict())
        db.add(db_domain_type)
        db.commit()
        db.refresh(db_domain_type)
        return db_domain_type
    
    @staticmethod
    def update_domain_type(db: Session, domain_type_id: int, domain_type_update: schemas.DomainTypeUpdate) -> Optional[models.DomainType]:
        db_domain_type = db.query(models.DomainType).filter(models.DomainType.id == domain_type_id).first()
        if db_domain_type:
            update_data = domain_type_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_domain_type, field, value)
            db.commit()
            db.refresh(db_domain_type)
        return db_domain_type
    
    @staticmethod
    def delete_domain_type(db: Session, domain_type_id: int) -> bool:
        db_domain_type = db.query(models.DomainType).filter(models.DomainType.id == domain_type_id).first()
        if db_domain_type:
            db.delete(db_domain_type)
            db.commit()
            return True
        return False

# 链接CRUD操作
class LinkCRUD:
    @staticmethod
    def get_links_by_miniprogram(db: Session, miniprogram_id: str) -> List[models.Link]:
        return db.query(models.Link).filter(
            models.Link.miniprogram_id == miniprogram_id
        ).order_by(models.Link.sort_order).all()
    
    @staticmethod
    def get_link(db: Session, link_id: int) -> Optional[models.Link]:
        return db.query(models.Link).filter(models.Link.id == link_id).first()
    
    @staticmethod
    def create_link(db: Session, link: schemas.LinkCreate) -> models.Link:
        db_link = models.Link(**link.dict())
        db.add(db_link)
        db.commit()
        db.refresh(db_link)
        return db_link
    
    @staticmethod
    def update_link(db: Session, link_id: int, link_update: schemas.LinkUpdate) -> Optional[models.Link]:
        db_link = db.query(models.Link).filter(models.Link.id == link_id).first()
        if db_link:
            update_data = link_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_link, field, value)
            db.commit()
            db.refresh(db_link)
        return db_link
    
    @staticmethod
    def delete_link(db: Session, link_id: int) -> bool:
        db_link = db.query(models.Link).filter(models.Link.id == link_id).first()
        if db_link:
            db.delete(db_link)
            db.commit()
            return True
        return False 