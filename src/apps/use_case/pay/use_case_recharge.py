import logging
from js_kits.except_kits.except_kits import FastapiResult, BackendException
from apps.use_case.pay.use_case_pay_base import UseCasePayBase

logger = logging.getLogger(__name__)

QueryProductTypeCustomer = "customer"
QueryProductTypeBoss = "boss"


class UseCaseRecharge(UseCasePayBase):

    async def get_order_obj(self, order_id, session):
        return None

    async def execute(self, order_id, user_obj) -> None:
        async with self.repo.session as session:
            order_obj = await self.get_order_obj(order_id, session)
            await self.pay(session, order_obj.description(), order_obj.amount, user_obj)
        raise BackendException()
