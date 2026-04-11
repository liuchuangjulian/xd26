import logging
from js_kits.except_kits.except_kits import FastapiResult
from apps.domain.repo.repo_address import AddressRepository
from apps.domain.repo.repo_cart import CartRepository
from apps.domain.repo.repo_category import CategoryRepository
from apps.domain.repo.repo_config import ConfigRepository
from apps.domain.repo.repo_coupons import CouponsRepository
from apps.domain.repo.repo_logistic import LogisticRepository
from apps.domain.repo.repo_membership import MembershipRepository
from apps.domain.repo.repo_user_membership import UserMembershipRepository
from apps.domain.repo.repo_order import OrderRepository
from apps.domain.repo.repo_transfer_record import TransferRecordRepository
from apps.domain.repo.repo_order_line import OrderLineRepository
from apps.domain.repo.repo_products import ProductRepository
from apps.domain.repo.repo_user import UserRepository

logger = logging.getLogger(__name__)


class IniUseCase:

    def __init__(self, repo_category: CategoryRepository,
                 repo_product: ProductRepository,
                 repo_order_line: OrderLineRepository,
                 repo_order: OrderRepository,
                 repo_cart: CartRepository,
                 repo_address: AddressRepository,
                 repo_user: UserRepository,
                 repo_coupons: CouponsRepository,
                 repo_logistic: LogisticRepository,
                 repo_membership: MembershipRepository,
                 repo_user_membership: UserMembershipRepository,
                 repo_transfer_record: TransferRecordRepository,
                 repo_config: ConfigRepository,
                 ):
        self.repo_category = repo_category
        self.repo_product = repo_product
        self.repo_order_line = repo_order_line
        self.repo_order = repo_order
        self.repo_cart = repo_cart
        self.repo_user = repo_user
        self.repo_address = repo_address
        self.repo_coupons = repo_coupons
        self.repo_logistic = repo_logistic
        self.repo_membership = repo_membership
        self.repo_user_membership = repo_user_membership
        self.repo_transfer_record = repo_transfer_record
        self.repo_config = repo_config

    async def execute(self) -> None:
        async with self.repo_category.session as session:
            await self.repo_category.ini(session)
            await self.repo_product.ini(session)
            await self.repo_order_line.ini(session)
            await self.repo_order.ini(session)
            await self.repo_cart.ini(session)
            await self.repo_user.ini(session)
            await self.repo_address.ini(session)
            await self.repo_coupons.ini(session)
            await self.repo_logistic.ini(session)
            await self.repo_membership.ini(session)
            await self.repo_user_membership.ini(session)
            await self.repo_transfer_record.ini(session)
            await self.repo_config.ini(session)
        raise FastapiResult()
