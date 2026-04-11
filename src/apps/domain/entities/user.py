from datetime import datetime, timedelta, date
from typing import Optional, List, Dict
from decimal import Decimal
import random
from js_kits.fastapi_kits.entity_base import Entity



class User(Entity):
    id: Optional[int]
    nickname: str
    code: str
    extend_property: Optional[dict]
    phone: str
    wechat_openid: str
    black: int
    avatar: str
    birthday: date
    balance: Decimal
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    def generate_code_nickname(self):
        self.code = "".join(random.choice("012356789") for _ in range(10))
        return f"顾客{self.code [:5]}-{self.code[5:]}"

    def user_info_to_dict(self):
        return {
            "avatar": self.avatar,
            "nickname": self.nickname,
            "birthday": self.birthday.strftime("%Y-%m-%d") if self.birthday else "",
            "code": self.code,
        }

    def to_login_result(self, token):
        info_dict = self.user_info_to_dict()
        info_dict["token"] = token
        return info_dict

    def update_value(self, **kwargs):
        for k, v in kwargs.items():
            if k in ["nickname", "avatar", "birthday", "wechat_id"]:
                setattr(self, k, v)



if __name__ == "__main__":
    print(User().generate_code_nickname())
