"""Módulo de configuração de cache para consultas do sistema"""

from functools import wraps

from cachetools import TTLCache
from sqlalchemy.orm import Query  # noqa: F401

# Configuração do cache
query_cache = TTLCache(maxsize=100, ttl=300)  # Cache por 5 minutos


def cache_query(f):
    """Decorator para cache de queries"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        cache_key = f.__name__ + str(args) + str(kwargs)
        if cache_key in query_cache:
            return query_cache[cache_key]
        result = f(*args, **kwargs)
        query_cache[cache_key] = result
        return result

    return wrapper


def clear_cache():
    """Limpa todo o cache de consultas"""
    query_cache.clear()
    print("Cache de consultas limpo")
