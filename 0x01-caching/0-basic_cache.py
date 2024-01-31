#!/usr/bin/env python3
"""Create a class BasicCache that inherits from BaseCaching."""
from typing import Any, Optional

BaseCaching = __import__("base_caching").BaseCaching


class BasicCache(BaseCaching):
    """A basic caching system"""

    def __init__(self):
        """Initializes the BasicCache instance"""
        super().__init__()

    def put(self, key: Any, item: Any) -> None:
        """Assign to the dictionary self.cache_data"""
        if key is None or item is None:
            return

        self.cache_data[key] = item

    def get(self, key):
        """Return the value linked to the given key"""
        if key is None or key not in self.cache_data:
            return None

        retrieve_value = self.cache_data[key]
        return retrieve_value
