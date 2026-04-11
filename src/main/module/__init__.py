import injector
from js_kits.fastapi_kits.mysql_module import MysqlModule
from js_kits.fastapi_kits.redis_module import RedisModule
from main.module.address import AddressModule
from main.module.area import AreaModule
from main.module.cart import CartModule
from main.module.config import ConfigModule
from main.module.coupons import CouponsModule
from main.module.logistic import LogisticModule
from main.module.membership import MembershipModule
from main.module.notice import NoticeModule
from main.module.order import OrderModule
from main.module.pay import PayModule
from main.module.redemption import RedemptionModule
from main.module.shop import ShopModule
from main.module.user import UserModule

__all__ = ["setup_dependency_injection"]


def setup_dependency_injection() -> injector.Injector:
    modules = [
               MysqlModule(),
               RedisModule(),
               ShopModule(),
               UserModule(),
               OrderModule(),
               AddressModule(),
               AreaModule(),
               RedemptionModule(),
               CartModule(),
               CouponsModule(),
               LogisticModule(),
               MembershipModule(),
               PayModule(),
               ConfigModule(),
               NoticeModule(),
    ]

    _injector = injector.Injector(modules, auto_bind=False)
    return _injector
