#!/usr/bin/env python3
"""Create a class BasicCache that inherits from BaseCaching."""

BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    def put(self, key, item):
        """Assign to the dictionary self.cache_data"""
        if key is None or item is None:
            return

        self.cache_data[key] = item

    def get(self, key):
        if key is None or key not in self.cache_data:
            return None

        retrieve_value = self.cache_data[key]
        return retrieve_value
