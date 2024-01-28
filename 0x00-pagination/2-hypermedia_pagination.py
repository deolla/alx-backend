#!/usr/bin/env python3
"""Write a function named index_range that takes
two integer arguments page and page_size."""
from typing import Tuple
import csv
import math
from typing import List


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Return a tuple containing a start index and an end index."""
    start_index = (page - 1) * page_size
    end_index = page_size + start_index
    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Return the appropriate page"""
        assert (
            isinstance(page, int) and page > 0
        ), "page must be a number greater than 0"
        assert (
            isinstance(page_size, int) and page_size > 0
        ), "page_size must be a number greater than 0"

        dataset = self.dataset()
        if dataset is None:
            return []
        start, end = index_range(page, page_size)
        return dataset[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """Return a dictionary containing keys and values"""
        data = self.get_page(page, page_size)
        data_len = len(data)
        total_pages = math.ceil(len(self.dataset()) / page_size)
        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None
        return {
            "page_size": data_len,
            "page": page,
            "data": data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": total_pages,
        }
