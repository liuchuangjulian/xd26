from aioredis import Redis
from fastapi_injector import Injected
from fastapi import APIRouter, Request, UploadFile, Depends, Body
import logging
from js_kits.fastapi_kits.input import PageParams
from js_kits.fastapi_kits.user_route import UserRoute
from apps.domain.repo.repo_user import UserRepository
from apps.use_case.coupons.query_coupons import QueryCoupons
from main.controllers.check_auth import auth

router_coupons = APIRouter(route_class=UserRoute, prefix="/coupons", tags=["优惠券"])
logger = logging.getLogger(__name__)


@router_coupons.get("/list")
@auth
async def get_coupons_list(request: Request, redis_client: Redis = Injected(Redis),
                           user_repo: UserRepository = Injected(UserRepository), uid=None,
                           page_params: PageParams = Depends(),
                           use_case: QueryCoupons = Injected(QueryCoupons),
                           ):
    await use_case.query(uid, page=page_params.page, page_size=page_params.page_size)
'''
curl -X 'GET' 'http://localhost:8080/api/coupons/list?page=1&page_size=10' -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b' | jq .
'''