from fastapi_injector import Injected
from fastapi import APIRouter, Request, Depends
from js_kits.fastapi_kits.user_route import UserRoute
from apps.use_case.redemption.redeem_card import RedeemCardUseCase
from apps.domain.repo.repo_user import UserRepository
from main.controllers.check_auth import auth
from main.controllers.input.redemption import RedeemCardParams

router_redemption = APIRouter(route_class=UserRoute, prefix="/redemption", tags=["兑换卡"])


@router_redemption.post("/redeem")
@auth
async def redeem_card(
        request: Request,
        user_repo: UserRepository = Injected(UserRepository),
        uid=None,
        params: RedeemCardParams = Depends(),
        use_case: RedeemCardUseCase = Injected(RedeemCardUseCase),
):
    """兑换兑换卡"""
    await use_case.execute(uid, params.card_number)
"""
curl -X 'POST' \
  'http://localhost:8080/api/redemption/redeem' \
  -H 'token: xxx' \
  -H 'Content-Type: application/json' \
  -d '{"card_number": "CARD88888888005"}' | jq .
"""
