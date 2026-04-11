import injector
from js_kits.fastapi_kits.async_injection_provider import async_provider
from sqlalchemy.ext.asyncio import AsyncSession
from apps.domain.entities.category import CategoryEntity
from apps.domain.entities.products import ProductsEntity
from apps.domain.repo.repo_address import AddressRepository
from apps.domain.repo.repo_cart import CartRepository
from apps.domain.repo.repo_category import CategoryRepository
from apps.domain.repo.repo_config import ConfigRepository
from apps.domain.repo.repo_coupons import CouponsRepository
from apps.domain.repo.repo_logistic import LogisticRepository
from apps.domain.repo.repo_membership import MembershipRepository
from apps.domain.repo.repo_order import OrderRepository
from apps.domain.repo.repo_order_line import OrderLineRepository
from apps.domain.repo.repo_products import ProductRepository
from apps.domain.repo.repo_user import UserRepository
from apps.domain.repo.repo_user_membership import UserMembershipRepository
from apps.domain.repo.repo_transfer_record import TransferRecordRepository
from apps.use_case.shop.query_category import QueryCategory
from apps.use_case.shop.query_product import QueryProducts
from apps.use_case.use_case_ini import IniUseCase


class ShopModule(injector.Module):

    @async_provider
    async def get_category_repository(self, session: AsyncSession) -> CategoryRepository:
        return CategoryRepository(session=session, Entity=CategoryEntity)

    @async_provider
    async def get_product_repository(self, session: AsyncSession) -> ProductRepository:
        return ProductRepository(session=session, Entity=ProductsEntity)

    @async_provider
    async def get_query_category(self, repo: CategoryRepository) -> QueryCategory:
        return QueryCategory(repo)

    @async_provider
    async def get_query_product(self, repo: ProductRepository) -> QueryProducts:
        return QueryProducts(repo)

    @async_provider
    async def get_use_case_ini(self, repo_category: CategoryRepository, repo_product: ProductRepository,
                               repo_order_line: OrderLineRepository, repo_order: OrderRepository,
                               repo_cart: CartRepository, repo_address: AddressRepository,
                               repo_user: UserRepository, repo_coupons: CouponsRepository,
                               repo_logistic: LogisticRepository, repo_membership: MembershipRepository,
                               repo_user_membership: UserMembershipRepository,
                               repo_transfer_record: TransferRecordRepository,
                               repo_config: ConfigRepository,
                               ) -> IniUseCase:
        return IniUseCase(repo_category, repo_product, repo_order_line, repo_order, repo_cart, repo_address,
                          repo_user, repo_coupons, repo_logistic, repo_membership, repo_user_membership,
                          repo_transfer_record, repo_config)
