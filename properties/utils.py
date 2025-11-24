import logging
from django_redis import get_redis_connection
from django.core.cache import cache
from .models import Property

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    conn = get_redis_connection("default")
    info = conn.info()

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)

    total_requests = hits + misses
    hit_ratio = hits / total_requests if total_requests > 0 else 0

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": hit_ratio,
    }

    logger.info(f"Redis Cache Metrics: {metrics}")

    return metrics


def get_all_properties():
    # Try to get cached queryset
    properties = cache.get('all_properties')

    if properties is None:
        # Not cached → fetch from DB
        properties = list(
            Property.objects.all().values(
                "id", "title", "description", "price", "location", "created_at"
            )
        )
        # Cache for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)

    return properties
