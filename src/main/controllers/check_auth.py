import json
from functools import wraps
from js_kits.except_kits.except_kits import UnauthorizedError, ClientError, ForbiddenError


def auth(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        redis_client = kwargs.get("redis_client")
        user_repo = kwargs.get("user_repo")
        kwargs.pop("uid")

        headers_dict = dict(request.headers)
        token = headers_dict.get("token")
        if not token:
            raise UnauthorizedError()

        token_data = await redis_client.get(token)
        if token_data:
            token_data = json.loads(token_data)
        else:
            async with user_repo.session as session:
                user_token_obj = await user_repo.get_user_info_by_token(session, token)
                if not user_token_obj or not user_token_obj.is_valid():
                    raise UnauthorizedError()
                token_data = {"uid": user_token_obj.uid}
                await redis_client.set(token, json.dumps(token_data))
        uid = token_data["uid"]
        return await func(uid=uid, *args, **kwargs)
    return wrapper
