from typing import Optional

from pydantic import BaseModel, Field, root_validator


class QueryProductsParams(BaseModel):
    name: Optional[str] = Field(None, description="name")
    category_id: int = Field(..., description="category_id")
