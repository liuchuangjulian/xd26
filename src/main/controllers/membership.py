from aioredis import Redis
from fastapi_injector import Injected
from fastapi import APIRouter, Request, Depends, Body
import logging
from js_kits.fastapi_kits.user_route import UserRoute
from apps.domain.repo.repo_user import UserRepository
from apps.use_case.membership.query_membership import QueryMembership
from apps.use_case.membership.create_user_membership import UseCaseCreateUserMembership
from main.controllers.check_auth import auth
from main.controllers.output.membership import MembershipListResponse, CreateUserMembershipResponse
from main.controllers.input.membership import CreateUserMembershipParams

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


@router_membership.post("/create", response_model=CreateUserMembershipResponse)
@auth
async def create_user_membership(request: Request,
                                 redis_client: Redis = Injected(Redis),
                                 user_repo: UserRepository = Injected(UserRepository),
                                 uid=None,
                                 params: CreateUserMembershipParams = Body(...),
                                 use_case: UseCaseCreateUserMembership = Injected(UseCaseCreateUserMembership)):
    await use_case.execute(uid, params.membership_id)
'''
curl -X 'POST' \
  'http://localhost:8080/api/membership/create' \
  -H 'accept: application/json' \
  -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b' \
  -H 'Content-Type: application/json' \
  -d '{"membership_id": 1}' | jq .
'''
