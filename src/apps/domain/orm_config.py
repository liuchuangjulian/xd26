from sqlalchemy import Table, Column, String, BigInteger, create_engine, DateTime, JSON
from sqlalchemy import MetaData, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import mapper
from apps.domain.entities.config import ConfigEntity

metadata = MetaData()


config_table = Table(
    "config",
    metadata,
    Column("id", BigInteger, primary_key=True, comment="主键"),
    Column("key", String(64), nullable=False, comment="名称", index=True),
    Column("name", String(64), nullable=False, comment="名称"),
    Column("is_active", TINYINT, nullable=False, default=0, comment="是否生效：0未生效，1已生效"),
    Column("extend_property", JSON, nullable=True, comment="属性信息"),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")),
    Column("deleted_at", DateTime, nullable=True, comment="删除时间"),
    mysql_charset="utf8mb4",
    comment="配置表"
)

def start_mappers():
    mapper(ConfigEntity, config_table)


if __name__ == '__main__':
    engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/xd25", echo=False)
    metadata.create_all(engine)
    start_mappers()
