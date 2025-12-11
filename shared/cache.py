"""Caching utilities."""

import hashlib
import json
from functools import wraps
from typing import Any, Callable, Optional
from datetime import datetime, timedelta

_memory_cache: dict = {}


def _hash_args(*args, **kwargs) -> str:
    """Generate hash for function arguments."""
    content = json.dumps({"args": str(args), "kwargs": str(kwargs)}, sort_keys=True)
    return hashlib.md5(content.encode()).hexdigest()


def cache(
    ttl: Optional[int] = None,
    use_disk: bool = False,
) -> Callable:
    """Decorator for caching function results."""
    ttl = ttl or 3600
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            cache_key = f"{func.__module__}.{func.__name__}:{_hash_args(*args, **kwargs)}"
            
            if cache_key in _memory_cache:
                entry = _memory_cache[cache_key]
                if datetime.now() < entry["expires"]:
                    return entry["value"]
                else:
                    del _memory_cache[cache_key]
            
            value = func(*args, **kwargs)
            
            entry = {
                "value": value,
                "expires": datetime.now() + timedelta(seconds=ttl),
            }
            _memory_cache[cache_key] = entry
            
            return value
        
        return wrapper
    return decorator


def clear_cache(pattern: Optional[str] = None) -> int:
    """Clear cached entries matching pattern."""
    global _memory_cache
    
    count = 0
    
    if pattern:
        keys_to_delete = [k for k in _memory_cache if pattern in k]
        for key in keys_to_delete:
            del _memory_cache[key]
            count += 1
    else:
        count = len(_memory_cache)
        _memory_cache = {}
    
    return count
