from aioredis import Redis
from fastapi_injector import Injected
from fastapi import APIRouter, Request, UploadFile, Depends, Body
import logging
from js_kits.fastapi_kits.input import PageParams
from js_kits.fastapi_kits.user_route import UserRoute
from apps.domain.repo.repo_user import UserRepository
from apps.use_case.address.create_address import UseCaseCreateAddress
from apps.use_case.address.query_address import QueryAddress
from apps.use_case.address.update_address import UseCaseUpdateAddress
from apps.use_case.address.delete_address import UseCaseDeleteAddress
from main.controllers.check_auth import auth
from main.controllers.input.address import CreateAddressParams, UpdateAddressParams, DeleteAddressParams, \
    AddressListParams

router_address = APIRouter(route_class=UserRoute, prefix="/address", tags=["地址"])
logger = logging.getLogger(__name__)


@router_address.post("/add")
@auth
async def get_create_address(
                     request: Request,
                     redis_client: Redis = Injected(Redis),
                     user_repo: UserRepository = Injected(UserRepository),
                     uid=None,
                     params: CreateAddressParams = Body(...),
                     use_case: UseCaseCreateAddress = Injected(UseCaseCreateAddress),
                      ):
    await use_case.execute(uid, province=params.province,
                           city=params.city,
                           district=params.district,
                           community_name=params.community_name, building_unit_room=params.building_unit_room,
                           phone=params.phone, name=params.name, selected=params.selected, tag=params.tag)
'''
curl -X 'POST' \
  'http://localhost:8080/api/address/add' \
  -H 'accept: application/json' -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b'  \
  -H 'Content-Type: application/json' \
  -d '{
  "province": "上海市",
  "city": "上海市",
  "district": "黄埔区",
  "community_name": "仲意小区",
  "building_unit_room": "2号楼一单元4901",
  "phone": "18810380117",
  "name": "李聚升", "selected": 1,
  "tag": "公司"
}' | jq .
'''


@router_address.post("/change")
@auth
async def get_change_address(
                     request: Request,
                     redis_client: Redis = Injected(Redis),
                     user_repo: UserRepository = Injected(UserRepository),
                     uid=None,
        params: UpdateAddressParams = Body(...),
        use_case: UseCaseUpdateAddress = Injected(UseCaseUpdateAddress),
                      ):
    await use_case.execute(address_id=params.address_id, uid=uid,
                           province=params.province, city=params.city, district=params.district,
                           community_name=params.community_name, building_unit_room=params.building_unit_room,
                        phone=params.phone, name=params.name, selected=params.selected, tag=params.tag)
'''
curl -X 'POST' \
  'http://localhost:8080/api/address/change' \
  -H 'accept: application/json' -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b'  \
  -H 'Content-Type: application/json' \
  -d '{"address_id": 1,
  "province": "上海市",
  "city": "上海市",
  "selected": 1,
  "district": "黄埔区",
  "community_name": "仲意小区",
  "building_unit_room": "2号楼一单元4901-1",
  "phone": "18810380117",
  "name": "李聚升",
  "tag": "公司"
}'
'''


@router_address.get("/list")
@auth
async def get_address_list(
                    request: Request,
                     redis_client: Redis = Injected(Redis),
                     user_repo: UserRepository = Injected(UserRepository),
                     uid=None,
        page_params: PageParams = Depends(),
        params: AddressListParams = Depends(),
        use_case: QueryAddress = Injected(QueryAddress),
                      ):
    await use_case.query(uid, selected=params.selected, page=page_params.page, page_size=page_params.page_size)
'''
curl -X 'GET' 'http://localhost:8080/api/address/list?selected=1&page=1&page_size=10' -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b' | jq .
'''


@router_address.post("/delete")
@auth
async def delete_address(
                     request: Request,
                      redis_client: Redis = Injected(Redis),
                      user_repo: UserRepository = Injected(UserRepository),
                      uid=None,
        params: DeleteAddressParams = Body(...),
        use_case: UseCaseDeleteAddress = Injected(UseCaseDeleteAddress),
                      ):
    await use_case.execute(uid=uid, address_id=params.address_id)
'''
curl -X 'POST' \
  'http://localhost:8080/api/address/delete' \
  -H 'accept: application/json' -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b'  \
  -H 'Content-Type: application/json' \
  -d '{
  "address_id": 1
}' | jq .
'''