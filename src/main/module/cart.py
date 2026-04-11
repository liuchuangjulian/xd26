import injector
from js_kits.fastapi_kits.async_injection_provider import async_provider
from sqlalchemy.ext.asyncio import AsyncSession
from apps.domain.entities.cart import CartEntity
from apps.domain.repo.repo_cart import CartRepository
from apps.use_case.cart.query_cart import QueryCart
from apps.use_case.cart.use_case_cart_change_num import UseCaseCartChangeNum


class CartModule(injector.Module):

    @async_provider
    async def get_cart_repository(self, session: AsyncSession) -> CartRepository:
        return CartRepository(session=session, Entity=CartEntity)

    @async_provider
    async def get_use_case_cart_change_num(self, repo: CartRepository) -> UseCaseCartChangeNum:
        return UseCaseCartChangeNum(repo)

    @async_provider
    async def get_query_product_cart(self, repo: CartRepository) -> QueryCart:
        return QueryCart(repo)
