import numpy as np

import q_simulator_bp_feljon as qs


def test_einsum_single():
    """test the einsum implementation of the H gate on a single qubit"""
    for N in [2, 5, 7]:
        for i in range(N):
            statevec = np.array([0] * (2**N), dtype=complex)
            statevec[0] = 1
            psi = np.reshape(statevec, (2,) * N, order="F")
            statevec_soll = np.array([0] * (2**N), dtype=complex)
            statevec_soll[2**i] = statevec_soll[0] = 1 / np.sqrt(2)
            psi_soll = np.reshape(statevec_soll, (2,) * N, order="F")
            result = qs._apply_unitary(psi, qs.H, i)
            print(result, psi_soll)
            assert np.allclose(result, psi_soll)
