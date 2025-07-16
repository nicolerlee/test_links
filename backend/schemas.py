from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# 基础模式
class CategoryBase(BaseModel):
    id: str = Field(..., max_length=50, description="分类ID")
    name: str = Field(..., max_length=100, description="分类显示名称")
    description: Optional[str] = Field(None, description="分类描述")
    sort_order: int = Field(0, description="排序权重")
    status: int = Field(1, description="状态：1启用，0禁用")

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="分类显示名称")
    description: Optional[str] = Field(None, description="分类描述")
    sort_order: Optional[int] = Field(None, description="排序权重")
    status: Optional[int] = Field(None, description="状态：1启用，0禁用")

class Category(CategoryBase):
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# 域名配置模式
class DomainConfigBase(BaseModel):
    domain_type: str = Field(..., max_length=50, description="域名类型")
    test_domain: Optional[str] = Field(None, max_length=500, description="测试环境域名")
    prod_domain: Optional[str] = Field(None, max_length=500, description="正式环境域名")
    first_level: Optional[str] = Field(None, max_length=100, description="一级目录")
    second_level: Optional[str] = Field(None, max_length=100, description="二级目录")
    third_level: Optional[str] = Field(None, max_length=100, description="三级目录")
    description: Optional[str] = Field(None, max_length=200, description="域名用途描述")
    status: int = Field(1, description="状态：1启用，0禁用")

class DomainConfigCreate(DomainConfigBase):
    miniprogram_id: str = Field(..., max_length=100, description="小程序ID")

class DomainConfigUpdate(BaseModel):
    domain_type: Optional[str] = Field(None, max_length=50, description="域名类型")
    test_domain: Optional[str] = Field(None, max_length=500, description="测试环境域名")
    prod_domain: Optional[str] = Field(None, max_length=500, description="正式环境域名")
    first_level: Optional[str] = Field(None, max_length=100, description="一级目录")
    second_level: Optional[str] = Field(None, max_length=100, description="二级目录")
    third_level: Optional[str] = Field(None, max_length=100, description="三级目录")
    description: Optional[str] = Field(None, max_length=200, description="域名用途描述")
    status: Optional[int] = Field(None, description="状态：1启用，0禁用")

class DomainConfig(DomainConfigBase):
    id: int
    miniprogram_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# 域名类型模式
class DomainTypeBase(BaseModel):
    domain_type: str = Field(..., max_length=50, description="域名类型")

class DomainTypeCreate(DomainTypeBase):
    miniprogram_id: str = Field(..., max_length=100, description="小程序ID")

class DomainTypeUpdate(BaseModel):
    domain_type: Optional[str] = Field(None, max_length=50, description="域名类型")

class DomainType(DomainTypeBase):
    id: int
    miniprogram_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# 链接模式
class LinkBase(BaseModel):
    title: str = Field(..., max_length=500, description="链接标题")
    url: str = Field(..., description="链接URL")
    domain_type: Optional[str] = Field(None, max_length=50, description="域名类型")
    sort_order: int = Field(0, description="排序权重")
    status: int = Field(1, description="状态：1启用，0禁用")

class LinkCreate(LinkBase):
    miniprogram_id: str = Field(..., max_length=100, description="小程序ID")

class LinkUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=500, description="链接标题")
    url: Optional[str] = Field(None, description="链接URL")
    domain_type: Optional[str] = Field(None, max_length=50, description="域名类型")
    sort_order: Optional[int] = Field(None, description="排序权重")
    status: Optional[int] = Field(None, description="状态：1启用，0禁用")

class Link(LinkBase):
    id: int
    miniprogram_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# 小程序模式
class MiniprogramBase(BaseModel):
    id: str = Field(..., max_length=100, description="小程序ID")
    name: str = Field(..., max_length=200, description="小程序显示名称")
    category_id: str = Field(..., max_length=50, description="分类ID")
    description: Optional[str] = Field(None, description="小程序描述")
    status: int = Field(1, description="状态：1启用，0禁用")
    sort_order: int = Field(0, description="排序权重")

class MiniprogramCreate(MiniprogramBase):
    pass

class MiniprogramUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200, description="小程序显示名称")
    category_id: Optional[str] = Field(None, max_length=50, description="分类ID")
    description: Optional[str] = Field(None, description="小程序描述")
    status: Optional[int] = Field(None, description="状态：1启用，0禁用")
    sort_order: Optional[int] = Field(None, description="排序权重")

class Miniprogram(MiniprogramBase):
    created_at: datetime
    updated_at: datetime
    category: Optional[Category] = None
    domain_configs: List[DomainConfig] = []
    domain_types: List[DomainType] = []
    links: List[Link] = []
    
    class Config:
        from_attributes = True

# 带关联数据的分类模式
class CategoryWithMiniprograms(Category):
    miniprograms: List[Miniprogram] = []
    
    class Config:
        from_attributes = True

# 响应模式
class ApiResponse(BaseModel):
    success: bool = True
    message: str = "操作成功"
    data: Optional[dict] = None

class ListResponse(BaseModel):
    success: bool = True
    message: str = "获取成功"
    data: List[dict] = []
    total: int = 0 