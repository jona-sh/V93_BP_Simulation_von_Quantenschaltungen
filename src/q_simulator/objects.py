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


H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]])
S = np.array([[1, 0], [0, 1j]])
CX = np.zeros((2,) * 4)
CX[0, 0, 0, 0] = 1
CX[0, 1, 0, 1] = 1
CX[1, 0, 1, 1] = 1
CX[1, 1, 1, 0] = 1
