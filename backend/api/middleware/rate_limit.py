"""Rate limiter configuration using slowapi (in-memory, no Redis required).

Default: 10 requests per minute per IP address.
Applied per-endpoint via @limiter.limit("10/minute") decorator.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])
