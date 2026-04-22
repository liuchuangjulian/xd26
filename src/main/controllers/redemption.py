from fastapi_injector import Injected
from fastapi import APIRouter, Request, Query, Body, Depends
from js_kits.fastapi_kits.user_route import UserRoute
from apps.use_case.redemption.query_redemption import QueryRedemptionHistory
from apps.use_case.redemption.redeem_card import RedeemCardUseCase
from apps.domain.repo.repo_user import UserRepository
from main.controllers.check_auth import auth
from main.controllers.input.redemption import RedeemCardParams

router_redemption = APIRouter(route_class=UserRoute, prefix="/redemption", tags=["兑换记录"])


@router_redemption.get("/history")
@auth
async def get_redemption_history(
    request: Request,
    user_repo: UserRepository = Injected(UserRepository),
    uid=None,
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    use_case: QueryRedemptionHistory = Injected(QueryRedemptionHistory)
):
    """查询用户的兑换记录"""
    await use_case.query(uid, page=page, page_size=page_size)
"""
curl -X 'GET' \
  'http://localhost:8080/api/redemption/history?page=1&page_size=10' \
  -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b' | jq .
"""


@router_redemption.post("/redeem")
@auth
async def redeem_card(
        request: Request,
        user_repo: UserRepository = Injected(UserRepository),
        uid=None,
        params: RedeemCardParams = Body(...),
        use_case: RedeemCardUseCase = Injected(RedeemCardUseCase),
):
    """兑换兑换卡"""
    await use_case.execute(uid, params.card_number)
"""
curl -X 'POST' \
  'http://localhost:8080/api/redemption/redeem' \
  -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b' \
  -H 'Content-Type: application/json' \
  -d '{"card_number": "CARD88888888005"}' | jq .
"""
