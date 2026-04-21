import logging
from js_kits.except_kits.except_kits import FastapiResult, ClientError
from apps.domain.repo.repo_membership_order import MembershipOrderRepository

logger = logging.getLogger(__name__)


class QueryMembershipOrder:
    def __init__(self, repo: MembershipOrderRepository):
        self.repo = repo

    async def query(self, uid, out_trade_no: str = None, status: int = None) -> None:
        """查询会员订单"""
        async with self.repo.session as session:
            equal_maps = {"uid": uid}
            if out_trade_no:
                equal_maps["out_trade_no"] = out_trade_no
            if status is not None:
                equal_maps["status"] = status

            total, obj_list = await self.repo.get_list(
                session,
                equal_maps=equal_maps,
                order_by_list=["-created_at"]
            )

            raise FastapiResult({
                "msg": "ok",
                "data": {
                    "total": total,
                    "list": [obj.to_dict() for obj in obj_list]
                }
            })
