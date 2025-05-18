import aioredis
import json
import hashlib

redis = aioredis.from_url("redis://localhost", decode_responses=True)


def make_cache_key(user_id: int, query_params: dict):
    raw = json.dumps({"user_id": user_id, **query_params}, sort_keys=True)
    return f"entries:{hashlib.sha256(raw.encode()).hexdigest()}"
