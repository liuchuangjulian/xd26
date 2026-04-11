from fastapi import APIRouter
from fastapi_injector import Injected
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from js_kits.except_kits.except_kits import FastapiResult, BackendException

health_router = APIRouter(tags=["健康检测"])


class HealthResp(BaseModel):
    message: str = Field(..., description="健康检查信息")


@health_router.get("/health")
async def health(
    session: AsyncSession = Injected(AsyncSession),
):
    try:
        await session.execute(text("SELECT 1"))
    except Exception as e:
        raise BackendException()
    raise FastapiResult({"message": "健康监测"})
