#!/usr/bin/env python3
"""Create a class LFUCache that inherits from BaseCaching."""
from collections import OrderedDict

BaseCaching = __import__("base_caching").BaseCaching


class LFUCache(BaseCaching):
    """A caching system using LFU eviction strategy."""

    def __init__(self):
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Add an item to the cache."""
        if key is not None and item is not None:
            self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            first = next(iter(self.cache_data))
            print("DISCARD: {}".format(first))
            self.cache_data.pop(first)

    def get(self, key):
        """Get an item from the cache."""
        if key is not None and key in self.cache_data:
            self.cache_data.move_to_end(key)
            return self.cache_data[key]
        return None
