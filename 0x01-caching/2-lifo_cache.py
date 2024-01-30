#!/usr/bin/env python3
"""Create a class LIFOCache that inherits from BaseCaching."""
BaseCaching = __import__("base_caching").BaseCaching


class LIFOCache(BaseCaching):
    """LIFO Cache Class"""

    def __init__(self):
        """Initialize LIFO Cache"""
        super().__init__()

    def put(self, key, item):
        """Add an item to the cache"""
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                last_key = list(self.cache_data.keys())[-1]
                del self.cache_data[last_key]
                print(f"DISCARD: {last_key}")
            self.cache_data[key] = item

    def get(self, key):
        """Get an item from the cache"""
        if key is not None and key in self.cache_data:
            return self.cache_data[key]
        return None
