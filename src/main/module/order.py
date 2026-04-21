import injector
from js_kits.fastapi_kits.async_injection_provider import async_provider
from sqlalchemy.ext.asyncio import AsyncSession
from apps.domain.entities.order import OrderEntity
from apps.domain.entities.order_line import OrderLineEntity
from apps.domain.repo.repo_order import OrderRepository
from apps.domain.repo.repo_order_line import OrderLineRepository
from apps.use_case.order.query_order import QueryOrder
from apps.use_case.order.query_order_line import QueryOrderLine
from apps.use_case.order.use_case_create_order import UseCaseCreateOrder
from apps.use_case.order.use_case_pre_create_order import UseCasePreCreateOrder
from apps.use_case.order.use_case_update_order import UseCaseUpdateOrder
from apps.use_case.order.create_shopping_order_pay import CreateShoppingOrderPay
from apps.use_case.order.handle_shopping_order_pay_callback import HandleShoppingOrderPayCallback


class OrderModule(injector.Module):

    @async_provider
    async def get_order_repository(self, session: AsyncSession) -> OrderRepository:
        return OrderRepository(session=session, Entity=OrderEntity)

    @async_provider
    async def get_order_line_repository(self, session: AsyncSession) -> OrderLineRepository:
        return OrderLineRepository(session=session, Entity=OrderLineEntity)

    @async_provider
    async def get_use_case_create_order(self, repo: OrderRepository) -> UseCaseCreateOrder:
        return UseCaseCreateOrder(repo)

    @async_provider
    async def get_query_order(self, repo: OrderRepository) -> QueryOrder:
        return QueryOrder(repo)

    @async_provider
    async def get_query_order_line(self, repo: OrderLineRepository) -> QueryOrderLine:
        return QueryOrderLine(repo)

    @async_provider
    async def get_use_case_change_order_status(self, repo: OrderRepository) -> UseCaseUpdateOrder:
        return UseCaseUpdateOrder(repo)

    @async_provider
    async def get_use_case_pre_create_order(self, repo: OrderRepository) -> UseCasePreCreateOrder:
        return UseCasePreCreateOrder(repo)

    @async_provider
    async def get_create_shopping_order_pay(self,
                                            order_repo: OrderRepository,
                                            user_repo,
                                            wx_pay) -> CreateShoppingOrderPay:
        from apps.domain.repo.repo_user import UserRepository
        return CreateShoppingOrderPay(order_repo, user_repo, wx_pay)

    @async_provider
    async def get_handle_shopping_order_pay_callback(self,
                                                     order_repo: OrderRepository) -> HandleShoppingOrderPayCallback:
        return HandleShoppingOrderPayCallback(order_repo)
