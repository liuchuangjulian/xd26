import logging
import datetime
from js_kits.except_kits.except_kits import FastapiResult, ClientError
from sqlalchemy.orm.attributes import flag_modified
from apps.domain.repo.repo_logistic import LogisticRepository

logger = logging.getLogger(__name__)


class UpdateLogisticStatus:
    def __init__(self, repo: LogisticRepository):
        self.repo = repo

    async def get_logistic_obj(self, session, order_id):
        _, logistic_list = await self.repo.get_list(session,
                                                    equal_maps={"order_id": order_id},
                                                    with_total=False, with_none_deleted=False)
        if not logistic_list:
            raise ClientError({"msg": "订单物流信息不存在"})
        return logistic_list[0]

    async def execute(self, order_id, status, node_name, owner, phone, notes) -> None:
        async with self.repo.session as session:
            logistic_obj = await self.get_logistic_obj(session, order_id)
            # 添加新的节点
            new_node = {
                "name": node_name,
                "owner": owner,
                "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "phone": phone,
                "notes": notes
            }

            # 更新节点列表和状态
            nodes = logistic_obj.nodes if logistic_obj.nodes else []
            nodes.append(new_node)
            logistic_obj.nodes = nodes
            logistic_obj.status = status
            flag_modified(self, "nodes")

            await self.repo.add(session, logistic_obj)
            raise FastapiResult({"msg": "ok",
                                 "data": logistic_obj.to_dict()
                                 })
