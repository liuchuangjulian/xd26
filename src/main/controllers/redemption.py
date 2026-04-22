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


'''
# 测试命令

## 1. 查询兑换记录
curl -X 'GET' \
  'http://localhost:8080/api/redemption/history?page=1&page_size=10' \
  -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b' | jq .

# 返回示例：
# {
#   "msg": "ok",
#   "total": 7,
#   "page": 1,
#   "page_size": 10,
#   "data": [
#     {
#       "id": 4,
#       "uid": 1,
#       "card_number": "CARD202604040004",
#       "amount": 300.0,
#       "status": 1,
#       "redemption_time": "2026-04-04 16:45:00",
#       "created_at": "2026-04-04 16:45:00"
#     }
#   ]
# }

## 2. 兑换兑换卡
curl -X 'POST' \
  'http://localhost:8080/api/redemption/redeem' \
  -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b' \
  -H 'Content-Type: application/json' \
  -d '{"card_number": "CARD88888888005"}' | jq .

# 返回示例：
# {
#   "msg": "兑换成功",
#   "data": {
#     "card_number": "CARD88888888005",
#     "amount": 1000.0,
#     "balance_before": 700.0,
#     "balance_after": 1700.0
#   },
#   "code": 0
# }

## 3. 测试错误情况
# 兑换已使用的卡
curl -X 'POST' \
  'http://localhost:8080/api/redemption/redeem' \
  -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b' \
  -H 'Content-Type: application/json' \
  -d '{"card_number": "CARD88888888003"}' | jq .

# 返回：
# {
#   "msg": "该兑换卡已使用",
#   "code": 1
# }

# 兑换不存在的卡
curl -X 'POST' \
  'http://localhost:8080/api/redemption/redeem' \
  -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b' \
  -H 'Content-Type: application/json' \
  -d '{"card_number": "CARD99999999999"}' | jq .

# 返回：
# {
#   "msg": "兑换卡不存在",
#   "code": 1
# }
'''
