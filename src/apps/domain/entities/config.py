import datetime
from js_kits.fastapi_kits.entity_base import Entity


class ConfigEntity(Entity):
    """
    配置
    """
    id: int
    key: str
    name: str  # 名称
    is_active: int  # 是否生效：0未生效，1已生效
    extend_property: dict  # 属性信息
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime