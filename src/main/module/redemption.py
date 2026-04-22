import injector
from js_kits.fastapi_kits.async_injection_provider import async_provider
from sqlalchemy.ext.asyncio import AsyncSession
from apps.domain.entities.redemption_card import RedemptionCard
from apps.domain.repo.repo_redemption import RedemptionRepository
from apps.domain.repo.repo_transfer_record import TransferRecordRepository
from apps.domain.repo.repo_user import UserRepository
from apps.use_case.redemption.redeem_card import RedeemCardUseCase


class RedemptionModule(injector.Module):

    @async_provider
    async def provide_redemption_repository(self, session: AsyncSession) -> RedemptionRepository:
        return RedemptionRepository(session=session, Entity=RedemptionCard)

    @async_provider
    async def provide_redeem_card_use_case(
        self,
        user_repo: UserRepository,
        redemption_repo: RedemptionRepository,
        transfer_record_repo: TransferRecordRepository
    ) -> RedeemCardUseCase:
        return RedeemCardUseCase(user_repo=user_repo, redemption_repo=redemption_repo, transfer_record_repo=transfer_record_repo)
