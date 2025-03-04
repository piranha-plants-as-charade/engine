import numpy as np
from typing import DefaultDict, Dict, List
from numpy.typing import NDArray
from collections import defaultdict
from functools import cache


class AudioData:

    def __init__(self, init_data: List[np.float32] = list()):
        self._data: DefaultDict[int, np.float32] = defaultdict(lambda: np.float32(0))
        for i, datem in enumerate(init_data):
            self.set(i, datem)

    @cache
    def as_array(self) -> NDArray[np.float32]:
        return np.array([self._data[i] for i in range(max(self._data.keys()))])

    def at(self, idx: int) -> np.float32:
        return self._data[idx]

    def set(self, idx: int, val: np.float32):
        assert idx >= 0
        self._data[idx] = val
        if val == 0:
            del self._data[idx]
        self.as_array.cache_clear()

    def add(self, idx: int, val: np.float32):
        self.set(idx, self.at(idx) + val)

    def pad_start(self, n: int):
        new_dict: Dict[int, np.float32] = dict()
        for key, val in self._data.items():
            new_dict[key + n] = val
        self._data = defaultdict(lambda: np.float32(0), new_dict)
        self.as_array.cache_clear()
