from aioredis import Redis
from fastapi_injector import Injected
from fastapi import APIRouter, Request, Depends, Body
import logging
from js_kits.fastapi_kits.user_route import UserRoute
from apps.domain.repo.repo_user import UserRepository
from apps.use_case.membership.query_membership import QueryMembership
from apps.use_case.membership.create_membership_order import CreateMembershipOrder
from apps.use_case.pay.unified_pay_callback import UnifiedPayCallback
from apps.use_case.membership.query_membership_order import QueryMembershipOrder
from main.controllers.check_auth import auth
from main.controllers.output.membership import MembershipListResponse, CreateUserMembershipResponse
from main.controllers.input.membership import CreateUserMembershipParams, QueryMembershipOrderParams

router_membership = APIRouter(route_class=UserRoute, prefix="/membership", tags=["会员"])
logger = logging.getLogger(__name__)


@router_membership.get("/list", response_model=MembershipListResponse)
@auth
async def get_membership_list(request: Request,
                              redis_client: Redis = Injected(Redis),
                              user_repo: UserRepository = Injected(UserRepository),
                              uid=None,
                              use_case: QueryMembership = Injected(QueryMembership)):
    await use_case.query(uid)
'''
curl -X 'GET' 'http://localhost:8080/api/membership/list' -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b' | jq .
'''


@router_membership.post("/buy", summary="购买会员（创建支付订单）")
@auth
async def buy_membership(request: Request,
                        redis_client: Redis = Injected(Redis),
                        user_repo: UserRepository = Injected(UserRepository),
                        uid=None,
                        params: CreateUserMembershipParams = Body(...),
                        use_case: CreateMembershipOrder = Injected(CreateMembershipOrder)):
    """购买会员，创建微信支付订单"""
    await use_case.execute(uid, params.membership_id)



@router_membership.get("/orders", summary="查询会员订单")
@auth
async def get_membership_orders(request: Request,
                                redis_client: Redis = Injected(Redis),
                                user_repo: UserRepository = Injected(UserRepository),
                                uid=None,
                                params: QueryMembershipOrderParams = Depends(),
                                use_case: QueryMembershipOrder = Injected(QueryMembershipOrder)):
    """查询用户的会员订单列表"""
    await use_case.query(uid, params.out_trade_no, params.status)
