import injector
from aioredis.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from apps.domain.entities.coupons import Coupon
from js_kits.fastapi_kits.async_injection_provider import async_provider

from apps.domain.entities.logistic import Logistic
from apps.domain.repo.repo_logistic import LogisticRepository
from apps.use_case.logistic.query_logistic import QueryLogistic


class LogisticModule(injector.Module):

    @async_provider
    async def provide_repo_logistic(self, session: AsyncSession, redis_client: Redis) -> LogisticRepository:
        return LogisticRepository(session, redis_client, Logistic)

    @async_provider
    async def provide_query_logistic(self, repo: LogisticRepository) -> QueryLogistic:
        return QueryLogistic(repo)
