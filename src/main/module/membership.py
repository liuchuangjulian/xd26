import injector
from js_kits.fastapi_kits.async_injection_provider import async_provider
from sqlalchemy.ext.asyncio import AsyncSession
from apps.domain.entities.membership import MembershipEntity
from apps.domain.entities.user_membership import UserMembershipEntity
from apps.domain.repo.repo_membership import MembershipRepository
from apps.domain.repo.repo_user_membership import UserMembershipRepository
from apps.use_case.membership.query_membership import QueryMembership
from apps.use_case.membership.create_user_membership import UseCaseCreateUserMembership


class MembershipModule(injector.Module):

    @async_provider
    async def get_membership_repository(self, session: AsyncSession) -> MembershipRepository:
        return MembershipRepository(session=session, Entity=MembershipEntity)

    @async_provider
    async def get_query_membership(self, repo: MembershipRepository) -> QueryMembership:
        return QueryMembership(repo)

    @async_provider
    async def get_user_membership_repository(self, session: AsyncSession) -> UserMembershipRepository:
        return UserMembershipRepository(session=session, Entity=UserMembershipEntity)

    @async_provider
    async def get_create_user_membership(self, repo: UserMembershipRepository, membership_repo: MembershipRepository) -> UseCaseCreateUserMembership:
        return UseCaseCreateUserMembership(repo, membership_repo)
