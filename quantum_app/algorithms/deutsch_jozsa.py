from qiskit import QuantumCircuit


def _balanced_oracle(circuit: QuantumCircuit, n_qubits: int) -> None:
    for i in range(n_qubits):
        circuit.cx(i, n_qubits)


def create_deutsch_jozsa_circuit(n_qubits: int = 3,
                                  oracle_type: str = "balanced") -> QuantumCircuit:
    total_qubits = n_qubits + 1
    qc = QuantumCircuit(total_qubits, n_qubits, name="Deutsch-Jozsa")

    qc.x(n_qubits)

    qc.h(range(total_qubits))
    qc.barrier()

    if oracle_type == "balanced":
        _balanced_oracle(qc, n_qubits)
    elif oracle_type == "constant":
        pass
    else:
        raise ValueError(f"Unknown oracle type: {oracle_type}. Use 'balanced' or 'constant'.")

    qc.barrier()

    qc.h(range(n_qubits))

    qc.measure(range(n_qubits), range(n_qubits))

    return qc
