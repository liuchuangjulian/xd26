import logging
from js_kits.except_kits.except_kits import FastapiResult
from apps.domain.repo.repo_transfer_record import TransferRecordRepository
from apps.domain.entities.transfer_record import RecordType

logger = logging.getLogger(__name__)


class QueryRedemptionHistory:
    def __init__(self, repo: TransferRecordRepository):
        self.repo = repo

    async def query(self, uid, page=1, page_size=10) -> None:
        """查询用户的兑换记录"""
        async with self.repo.session as session:
            # 查询用户的兑换记录（按类型筛选兑换记录）
            total, obj_list = await self.repo.get_list(
                session,
                equal_maps={"user_id": str(uid), "type": RecordType.Redemption.value},
                page=page,
                page_size=page_size,
                order_by_list=["-created_at"]
            )

            # 格式化返回数据
            data = []
            for obj in obj_list:
                extra = obj.extra or {}
                data.append({
                    "id": obj.id,
                    "type": obj.type,
                    "amount": obj.amount / 100,  # 分转元
                    "status": obj.status,
                    "card_number": extra.get("card_number", ""),
                    "balance_before": extra.get("balance_before", 0),
                    "balance_after": extra.get("balance_after", 0),
                    "redemption_time": obj.created_at.strftime("%Y-%m-%d %H:%M:%S") if obj.created_at else ""
                })

            raise FastapiResult({
                "msg": "ok",
                "total": total,
                "page": page,
                "page_size": page_size,
                "data": data
            })
