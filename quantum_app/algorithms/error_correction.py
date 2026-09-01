from qiskit import QuantumCircuit


def create_error_correction_circuit() -> QuantumCircuit:
    qc = QuantumCircuit(5, 1, name="Error Correction")

    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.barrier()

    qc.x(1)
    qc.barrier()

    qc.cx(0, 3)
    qc.cx(1, 3)
    qc.cx(1, 4)
    qc.cx(2, 4)
    qc.barrier()

    qc.ccx(3, 4, 0)
    qc.measure(0, 0)

    return qc
