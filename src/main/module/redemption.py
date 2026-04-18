import injector
from js_kits.fastapi_kits.async_injection_provider import async_provider
from sqlalchemy.ext.asyncio import AsyncSession
from apps.domain.entities.redemption_history import RedemptionHistory
from apps.domain.entities.redemption_card import RedemptionCard
from apps.domain.repo.repo_redemption import RedemptionRepository
from apps.domain.repo.repo_user import UserRepository
from apps.use_case.redemption.query_redemption import QueryRedemptionHistory
from apps.use_case.redemption.redeem_card import RedeemCardUseCase


class RedemptionModule(injector.Module):

    @async_provider
    async def provide_redemption_repository(self, session: AsyncSession) -> RedemptionRepository:
        return RedemptionRepository(session=session, Entity=RedemptionHistory)

    @async_provider
    async def provide_query_redemption_history(self, repo: RedemptionRepository) -> QueryRedemptionHistory:
        return QueryRedemptionHistory(repo=repo)

    @async_provider
    async def provide_redeem_card_use_case(
        self,
        user_repo: UserRepository,
        redemption_repo: RedemptionRepository
    ) -> RedeemCardUseCase:
        return RedeemCardUseCase(user_repo=user_repo, redemption_repo=redemption_repo)
