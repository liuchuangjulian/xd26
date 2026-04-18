from fastapi_injector import Injected
from fastapi import APIRouter, Request, UploadFile, Depends, Body
import logging
from apps.domain.repo.repo_user import UserRepository
from aioredis import Redis
from js_kits.fastapi_kits.input import PageParams
from js_kits.fastapi_kits.user_route import UserRoute
from apps.use_case.order.query_order import QueryOrder
from apps.use_case.order.query_order_line import QueryOrderLine
from apps.use_case.order.use_case_create_order import UseCaseCreateOrder
from apps.use_case.order.use_case_pre_create_order import UseCasePreCreateOrder
from apps.use_case.order.use_case_update_order import UseCaseUpdateOrder
from main.controllers.check_auth import auth
from main.controllers.input.order import CreateOrderParams, QueryOrderParams, QueryOrderLineParams, \
    PreCreateOrderParams, ChangeOrderStatsParams
from main.controllers.output.order import PreCreateOrderResponse

router_order = APIRouter(route_class=UserRoute, prefix="/order", tags=["订单"])
logger = logging.getLogger(__name__)


@router_order.post("/pre_create", response_model=PreCreateOrderResponse)
@auth
async def create_order(request: Request, redis_client: Redis = Injected(Redis),
                       user_repo: UserRepository = Injected(UserRepository), uid=None,
                       params: PreCreateOrderParams = Body(...),
                       use_case: UseCasePreCreateOrder = Injected(UseCasePreCreateOrder)):
    await use_case.execute(uid, [{"count": product_count.count, "p_id": product_count.p_id}
                                 for product_count in params.p_id_count_list],
                                 coupon_id=params.coupon_id)
'''
curl -X 'POST' \
  'http://localhost:8080/api/order/pre_create' \
  -H 'accept: application/json' -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b' \
  -H 'Content-Type: application/json' \
  -d '{"coupon_id": 0, "p_id_count_list": [{"p_id": 1,"count": 1}]}' | jq .

# coupon_id=0 表示自动选择最优优惠券
# coupon_id>0 表示使用指定的优惠券ID
'''


@router_order.post("/create")
@auth
async def create_order(request: Request, redis_client: Redis = Injected(Redis),
                       user_repo: UserRepository = Injected(UserRepository), uid=None,
                       params: CreateOrderParams = Body(...),
                       use_case: UseCaseCreateOrder = Injected(UseCaseCreateOrder)):
    await use_case.execute(uid, [{"count": product_count.count, "p_id": product_count.p_id}
                                 for product_count in params.p_id_count_list],
                           params.address_id, params.coupon_id)
'''
curl -X 'POST' \
  'http://localhost:8080/api/order/create' \
  -H 'accept: application/json' -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b' \
  -H 'Content-Type: application/json' \
  -d '{"address_id": 1,"coupon_id": 0,
  "p_id_count_list": [{"p_id": 1,"count": 1}]}' | jq .
'''


@router_order.get("/list")
@auth
async def get_order_list(request: Request, redis_client: Redis = Injected(Redis),
                         user_repo: UserRepository = Injected(UserRepository), uid=None,
                         params: QueryOrderParams = Depends(), page_params: PageParams = Depends(),
                         use_case: QueryOrder = Injected(QueryOrder),
                         ):
    await use_case.query(uid=uid, status=params.status, page=page_params.page, page_size=page_params.page_size)
'''
curl -X 'GET'  'http://localhost:8080/api/order/list?status=1&page=1&page_size=10'  -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b'  | jq .
'''


@router_order.get("/line/list")
@auth
async def get_order_line_list(request: Request, redis_client: Redis = Injected(Redis),
                              user_repo: UserRepository = Injected(UserRepository), uid=None,
                              params: QueryOrderLineParams = Depends(),  page_params: PageParams = Depends(),
                              use_case: QueryOrderLine = Injected(QueryOrderLine)):
    await use_case.query(uid=1, order_id=params.order_id, page=page_params.page, page_size=page_params.page_size)
'''
curl -X 'GET'  'http://localhost:8080/api/order/line/list?order_id=1&page=1&page_size=10'  -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b'  | jq .
'''


@router_order.post("/change_stats")
@auth
async def user_change_order_stats(request: Request, redis_client: Redis = Injected(Redis),
                                  user_repo: UserRepository = Injected(UserRepository), uid=None,
                                  params: ChangeOrderStatsParams = Body(...),
                                  use_case: UseCaseUpdateOrder = Injected(UseCaseUpdateOrder)):
    await use_case.execute(uid, order_id=params.order_id, status=params.status)
'''
curl -X 'POST' \
  'http://localhost:8080/api/order/change_stats' \
  -H 'accept: application/json' -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b' \
  -H 'Content-Type: application/json' \
  -d '{"status": 7,"order_id": 1}' | jq .
'''