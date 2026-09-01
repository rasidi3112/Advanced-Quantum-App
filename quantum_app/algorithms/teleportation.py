from qiskit import QuantumCircuit


def create_teleportation_circuit() -> QuantumCircuit:
    qc = QuantumCircuit(3, 3, name="Teleportation")

    qc.h(0)
    qc.barrier()

    qc.h(1)
    qc.cx(1, 2)
    qc.barrier()

    qc.cx(0, 1)
    qc.h(0)
    qc.barrier()

    qc.measure([0, 1], [0, 1])
    qc.barrier()

    qc.cx(1, 2)
    qc.cz(0, 2)
    qc.measure(2, 2)

    return qc
