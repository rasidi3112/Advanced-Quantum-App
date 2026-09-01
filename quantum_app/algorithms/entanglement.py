from qiskit import QuantumCircuit


def create_entanglement_circuit(n_pairs: int = 2) -> QuantumCircuit:
    total_qubits = n_pairs * 2
    qc = QuantumCircuit(total_qubits, total_qubits, name="Bell States")

    for i in range(n_pairs):
        qc.h(i * 2)
        qc.cx(i * 2, i * 2 + 1)

    qc.barrier()
    qc.measure(range(total_qubits), range(total_qubits))

    return qc
