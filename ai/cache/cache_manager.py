from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import hashlib
import json
from config.logging import logger


class CacheManager:
    # Manage caching of KPI results
    
    def __init__(self, cache_ttl_minutes: int = 60):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.cache_ttl = timedelta(minutes=cache_ttl_minutes)
    
    def _generate_cache_key(self, dataset_id: str, kpi_name: str) -> str:
        # Generate a unique cache key
        key_string = f"{dataset_id}_{kpi_name}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, dataset_id: str, kpi_name: str) -> Optional[Dict[str, Any]]:
        # Get cached KPI result if available and not expired
        cache_key = self._generate_cache_key(dataset_id, kpi_name)
        
        if cache_key not in self.cache:
            return None
        
        cached_item = self.cache[cache_key]
        
        # Check if cache is expired
        if datetime.now() - cached_item["timestamp"] > self.cache_ttl:
            del self.cache[cache_key]
            logger.info(f"Cache expired for {kpi_name}")
            return None
        
        logger.info(f"Cache hit for {kpi_name}")
        return cached_item["data"]
    
    def set(self, dataset_id: str, kpi_name: str, data: Dict[str, Any]):
        # Cache KPI result
        cache_key = self._generate_cache_key(dataset_id, kpi_name)
        
        self.cache[cache_key] = {
            "data": data,
            "timestamp": datetime.now()
        }
        
        logger.info(f"Cached result for {kpi_name}")
    
    def invalidate(self, dataset_id: str):
        # Invalidate all cache entries for a dataset
        keys_to_delete = []
        
        for cache_key, cached_item in self.cache.items():
            # Check if this cache entry belongs to the dataset
            # This is a simple implementation - in production, you'd store dataset_id in the cache
            if dataset_id in str(cached_item["data"]):
                keys_to_delete.append(cache_key)
        
        for key in keys_to_delete:
            del self.cache[key]
        
        logger.info(f"Invalidated {len(keys_to_delete)} cache entries for dataset {dataset_id}")
    
    def clear(self):
        # Clear all cache
        self.cache.clear()
        logger.info("Cache cleared")


# Global cache manager instance
cache_manager = CacheManager()
