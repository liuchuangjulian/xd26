import logging
from js_kits.except_kits.except_kits import FastapiResult
from apps.domain.repo.repo_membership import MembershipRepository
from apps.domain.repo.repo_user_membership import UserMembershipRepository

logger = logging.getLogger(__name__)


class QueryMembership:
    def __init__(self, repo: MembershipRepository, user_membership_repo: UserMembershipRepository):
        self.repo = repo
        self.user_membership_repo = user_membership_repo

    async def query(self, uid) -> None:
        print(uid)
        async with self.repo.session as session:
            # 查询用户已购买的会员记录，按membership_id分组统计购买数量
            _, user_membership_list = await self.user_membership_repo.get_list(
                session,
                page_size=-1,
                equal_maps={"uid": uid},
                with_total=False
            )
            # 统计每个会员的购买数量
            membership_purchase_count = {}
            for user_membership in user_membership_list:
                membership_id = user_membership.membership_id
                membership_purchase_count[membership_id] = membership_purchase_count.get(membership_id, 0) + 1
            print(membership_purchase_count)

            # 查询所有会员
            total, obj_list = await self.repo.get_list(
                session,
                order_by_list=["show_index"]
            )

            # 检查每个会员的购买数量是否超过限制，如果超过则将status置为0
            result_list = []
            for membership in obj_list:
                membership_dict = membership.to_dict()
                purchased_count = membership_purchase_count.get(membership.id, 0)
                # 安全获取 max_purchase_count，如果不存在则默认为 -1（无限制）
                max_purchase_count = getattr(membership, 'max_purchase_count', -1)
                print(membership.to_dict(), max_purchase_count, purchased_count, max_purchase_count)
                # 如果设置了最大购买数量限制（大于-1）且已购买数量达到或超过限制
                if -1 < max_purchase_count < purchased_count:
                    membership_dict['purchased_count'] = purchased_count
                    membership_dict['max_purchase_count'] = max_purchase_count
                else:
                    membership_dict['status'] = 0  # 设置为不可用
                    membership_dict['purchased_count'] = purchased_count
                    membership_dict['max_purchase_count'] = max_purchase_count

                result_list.append(membership_dict)

            raise FastapiResult({
                "msg": "ok",
                "data": result_list
            })
