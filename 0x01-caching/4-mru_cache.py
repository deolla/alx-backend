#!/usr/bin/env python3
"""Create a class MRUCache that inherits from BaseCaching."""
BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """A caching system using MRU eviction strategy."""
    def __init__(self):
        """Initializes the MRUCache instance"""
        super().__init__()
        self.mru_order = []

    def put(self, key, item):
        """
        Adds an item to the cache using MRU algorithm
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Get the most recently used item (MRU)
                mru_key = self.mru_order.pop()
                del self.cache_data[mru_key]
                print("DISCARD:", mru_key)

            # Add the new item
            self.cache_data[key] = item
            self.mru_order.append(key)

    def get(self, key):
        """
        Retrieves the value from the cache linked to the given key
        """
        if key is not None and key in self.cache_data:
            # Move the accessed key to the end of MRU order
            self.mru_order.remove(key)
            self.mru_order.append(key)
            return self.cache_data[key]
        return None
