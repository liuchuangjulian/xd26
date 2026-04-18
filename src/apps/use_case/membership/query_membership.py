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
            # 查询所有会员
            total, obj_list = await self.repo.get_list(
                session,
                order_by_list=["show_index"]
            )
            result_list, cannot_buy_list = [], []
            for membership in obj_list:
                membership_dict = membership.to_dict()
                purchased_count = membership_purchase_count.get(membership.id, 0)
                max_purchase_count = getattr(membership, 'max_purchase_count', -1)
                membership_dict['purchased_count'] = purchased_count
                if purchased_count >= max_purchase_count > -1:
                    membership_dict['status'] = 0
                if membership_dict['status']:
                    result_list.append(membership_dict)
                else:
                    cannot_buy_list.append(membership_dict)
            result_list.extend(cannot_buy_list)
            raise FastapiResult({
                "msg": "ok",
                "data": result_list
            })
