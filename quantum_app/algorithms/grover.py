import numpy as np
from qiskit import QuantumCircuit


def _apply_oracle(circuit: QuantumCircuit, target_bits: str, n_qubits: int) -> None:
    for i, bit in enumerate(target_bits):
        if bit == '0':
            circuit.x(i)

    circuit.h(n_qubits - 1)
    circuit.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    circuit.h(n_qubits - 1)

    for i, bit in enumerate(target_bits):
        if bit == '0':
            circuit.x(i)


def _apply_diffusion(circuit: QuantumCircuit, n_qubits: int) -> None:
    circuit.h(range(n_qubits))
    circuit.x(range(n_qubits))
    circuit.h(n_qubits - 1)
    circuit.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    circuit.h(n_qubits - 1)
    circuit.x(range(n_qubits))
    circuit.h(range(n_qubits))


def create_grover_circuit(n_qubits: int = 3, target: str = '101') -> QuantumCircuit:
    if len(target) != n_qubits:
        raise ValueError(
            f"Target length ({len(target)}) must match n_qubits ({n_qubits})"
        )

    qc = QuantumCircuit(n_qubits, n_qubits, name="Grover Search")

    qc.h(range(n_qubits))

    iterations = int(np.pi / 4 * np.sqrt(2 ** n_qubits))
    for _ in range(iterations):
        _apply_oracle(qc, target, n_qubits)
        qc.barrier()
        _apply_diffusion(qc, n_qubits)
        qc.barrier()

    qc.measure(range(n_qubits), range(n_qubits))
    return qc
