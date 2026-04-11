import logging
import datetime
from js_kits.except_kits.except_kits import FastapiResult, ClientError
from apps.domain.entities.user_membership import UserMembershipEntity
from apps.domain.repo.repo_user_membership import UserMembershipRepository
from apps.domain.repo.repo_membership import MembershipRepository

logger = logging.getLogger(__name__)


class UseCaseCreateUserMembership:
    def __init__(self, repo: UserMembershipRepository, membership_repo: MembershipRepository):
        self.repo = repo
        self.membership_repo = membership_repo

    async def execute(self, uid, membership_id) -> None:
        async with self.repo.session as session:
            # 获取会员信息
            _, membership_list = await self.membership_repo.get_list(session, with_total=False, equal_maps={"id": membership_id})
            if not membership_list:
                raise ClientError({"msg": "会员类型不存在", "code": -1})
            membership = membership_list[0]

            # 检查是否已有有效会员
            _, existing_memberships = await self.repo.get_list(
                session,
                equal_maps={"uid": uid},
                with_total=False
            )
            # 计算开始和结束日期
            start_day = datetime.date.today()
            end_day = start_day + datetime.timedelta(days=membership.duration)

            # 如果有有效会员，从原结束日期开始计算
            if existing_memberships:
                latest_membership = max(existing_memberships, key=lambda x: x.end_day)
                if latest_membership.end_day >= start_day:
                    start_day = latest_membership.end_day
                    end_day = start_day + datetime.timedelta(days=membership.duration)

            # 创建用户会员记录
            obj = UserMembershipEntity(
                uid=uid,
                membership_id=membership_id,
                membership_info={
                    "id": membership.id,
                    "name": membership.name,
                    "price": float(membership.price),
                    "duration": membership.duration,
                    "description": membership.description,
                },
                start_day=start_day,
                end_day=end_day,
                extend_property={}
            )
            await self.repo.add(session, obj)

            raise FastapiResult({"msg": "开通会员成功",
                                 "data": {
                                     "id": obj.id,
                                     "membership_name": membership.name,
                                     "start_day": str(start_day),
                                     "end_day": str(end_day),
                                 }
                                 })
