#!/usr/bin/env python3
"""Create a class LFUCache that inherits from BaseCaching."""
from collections import defaultdict
from datetime import datetime

BaseCaching = __import__("base_caching").BaseCaching


class LFUCache(BaseCaching):
    """A caching system using LFU eviction strategy."""

    def __init__(self):
        super().__init__()
        self.frequency_counter = defaultdict(int)
        self.last_used_time = {}

    def put(self, key, item):
        """Add an item to the cache"""
        if key is None or item is None:
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # Find the least frequency used items
            min_frequency = min(self.frequency_counter.values())
            least_frequent_keys = [
                k for k, v in self.frequency_counter.items() if v == min_frequency
            ]

            # If there is more than one least frequent item, use LRU tie-breaking
            if len(least_frequent_keys) > 1:
                least_recently_used_key = min(
                    least_frequent_keys,
                    key=lambda k: self.last_used_time.get(k, datetime.min),
                )
            else:
                least_recently_used_key = least_frequent_keys[0]

            del self.cache_data[least_recently_used_key]
            del self.frequency_counter[least_recently_used_key]
            print(f"DISCARD: {least_recently_used_key}")

        self.cache_data[key] = item
        self.frequency_counter[key] += 1
        self.last_used_time[key] = datetime.now()

    def get(self, key):
        """Retrieve an item from the cache."""
        if key is None or key not in self.cache_data:
            return None

        # Update frequency and last used time for the key
        self.frequency_counter[key] += 1
        self.last_used_time[key] = datetime.now()

        return self.cache_data[key]
