from aioredis import Redis
from fastapi_injector import Injected
from fastapi import APIRouter, Request, Query, Body
from js_kits.fastapi_kits.user_route import UserRoute
from pydantic import BaseModel, Field
from apps.use_case.redemption.query_redemption import QueryRedemptionHistory
from apps.domain.repo.repo_user import UserRepository
from main.controllers.check_auth import auth

router_redemption = APIRouter(route_class=UserRoute, prefix="/redemption", tags=["兑换记录"])


class RedeemCardParams(BaseModel):
    card_number: str = Field(..., description="兑换卡卡号")


@router_redemption.get("/history")
@auth
async def get_redemption_history(
    request: Request,
    redis_client: Redis = Injected(Redis),
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
    params: RedeemCardParams = Body(...),
    redis_client: Redis = Injected(Redis),
    user_repo: UserRepository = Injected(UserRepository),
    uid=None
):
    """兑换兑换卡"""
    from sqlalchemy import text
    import datetime
    from decimal import Decimal
    from js_kits.except_kits.except_kits import ClientError, FastapiResult

    async with user_repo.session as session:
        # 1. 查询兑换卡
        result = await session.execute(
            text("SELECT * FROM redemption_cards WHERE card_number = :card_number AND deleted_at IS NULL"),
            {"card_number": params.card_number}
        )
        card = result.fetchone()

        if not card:
            raise ClientError({"msg": "兑换卡不存在"})

        card_dict = dict(card._mapping)

        # 2. 检查卡状态
        if card_dict['status'] == 1:
            raise ClientError({"msg": "该兑换卡已使用"})

        # 3. 检查过期时间
        if card_dict['expired_at']:
            expired_at = card_dict['expired_at']
            if expired_at < datetime.datetime.now():
                raise ClientError({"msg": "该兑换卡已过期"})

        # 4. 查询用户当前余额
        result = await session.execute(
            text("SELECT id, balance FROM user WHERE id = :uid"),
            {"uid": uid}
        )
        user_data = result.fetchone()

        if not user_data:
            raise ClientError({"msg": "用户不存在"})

        user_id, current_balance = user_data
        current_balance = Decimal(str(current_balance)) if current_balance else Decimal('0.00')
        card_amount = Decimal(str(card_dict['amount']))

        # 5. 更新用户余额
        new_balance = current_balance + card_amount
        await session.execute(
            text("UPDATE user SET balance = :balance WHERE id = :uid"),
            {"balance": new_balance, "uid": uid}
        )

        # 6. 更新兑换卡状态
        await session.execute(
            text("""
                UPDATE redemption_cards
                SET status = 1, used_at = NOW(), used_by = :uid
                WHERE card_number = :card_number
            """),
            {"uid": uid, "card_number": params.card_number}
        )

        # 7. 创建兑换记录
        await session.execute(
            text("""
                INSERT INTO redemption_history
                (uid, card_number, amount, status, redemption_time)
                VALUES (:uid, :card_number, :amount, 1, NOW())
            """),
            {
                "uid": uid,
                "card_number": params.card_number,
                "amount": float(card_amount)
            }
        )

        # 8. 提交事务
        await session.commit()

        raise FastapiResult({
            "msg": "兑换成功",
            "data": {
                "card_number": params.card_number,
                "amount": float(card_amount),
                "balance_before": float(current_balance),
                "balance_after": float(new_balance)
            }
        })


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
