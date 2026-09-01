import numpy as np
from qiskit import QuantumCircuit


def create_vqe_circuit(n_qubits: int = 2, theta_1: float = np.pi / 4,
                        theta_2: float = np.pi / 3) -> QuantumCircuit:
    qc = QuantumCircuit(n_qubits, n_qubits, name="VQE Ansatz")

    for i in range(n_qubits):
        qc.ry(theta_1, i)

    for i in range(n_qubits - 1):
        qc.cx(i, i + 1)
    qc.barrier()

    for i in range(n_qubits):
        qc.ry(theta_2, i)

    qc.measure(range(n_qubits), range(n_qubits))

    return qc
