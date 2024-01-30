#!/usr/bin/env python3
"""Create a class LRUCache that inherits from BaseCaching."""

from collections import OrderedDict

BaseCaching = __import__("base_caching").BaseCaching


class LRUCache(BaseCaching):
    """A caching system using LRU eviction strategy"""

    def __init__(self):
        """Initializes the LRUCache instance"""
        super().__init__()
        self.lru_order = []

    def put(self, key, item):
        """
        Adds an item to the cache using LRU algorithm
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Get the least recently used item (LRU)
                lru_key = self.lru_order.pop(0)
                del self.cache_data[lru_key]
                print("DISCARD:", lru_key)

            self.cache_data[key] = item
            self.lru_order.append(key)

    def get(self, key):
        """
        Retrieves the value from the cache linked to the given key
        """
        if key is not None and key in self.cache_data:
            self.lru_order.remove(key)
            self.lru_order.append(key)
            return self.cache_data[key]
        return None
