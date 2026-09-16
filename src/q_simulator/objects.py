from dataclasses import dataclass

import numpy as np


@dataclass
class Configuration:
    method: str = "default"
    number_of_shots: int = 2**16


class Result:
    def __init__(self, counts: dict, statevector: np.ndarray):
        self.counts = counts
        self.statevector = statevector
