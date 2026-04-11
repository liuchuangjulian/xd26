import injector
from js_kits.fastapi_kits.async_injection_provider import async_provider
from sqlalchemy.ext.asyncio import AsyncSession
from apps.domain.entities.address import Address
from apps.domain.repo.repo_address import AddressRepository
from apps.domain.repo.repo_cart import CartRepository
from apps.domain.repo.repo_category import CategoryRepository
from apps.use_case.address.create_address import UseCaseCreateAddress
from apps.use_case.address.delete_address import UseCaseDeleteAddress
from apps.use_case.address.query_address import QueryAddress
from apps.use_case.address.update_address import UseCaseUpdateAddress
from apps.use_case.shop.query_category import QueryCategory
from apps.use_case.cart.use_case_cart_change_num import UseCaseCartChangeNum


class AddressModule(injector.Module):

    @async_provider
    async def get_address_repository(self, session: AsyncSession) -> AddressRepository:
        return AddressRepository(session=session, Entity=Address)

    @async_provider
    async def get_use_case_cart_change_num(self, repo: CartRepository) -> UseCaseCartChangeNum:
        return UseCaseCartChangeNum(repo)

    @async_provider
    async def get_query_address(self, repo: AddressRepository) -> QueryAddress:
        return QueryAddress(repo)

    @async_provider
    async def get_use_case_create_address(self, repo: AddressRepository) -> UseCaseCreateAddress:
        return UseCaseCreateAddress(repo)

    @async_provider
    async def get_use_case_update_address(self, repo: AddressRepository) -> UseCaseUpdateAddress:
        return UseCaseUpdateAddress(repo)

    @async_provider
    async def get_use_case_delete_address(self, repo: AddressRepository) -> UseCaseDeleteAddress:
        return UseCaseDeleteAddress(repo)
