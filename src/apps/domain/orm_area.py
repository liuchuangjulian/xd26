from sqlalchemy import Table, Column, String, BigInteger, create_engine, DateTime
from sqlalchemy import MetaData, text
from sqlalchemy.dialects.mysql import SMALLINT
from sqlalchemy.orm import mapper
from apps.domain.entities.area import Area

metadata = MetaData()


area_table = Table(
    "area",
    metadata,
    Column("id", BigInteger, primary_key=True, comment="主键"),
    Column("code", String(20), nullable=False, comment="区域编码"),
    Column("name", String(50), nullable=False, comment="区域名称"),
    Column("parent_code", String(20), nullable=True, comment="父级编码"),
    Column("level", SMALLINT, nullable=False, comment="层级：1省 2市 3区"),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")),
    Column("deleted_at", DateTime, nullable=True, comment="删除时间"),
    mysql_charset="utf8mb4",
    comment="省市区表"
)


def start_mappers():
    mapper(Area, area_table)


if __name__ == '__main__':
    engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/xd25", echo=False)
    metadata.create_all(engine)
    start_mappers()
