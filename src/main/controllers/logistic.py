from aioredis.client import Redis
from fastapi_injector import Injected
from fastapi import APIRouter, Request, UploadFile, Depends, Body
import logging
from js_kits.fastapi_kits.user_route import UserRoute
from apps.domain.repo.repo_user import UserRepository
from apps.use_case.logistic.query_logistic import QueryLogistic
from main.controllers.check_auth import auth
from main.controllers.input.logistic import QueryLogisticParams

router_logistic = APIRouter(route_class=UserRoute, prefix="/logistic", tags=["物流"])
logger = logging.getLogger(__name__)


@router_logistic.get("")
@auth
async def get_logistic_info(request: Request,
                            redis_client: Redis = Injected(Redis),
                            user_repo: UserRepository = Injected(UserRepository),
                            uid=None, params: QueryLogisticParams = Depends(),
                            use_case: QueryLogistic = Injected(QueryLogistic),
                            ):
    await use_case.query(uid, params.order_id)

'''
curl -X 'GET' 'http://localhost:8080/api/logistic?order_id=1'  -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b'  | jq .
'''