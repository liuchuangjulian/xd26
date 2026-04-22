import logging
from js_kits.except_kits.except_kits import FastapiResult
from apps.domain.repo.repo_transfer_record import TransferRecordRepository

logger = logging.getLogger(__name__)


class QueryTransferRecord:
    def __init__(self, repo: TransferRecordRepository):
        self.repo = repo

    async def query(self, uid, status, type, page, page_size) -> None:
        equal_maps = {"uid": uid}

        if status:
            equal_maps["status"] = status

        if type:
            equal_maps["type"] = type

        async with self.repo.session as session:
            total, record_list = await self.repo.get_list(
                session,
                page=page,
                page_size=page_size,
                equal_maps=equal_maps,
                order_by_list=["-created_at"],
            )

            # 格式化返回数据
            data = []
            for obj in record_list:
                extra = obj.extra or {}
                item = {
                    "id": obj.id,
                    "type": obj.type,
                    "amount": obj.amount / 100,  # 分转元
                    "amount_real": obj.amount_real / 100,
                    "amount_gift": obj.amount_gift / 100,
                    "status": obj.status,
                    "created_at": obj.created_at.strftime("%Y-%m-%d %H:%M:%S") if obj.created_at else ""
                }

                # 兑换卡记录的特殊字段
                if obj.type == "redemption":
                    item["card_number"] = extra.get("card_number", "")

                data.append(item)

            raise FastapiResult({
                "msg": "ok",
                "total": total,
                "page": page,
                "page_size": page_size,
                "data": data
            })
