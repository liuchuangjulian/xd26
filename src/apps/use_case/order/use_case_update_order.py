import logging
from js_kits.except_kits.except_kits import FastapiResult, ClientError
from apps.domain.entities.order import OrderStatus
from apps.domain.repo.repo_order import OrderRepository

logger = logging.getLogger(__name__)


class UseCaseUpdateOrder:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    async def execute(self, uid, order_id, status) -> None:
        async with self.repo.session as session:
            _, order_list = await self.repo.get_list(session,
                                                     equal_maps={"id": order_id, "uid": uid}, with_total=False)
            if not order_list:
                raise ClientError({"msg": "id 不存在或者已经删除"})
            order_obj = order_list[0]
            if order_obj.status in OrderStatus.user_can_changed():
                order_obj.status = status
            else:
                raise ClientError({"msg": "status不可修改"})
            await self.repo.add(session, order_obj)
            raise FastapiResult({"msg": "ok",
                                 "data": order_obj.id
                                 })
