from sqlalchemy import create_engine, Integer, Float, SmallInteger, Index
from sqlalchemy import MetaData, JSON
from sqlalchemy import Table, Column, String, DateTime, text, BigInteger
from sqlalchemy.orm import mapper
from apps.domain.entities.address import Address
from apps.domain.entities.cart import CartEntity
from apps.domain.entities.category import CategoryEntity
from apps.domain.entities.membership import MembershipEntity
from apps.domain.entities.order import OrderEntity
from apps.domain.entities.order_line import OrderLineEntity
from apps.domain.entities.products import ProductsEntity
from apps.domain.entities.transfer_record import TransferRecord

metadata = MetaData()


category_table = Table(
    "category",
    metadata,
    Column("id", BigInteger, primary_key=True, comment="主键"),
    Column("name", String(128), nullable=False, comment="名称"),
    Column("show_index", Integer, nullable=True, comment="展示序号"),
    Column("extend_property", JSON, nullable=True, comment="扩展数据"),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
           comment="数据更新时间"),
    Column("deleted_at", DateTime, nullable=True),
    mysql_charset="utf8mb4",
    comment="类目"
)


products_table = Table(
    "products",
    metadata,
    Column("id", BigInteger, primary_key=True, comment="主键"),
    Column("category_id_list", JSON, nullable=True, comment="类目列表"),
    Column("show_index", Integer, nullable=True, comment="展示序号"),
    Column("name", String(128), nullable=False, comment="名称"),
    Column("describe", String(1024), nullable=False, comment="描述"),
    Column("barcode", String(128), nullable=False, comment="条码"),
    Column("tips", JSON, nullable=True, comment="提示列表"),
    Column("sold", Integer, nullable=True, comment="提示列表"),
    Column("img", String(1024), nullable=False, comment="主图"),
    Column("original_price", Integer, nullable=False, comment="原价"),
    Column("price", Integer, nullable=False, comment="售卖-价格"),
    Column("units", String(128), nullable=False, comment="单位"),
    Column("extend_property", JSON, nullable=True, comment="扩展数据"),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
           comment="数据更新时间"),
    Column("deleted_at", DateTime, nullable=True),
    mysql_charset="utf8mb4",
    comment="商品"
)


cart_table = Table(
    "cart",
    metadata,
    Column("id", BigInteger, primary_key=True, comment="主键"),
    Column("uid", Integer, nullable=False, index=True, comment="uid"),
    Column("p_id_info_map", JSON, nullable=True, comment="产品&数量"),
    Column("p_list", JSON, nullable=True, comment="产品&数量"),
    Column("extend_property", JSON, nullable=True, comment="扩展数据"),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
           comment="数据更新时间"),
    Column("deleted_at", DateTime, nullable=True),
    # Index("ix_key", "key"),
    # Index("ix_key_id", "key", "id"),
    mysql_charset="utf8mb4",
    comment="购物车"
)


order_table = Table(
    "order",
    metadata,
    Column("id", BigInteger, primary_key=True, comment="主键"),
    Column("main_info", String(128), nullable=True, comment="主要信息"),
    Column("uid", Integer, nullable=True, comment="uid"),
    Column("real_pay", Integer, nullable=True, comment="实际支付"),
    Column("total", Integer, nullable=True, comment="总金额"),
    Column("count", Integer, nullable=True, comment="总件数"),
    Column("discount", Integer, nullable=True, comment="总折扣"),
    Column("status", SmallInteger, nullable=False, comment="状态"),
    Column("balance", Integer, nullable=True, comment="余额"),
    Column("coins", Integer, nullable=True, comment="使用积分"),
    Column("coupon_id_list", JSON, nullable=True, comment="优惠券 id 数组"),
    Column("payment_id_list", JSON, nullable=True, comment="支付id列表数组"),
    Column("delivery_id_list", JSON, nullable=True, comment="配送id列表 数组"),
    Column("feedback_coins", Integer, nullable=True, comment="回馈积分"),
    Column("extend_property", JSON, nullable=True, comment="扩展数据"),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
           comment="数据更新时间"),
    Column("deleted_at", DateTime, nullable=True),
    mysql_charset="utf8mb4",
    comment="订单"
)

