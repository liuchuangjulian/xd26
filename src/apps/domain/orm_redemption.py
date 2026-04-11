from sqlalchemy import Table, Column, String, BigInteger, create_engine, DateTime, Numeric
from sqlalchemy import MetaData, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import mapper
from apps.domain.entities.redemption_history import RedemptionHistory

metadata = MetaData()


redemption_history_table = Table(
    "redemption_history",
    metadata,
    Column("id", BigInteger, primary_key=True, comment="主键"),
    Column("uid", BigInteger, nullable=False, comment="用户ID"),
    Column("card_number", String(64), nullable=False, comment="兑换卡卡号"),
    Column("card_password", String(64), nullable=True, comment="兑换卡密码"),
    Column("amount", Numeric(10, 2), nullable=False, comment="兑换金额"),
    Column("status", TINYINT, nullable=False, comment="状态：1已兑换 2已取消"),
    Column("redemption_time", DateTime, nullable=False, comment="兑换时间"),
    Column("expired_at", DateTime, nullable=True, comment="过期时间"),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")),
    Column("deleted_at", DateTime, nullable=True, comment="删除时间"),
    mysql_charset="utf8mb4",
    comment="兑换记录"
)


def start_mappers():
    mapper(RedemptionHistory, redemption_history_table)


if __name__ == '__main__':
    engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/xd25", echo=False)
    metadata.create_all(engine)
    start_mappers()
