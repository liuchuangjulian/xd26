import injector
from aioredis.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from apps.domain.entities.user import User
from js_kits.fastapi_kits.async_injection_provider import async_provider
from apps.domain.repo.repo_user import UserRepository
from apps.use_case.user.query_user_info import QueryUserInfo
from apps.use_case.user.use_case_change_user_info import UseCaseChangeUserInfo
from apps.use_case.user.use_case_wechat_login import WechatLoginUseCase


class UserModule(injector.Module):

    @async_provider
    async def provide_repo_user(self, session: AsyncSession, redis_client: Redis) -> UserRepository:
        return UserRepository(session, redis_client, User)

    @async_provider
    async def provide_query_user_info(self, repo: UserRepository) -> QueryUserInfo:
        return QueryUserInfo(repo)

    @async_provider
    async def provide_use_change_user_info(self, repo: UserRepository) -> UseCaseChangeUserInfo:
        return UseCaseChangeUserInfo(repo)

    @async_provider
    async def provide_use_case_wc_login(self, user_repo: UserRepository) -> WechatLoginUseCase:
        return WechatLoginUseCase(user_repo)
