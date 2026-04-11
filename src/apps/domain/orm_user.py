from sqlalchemy import Table, Column, String, Integer, DateTime, create_engine, Date
from sqlalchemy import MetaData, text, JSON
from sqlalchemy.dialects.mysql import BIGINT, TINYINT, SMALLINT
from sqlalchemy.orm import mapper
from apps.domain.entities.coupons import Coupon
from apps.domain.entities.logistic import Logistic
from apps.domain.entities.user import User
from apps.domain.entities.user_token import UserToken
from apps.domain.entities.user_membership import UserMembershipEntity

metadata = MetaData()


user_table = Table(
    "user",
    metadata,
    Column("id", BIGINT(unsigned=True), primary_key=True, autoincrement=True, comment="主键"),
    Column("nickname", String(32), nullable=True, default="", comment="昵称"),
    Column("code", String(10), nullable=True, default="", comment="会员号"),
    Column("extend_property", JSON, nullable=True, default=None, comment="扩展属性"),
    Column("phone", String(100), nullable=True, default="", comment="加密手机号"),
    Column("wechat_openid", String(100), nullable=True, comment="微信openid"),
    Column("black", TINYINT, nullable=True, index=True, comment="黑名单"),
    Column("avatar", String(1024), nullable=True, default="", comment="头像"),
    Column("birthday", Date, nullable=True, comment="生日"),
    Column("deleted_at", DateTime, nullable=True, comment="删除时间"),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="数据产生时间"),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
           comment="数据更新时间"),
    mysql_charset="utf8mb4",
    comment="用户"
)

user_token_table = Table(
    "user_token",
    metadata,
    Column("id", BIGINT(unsigned=True), primary_key=True, autoincrement=True, comment="主键"),
    Column("uid", BIGINT(unsigned=True), index=True, comment="用户id"),
    Column("token", String(100), index=True, nullable=False, comment="token"),
    Column("expired_at", DateTime, index=True, nullable=False, comment="过期于"),
    Column("deleted_at", DateTime, nullable=True, comment="删除时间"),
    mysql_charset="utf8mb4",
    comment="token对照"
)


coupon_table = Table(
    "coupon",
    metadata,
    Column("id", BIGINT(unsigned=True), primary_key=True, autoincrement=True, comment="主键"),
    Column("coupon_type", SMALLINT, comment="类型"),
    Column("generated_type", SMALLINT, comment="类型"),
    Column("title", String(128), nullable=False, comment="名字"),
    Column("price", Integer, comment="价格"),
    Column("limit", Integer, comment="限制"),
    Column("uid", BIGINT(unsigned=True), index=True, comment="用户id"),
    Column("extend_property", JSON, nullable=True, default=None, comment="扩展属性"),
    Column("effected_at", Date, index=True, nullable=False, comment="生效于"),
    Column("expired_at", Date, index=True, nullable=False, comment="过期于"),
    Column("deleted_at", DateTime, nullable=True, comment="删除时间"),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="数据产生时间"),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
           comment="数据更新时间"),
    mysql_charset="utf8mb4",
    comment="优惠券"
)


logistic_table = Table(
    "logistic",
    metadata,
    Column("id", BIGINT(unsigned=True), primary_key=True, autoincrement=True, comment="主键"),
    Column("order_id", BIGINT(unsigned=True), index=True, comment="订单id"),
    Column("nodes", JSON, nullable=True, default=None, comment="节点"),
    Column("status", SMALLINT, index=True, comment="当前状态"),
    Column("address_id", BIGINT(unsigned=True), index=True, comment="原始送货地址"),
    Column("address_info", JSON, nullable=True, default=None, comment="地址快照"),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="数据产生时间"),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
           comment="数据更新时间"),
    mysql_charset="utf8mb4",
    comment="订单配送信息"
)


user_membership_table = Table(
    "user_membership",
    metadata,
    Column("id", BIGINT(unsigned=True), primary_key=True, autoincrement=True, comment="主键"),
    Column("uid", BIGINT(unsigned=True), index=True, comment="用户ID"),
    Column("membership_id", BIGINT(unsigned=True), comment="会员ID"),
    Column("membership_info", JSON, nullable=True, default=None, comment="会员信息快照"),
    Column("start_day", Date, nullable=False, comment="开始日期"),
    Column("end_day", Date, nullable=False, comment="结束日期"),
    Column("extend_property", JSON, nullable=True, default=None, comment="扩展数据"),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间"),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
           comment="更新时间"),
    Column("deleted_at", DateTime, nullable=True, comment="删除时间"),
    mysql_charset="utf8mb4",
    comment="用户会员信息"
)


def start_mappers():
    mapper(User, user_table)
    mapper(UserToken, user_token_table)
    mapper(Coupon, coupon_table)
    mapper(Logistic, logistic_table)
    mapper(UserMembershipEntity, user_membership_table)


if __name__ == '__main__':
    engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/xd25", echo=True)
    metadata.create_all(engine)
    start_mappers()
