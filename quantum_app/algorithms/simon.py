from qiskit import QuantumCircuit


def _simon_oracle(circuit: QuantumCircuit, secret: str, n_qubits: int) -> None:
    for i in range(n_qubits):
        circuit.cx(i, i + n_qubits)

    first_one = -1
    for i, bit in enumerate(reversed(secret)):
        if bit == '1':
            first_one = i
            break

    if first_one >= 0:
        for i, bit in enumerate(reversed(secret)):
            if bit == '1':
                circuit.cx(first_one, i + n_qubits)


def create_simon_circuit(secret: str = "110") -> QuantumCircuit:
    n_qubits = len(secret)
    total_qubits = 2 * n_qubits
    qc = QuantumCircuit(total_qubits, n_qubits, name="Simon's Algorithm")

    qc.h(range(n_qubits))
    qc.barrier()

    _simon_oracle(qc, secret, n_qubits)
    qc.barrier()

    qc.h(range(n_qubits))

    qc.measure(range(n_qubits), range(n_qubits))

    return qc
