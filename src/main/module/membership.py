import injector
from js_kits.fastapi_kits.async_injection_provider import async_provider
from sqlalchemy.ext.asyncio import AsyncSession
from wechatpayv3 import WeChatPay
from apps.domain.entities.membership import MembershipEntity
from apps.domain.entities.user_membership import UserMembershipEntity
from apps.domain.entities.membership_order import MembershipOrderEntity
from apps.domain.repo.repo_membership import MembershipRepository
from apps.domain.repo.repo_user_membership import UserMembershipRepository
from apps.domain.repo.repo_membership_order import MembershipOrderRepository
from apps.domain.repo.repo_user import UserRepository
from apps.use_case.membership.query_membership import QueryMembership
from apps.use_case.membership.create_user_membership import UseCaseCreateUserMembership
from apps.use_case.membership.create_membership_order import CreateMembershipOrder
from apps.use_case.membership.handle_membership_pay_callback import HandleMembershipPayCallback
from apps.use_case.membership.query_membership_order import QueryMembershipOrder
from apps.use_case.pay.unified_pay_callback import UnifiedPayCallback
from apps.use_case.order.handle_shopping_order_pay_callback import HandleShoppingOrderPayCallback


class MembershipModule(injector.Module):

    @async_provider
    async def get_membership_repository(self, session: AsyncSession) -> MembershipRepository:
        return MembershipRepository(session=session, Entity=MembershipEntity)

    @async_provider
    async def get_query_membership(self, repo: MembershipRepository, user_membership_repo: UserMembershipRepository) -> QueryMembership:
        return QueryMembership(repo, user_membership_repo)

    @async_provider
    async def get_user_membership_repository(self, session: AsyncSession) -> UserMembershipRepository:
        return UserMembershipRepository(session=session, Entity=UserMembershipEntity)

    @async_provider
    async def get_create_user_membership(self, repo: UserMembershipRepository, membership_repo: MembershipRepository) -> UseCaseCreateUserMembership:
        return UseCaseCreateUserMembership(repo, membership_repo)

    @async_provider
    async def get_membership_order_repository(self, session: AsyncSession) -> MembershipOrderRepository:
        return MembershipOrderRepository(session=session, Entity=MembershipOrderEntity)

    @async_provider
    async def get_create_membership_order(self,
                                          membership_order_repo: MembershipOrderRepository,
                                          user_membership_repo: UserMembershipRepository,
                                          membership_repo: MembershipRepository,
                                          user_repo: UserRepository,
                                          wx_pay: WeChatPay) -> CreateMembershipOrder:
        return CreateMembershipOrder(membership_order_repo, user_membership_repo, membership_repo, user_repo, wx_pay)

    @async_provider
    async def get_handle_membership_pay_callback(self,
                                                  membership_order_repo: MembershipOrderRepository,
                                                  user_membership_repo: UserMembershipRepository) -> HandleMembershipPayCallback:
        return HandleMembershipPayCallback(membership_order_repo, user_membership_repo)

    @async_provider
    async def get_query_membership_order(self, repo: MembershipOrderRepository) -> QueryMembershipOrder:
        return QueryMembershipOrder(repo)

    @async_provider
    async def get_unified_pay_callback(self,
                                       handle_membership_pay_callback: HandleMembershipPayCallback,
                                       handle_shopping_order_pay_callback: HandleShoppingOrderPayCallback) -> UnifiedPayCallback:
        return UnifiedPayCallback(handle_membership_pay_callback, handle_shopping_order_pay_callback)
