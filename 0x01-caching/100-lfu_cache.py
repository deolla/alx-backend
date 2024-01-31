#!/usr/bin/env python3
"""Create a class LFUCache that inherits from BaseCaching."""
from collections import OrderedDict

BaseCaching = __import__("base_caching").BaseCaching


class LFUCache(BaseCaching):
    """A caching system using LFU eviction strategy."""

    def __init__(self):
        super().__init__()
        self.lfu_order = []

    def put(self, key, item):
        """Add an item to the cache."""
        if key and item:
            if key in self.cache_data:
                self.cache_data[key] = item
                self.lfu_order.remove(key)
            else:
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    lfu = self.lfu_order.pop(0)
                    del self.cache_data[lfu]
                    print("DISCARD: {}".format(lfu))
                self.cache_data[key] = item
            self.lfu_order.append(key)

    def get(self, key):
        """Get an item from the cache."""
        if key and key in self.cache_data:
            self.lfu_order.remove(key)
            self.lfu_order.append(key)
            return self.cache_data[key]
        return None
