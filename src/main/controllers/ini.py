from fastapi import APIRouter, Body, Depends
import logging
from fastapi_injector import Injected
from js_kits.fastapi_kits.user_route import UserRoute
from apps.use_case.use_case_ini import IniUseCase

router_api_ini = APIRouter(route_class=UserRoute, prefix="/ini", tags=["ini"])
logger = logging.getLogger(__name__)


@router_api_ini.get("")
async def ini(use_case: IniUseCase = Injected(IniUseCase)):
    await use_case.execute()
