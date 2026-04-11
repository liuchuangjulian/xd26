from typing import Optional, List
from pydantic import BaseModel, Field, root_validator


class CreateUserMembershipParams(BaseModel):
    membership_id: int = Field(..., description="会员ID")
