import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT


def create_phase_estimation_circuit(n_counting_qubits: int = 3) -> QuantumCircuit:
    n_qubits = n_counting_qubits + 1
    qc = QuantumCircuit(n_qubits, n_counting_qubits, name="Phase Estimation")

    qc.x(n_counting_qubits)

    qc.h(range(n_counting_qubits))
    qc.barrier()

    for i in range(n_counting_qubits):
        for _ in range(2 ** i):
            qc.cp(np.pi / 4, i, n_counting_qubits)

    qc.barrier()

    qc.append(QFT(n_counting_qubits, inverse=True), range(n_counting_qubits))

    qc.measure(range(n_counting_qubits), range(n_counting_qubits))

    return qc
