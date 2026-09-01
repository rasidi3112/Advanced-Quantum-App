from qiskit import QuantumCircuit


def create_quantum_walk_circuit(steps: int = 3) -> QuantumCircuit:
    position_qubits = 3
    coin_qubit = 1
    n_qubits = position_qubits + coin_qubit

    qc = QuantumCircuit(n_qubits, position_qubits, name="Quantum Walk")

    qc.x(1)

    for _ in range(steps):
        qc.h(0)
        qc.barrier()

        qc.cx(0, 1)
        qc.x(0)
        qc.cx(0, 2)
        qc.x(0)
        qc.barrier()

    qc.measure(range(1, n_qubits), range(position_qubits))

    return qc
