import injector
from aioredis.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from apps.domain.entities.coupons import Coupon
from js_kits.fastapi_kits.async_injection_provider import async_provider
from apps.domain.repo.repo_coupons import CouponsRepository
from apps.use_case.coupons.query_coupons import QueryCoupons


class CouponsModule(injector.Module):

    @async_provider
    async def provide_repo_coupons(self, session: AsyncSession, redis_client: Redis) -> CouponsRepository:
        return CouponsRepository(session, redis_client, Coupon)

    @async_provider
    async def provide_query_coupons(self, repo: CouponsRepository) -> QueryCoupons:
        return QueryCoupons(repo)
