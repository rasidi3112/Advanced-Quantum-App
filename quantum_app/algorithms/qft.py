from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT


def create_qft_circuit(n_qubits: int = 4) -> QuantumCircuit:
    qc = QuantumCircuit(n_qubits, n_qubits, name="QFT")

    qc.x(0)
    qc.barrier()

    qc.append(QFT(n_qubits, do_swaps=False), range(n_qubits))

    for i in range(n_qubits // 2):
        qc.swap(i, n_qubits - i - 1)

    qc.barrier()
    qc.measure(range(n_qubits), range(n_qubits))

    return qc
