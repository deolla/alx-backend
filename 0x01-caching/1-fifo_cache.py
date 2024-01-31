#!/usr/bin/env python3
"""Create a class FIFOCache that inherits from BaseCaching"""

BaseCaching = __import__("base_caching").BaseCaching


class FIFOCache(BaseCaching):
    """A caching system using FIFO eviction strategy"""

    def __init__(self):
        super().__init__()

    def put(self, key, item):
        """Add an item to the cache"""
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                first_key = next(iter(self.cache_data))
                del self.cache_data[first_key]
                print(f"DISCARD: {first_key}")
            self.cache_data[key] = item

    def get(self, key):
        """Retrieve an item from the cache."""
        if key is not None or key in self.cache_data:
            return self.cache_data[key]
        return None