order_line_table = Table(
    "order_line",
    metadata,
    Column("id", BigInteger, primary_key=True, comment="主键"),
    Column("uid", Integer, nullable=True, comment="uid"),
    Column("index", Integer, nullable=True, comment="序号"),
    Column("name", String(128), nullable=False, comment="品名"),
    Column("barcode", String(128), nullable=False, comment="条码"),
    Column("order_id", Integer, nullable=True, comment="order_id"),
    Column("p_id", Integer, nullable=True, comment="商品id"),
    Column("price", Integer, nullable=True, comment="价格(单价格)"),
    Column("amount", Integer, nullable=True, comment="总价格"),
    Column("count", Integer, nullable=True, comment="商品数量"),
    Column("extend_property", JSON, nullable=True, comment="扩展数据"),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
           comment="数据更新时间"),
    Column("deleted_at", DateTime, nullable=True),
    mysql_charset="utf8mb4",
    comment="订单行"
)


membership_table = Table(
    "membership",
    metadata,
    Column("id", BigInteger, primary_key=True, comment="主键"),
    Column("name", String(128), nullable=False, comment="会员名称"),
    Column("price", Float, nullable=False, comment="价格"),
    Column("duration", Integer, nullable=False, comment="有效期（天）"),
    Column("description", String(512), nullable=True, comment="描述"),
    Column("status", SmallInteger, nullable=False, server_default=text("1"), comment="状态：1-启用，0-禁用"),
    Column("show_index", Integer, nullable=True, comment="展示序号"),
    Column("max_purchase_count", Integer, nullable=True, comment="最大购买数量"),
    Column("extend_property", JSON, nullable=True, comment="扩展数据"),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
           comment="数据更新时间"),
    Column("deleted_at", DateTime, nullable=True),
    mysql_charset="utf8mb4",
    comment="会员信息"
)


community_table = Table(
    "community",
    metadata,
    Column("id", BigInteger, primary_key=True, comment="主键"),
    Column("province", String(128), nullable=False, comment="省"),
    Column("city", String(128), nullable=False, comment="市"),
    Column("district", String(128), nullable=False, comment="区"),
    Column("name", String(128), nullable=False, comment="小区"),
    Column("lon", Float, nullable=True, comment="经度"),
    Column("lat", Float, nullable=True, comment="纬度"),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
           comment="数据更新时间"),
    Column("deleted_at", DateTime, nullable=True),
    mysql_charset="utf8mb4",
    comment="可选小区"
)


address_table = Table(
    "address",
    metadata,
    Column("id", BigInteger, primary_key=True, comment="主键"),
    Column("uid", BigInteger, nullable=False, comment="uid", index=True),
    Column("province", String(128), nullable=False, comment="province"),
    Column("city", String(128), nullable=False, comment="city"),
    Column("district", String(128), nullable=False, comment="district"),
    Column("community_name", String(128), nullable=False, comment="community_name"),
    Column("selected", SmallInteger, nullable=False, comment="选择"),
    Column("building_unit_room", String(256), nullable=False, comment="2号楼"),
    Column("phone", String(128), nullable=False, comment="手机"),
    Column("name", String(128), nullable=False, comment="联系人"),
    Column("tag", String(32), nullable=True, default="", comment="标签"),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
           comment="数据更新时间"),
    Column("deleted_at", DateTime, nullable=True),
    mysql_charset="utf8mb4",
    comment="地址"
)


transfer_record_table = Table(
    "transfer_record",
    metadata,
    Column("id", BigInteger, primary_key=True, comment="主键"),
    Column("type", String(64), nullable=False, comment="记录类型"),
    Column("shop_id", String(128), nullable=False, comment="店铺id", index=True),
    Column("user_id", String(128), nullable=False, comment="用户id", index=True),
    Column("amount", Integer, nullable=False, comment="交易金额（分）"),
    Column("real", Integer, nullable=False, comment="实际金额（分）"),
    Column("gift", Integer, nullable=False, server_default=text("0"), comment="赠送金额（分）"),
    Column("coin_count", Integer, nullable=False, server_default=text("0"), comment="积分"),
    Column("op_user_id", String(128), nullable=True, comment="操作用户id"),
    Column("status", String(32), nullable=False, comment="状态", index=True),
    Column("extra", JSON, nullable=True, comment="附加属性"),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间", index=True),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
           comment="更新时间"),
    Column("deleted_at", DateTime, nullable=True),
    mysql_charset="utf8mb4",
    comment="交易记录"
)


def start_mappers():
    mapper(CategoryEntity, category_table)
    mapper(ProductsEntity, products_table)
    mapper(CartEntity, cart_table)
    mapper(OrderEntity, order_table)
    mapper(OrderLineEntity, order_line_table)
    mapper(MembershipEntity, membership_table)
    mapper(Address, address_table)
    mapper(TransferRecord, transfer_record_table)


if __name__ == '__main__':
    engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/xd25", echo=False)
    metadata.create_all(engine)
    start_mappers()
