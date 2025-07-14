from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(String(50), primary_key=True, comment="分类ID")
    name = Column(String(100), nullable=False, comment="分类显示名称")
    description = Column(Text, comment="分类描述")
    sort_order = Column(Integer, default=0, comment="排序权重")
    status = Column(Integer, default=1, comment="状态：1启用，0禁用")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    miniprograms = relationship("Miniprogram", back_populates="category", cascade="all, delete-orphan")

class Miniprogram(Base):
    __tablename__ = "miniprograms"
    
    id = Column(String(100), primary_key=True, comment="小程序ID")
    name = Column(String(200), nullable=False, comment="小程序显示名称")
    category_id = Column(String(50), ForeignKey("categories.id", ondelete="CASCADE"), nullable=False, comment="分类ID")
    description = Column(Text, comment="小程序描述")
    status = Column(Integer, default=1, comment="状态：1启用，0禁用")
    sort_order = Column(Integer, default=0, comment="排序权重")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    category = relationship("Category", back_populates="miniprograms")
    domain_configs = relationship("DomainConfig", back_populates="miniprogram", cascade="all, delete-orphan")
    links = relationship("Link", back_populates="miniprogram", cascade="all, delete-orphan")
    
    # 索引
    __table_args__ = (
        Index('idx_category', 'category_id'),
        Index('idx_status', 'status'),
    )

class DomainConfig(Base):
    __tablename__ = "domain_configs"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    miniprogram_id = Column(String(100), ForeignKey("miniprograms.id", ondelete="CASCADE"), nullable=False, comment="小程序ID")
    domain_type = Column(String(50), nullable=False, comment="域名类型：default(默认), order(订购), receive(领取), pay(付费)等")
    test_domain = Column(String(500), comment="测试环境域名")
    prod_domain = Column(String(500), comment="正式环境域名")
    first_level = Column(String(100), comment="一级目录")
    second_level = Column(String(100), comment="二级目录")
    third_level = Column(String(100), comment="三级目录")
    description = Column(String(200), comment="域名用途描述")
    status = Column(Integer, default=1, comment="状态：1启用，0禁用")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    miniprogram = relationship("Miniprogram", back_populates="domain_configs")
    
    # 索引和约束
    __table_args__ = (
        Index('idx_miniprogram', 'miniprogram_id'),
        Index('idx_domain_type', 'domain_type'),
        Index('uk_miniprogram_domain_type', 'miniprogram_id', 'domain_type', unique=True),
    )

class Link(Base):
    __tablename__ = "links"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    miniprogram_id = Column(String(100), ForeignKey("miniprograms.id", ondelete="CASCADE"), nullable=False, comment="小程序ID")
    title = Column(String(500), nullable=False, comment="链接标题")
    url = Column(Text, nullable=False, comment="链接URL")
    sort_order = Column(Integer, default=0, comment="排序权重")
    status = Column(Integer, default=1, comment="状态：1启用，0禁用")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    miniprogram = relationship("Miniprogram", back_populates="links")
    
    # 索引
    __table_args__ = (
        Index('idx_miniprogram', 'miniprogram_id'),
        Index('idx_status', 'status'),
        Index('idx_sort', 'sort_order'),
    ) 