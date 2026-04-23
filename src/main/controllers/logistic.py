from aioredis.client import Redis
from fastapi_injector import Injected
from fastapi import APIRouter, Request, UploadFile, Depends, Body
import logging
from js_kits.fastapi_kits.user_route import UserRoute
from apps.domain.repo.repo_user import UserRepository
from apps.use_case.logistic.query_logistic import QueryLogistic
from apps.use_case.logistic.update_logistic_status import UpdateLogisticStatus
from main.controllers.check_auth import auth
from main.controllers.input.logistic import QueryLogisticParams, UpdateLogisticStatusParams

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


@router_logistic.post("/update_status")
@auth
async def update_logistic_status(request: Request,
                                  redis_client: Redis = Injected(Redis),
                                  user_repo: UserRepository = Injected(UserRepository),
                                  uid=None, params: UpdateLogisticStatusParams = Body(...),
                                  use_case: UpdateLogisticStatus = Injected(UpdateLogisticStatus)):
    await use_case.execute(params.order_id, params.status, params.node_name,
                          params.owner, params.phone, params.notes)
'''
curl -X 'POST' \
  'http://localhost:8080/api/logistic/update_status' \
  -H 'accept: application/json' -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b' \
  -H 'Content-Type: application/json' \
  -d '{"order_id": 1,"status": 3,"node_name": "派送中","owner": "派送员：张三","phone": "021-12345678","notes": ""}' | jq .
'''