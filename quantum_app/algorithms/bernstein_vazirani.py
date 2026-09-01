from qiskit import QuantumCircuit


def _bv_oracle(circuit: QuantumCircuit, secret: str, n_qubits: int) -> None:
    for i, bit in enumerate(reversed(secret)):
        if bit == '1':
            circuit.cx(i, n_qubits)


def create_bernstein_vazirani_circuit(secret: str = "101") -> QuantumCircuit:
    n_qubits = len(secret)
    total_qubits = n_qubits + 1
    qc = QuantumCircuit(total_qubits, n_qubits, name="Bernstein-Vazirani")

    qc.x(n_qubits)

    qc.h(range(total_qubits))
    qc.barrier()

    _bv_oracle(qc, secret, n_qubits)
    qc.barrier()

    qc.h(range(n_qubits))

    qc.measure(range(n_qubits), range(n_qubits))

    return qc
