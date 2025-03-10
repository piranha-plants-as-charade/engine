import numpy as np
from numpy.typing import NDArray


def mode(arr: NDArray[np.float16]) -> np.float64 | None:
    int_arr = arr[~np.isnan(arr)].astype(np.int32)
    if int_arr.size == 0:
        return None
    counts = np.bincount(int_arr)
    return np.argmax(counts).astype(np.float64)
