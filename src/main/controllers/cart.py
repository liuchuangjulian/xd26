from fastapi_injector import Injected
from fastapi import APIRouter, Body, Request
import logging
from aioredis import Redis
from apps.domain.repo.repo_user import UserRepository
from js_kits.fastapi_kits.user_route import UserRoute
from apps.use_case.cart.query_cart import QueryCart
from apps.use_case.cart.use_case_cart_change_num import UseCaseCartChangeNum
from main.controllers.check_auth import auth
from main.controllers.input.cart import AddToCartParams, CartChangeNumParams, DelFromCartParams

router_cart = APIRouter(route_class=UserRoute, prefix="/cart", tags=["购物车"])
logger = logging.getLogger(__name__)


@router_cart.post("/change_num")
@auth
async def change_num(request: Request,
                     redis_client: Redis = Injected(Redis),
                     user_repo: UserRepository = Injected(UserRepository),
                     uid=None,
                     params: CartChangeNumParams = Body(...),
                     use_case: UseCaseCartChangeNum = Injected(UseCaseCartChangeNum)):
    # 购物车（加1/减1/调整数量（设置为0））
    await use_case.execute(uid, params.p_id, params.num, params.dif)
"""
curl -X POST 'http://127.0.0.1:8080/api/cart/change_num'  -H 'content-type: application/json' -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b' -d '{"p_id": 1, "num": 10, "dif": 0}' | jq .
"""


@router_cart.get("/list")
@auth
async def get_cart_list(request: Request, redis_client: Redis = Injected(Redis),
                        user_repo: UserRepository = Injected(UserRepository),
                        uid=None, rank=None, use_case: QueryCart = Injected(QueryCart)):
    # 查询购物车
    await use_case.query(uid, rank == "0")
    """
    curl 'http://127.0.0.1:8080/api/cart/list' -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b' | jq .
    """
