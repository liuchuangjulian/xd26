from pydantic import Field as PydanticField
from pydantic.fields import FieldInfo

def AutoTitleField(*args, **kwargs) -> FieldInfo:
    description = kwargs.pop("description")
    return PydanticField(
        *args,
        title=description,
        description=description,
        ** kwargs
    )
