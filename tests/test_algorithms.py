import pytest
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

from quantum_app.algorithms.entanglement import create_entanglement_circuit
from quantum_app.algorithms.teleportation import create_teleportation_circuit
from quantum_app.algorithms.grover import create_grover_circuit
from quantum_app.algorithms.qft import create_qft_circuit
from quantum_app.algorithms.phase_estimation import create_phase_estimation_circuit
from quantum_app.algorithms.vqe import create_vqe_circuit
from quantum_app.algorithms.quantum_walk import create_quantum_walk_circuit
from quantum_app.algorithms.error_correction import create_error_correction_circuit
from quantum_app.algorithms.deutsch_jozsa import create_deutsch_jozsa_circuit
from quantum_app.algorithms.bernstein_vazirani import create_bernstein_vazirani_circuit
from quantum_app.algorithms.simon import create_simon_circuit
from quantum_app.core import AdvancedQuantumApp
from quantum_app.utils import format_counts, format_header, calculate_fidelity


@pytest.fixture
def simulator():
    return AerSimulator()


@pytest.fixture
def app():
    return AdvancedQuantumApp()


def run_circuit(simulator, circuit, shots=1024):
    compiled = transpile(circuit, simulator)
    job = simulator.run(compiled, shots=shots)
    return job.result().get_counts()


class TestCircuitGeneration:

    def test_entanglement_circuit(self):
        circuit = create_entanglement_circuit(n_pairs=2)
        assert isinstance(circuit, QuantumCircuit)
        assert circuit.num_qubits == 4
        assert circuit.num_clbits == 4

    def test_entanglement_single_pair(self):
        circuit = create_entanglement_circuit(n_pairs=1)
        assert circuit.num_qubits == 2

    def test_teleportation_circuit(self):
        circuit = create_teleportation_circuit()
        assert isinstance(circuit, QuantumCircuit)
        assert circuit.num_qubits == 3
        assert circuit.num_clbits == 3

    def test_grover_circuit(self):
        circuit = create_grover_circuit(n_qubits=3, target='101')
        assert isinstance(circuit, QuantumCircuit)
        assert circuit.num_qubits == 3

    def test_grover_invalid_target(self):
        with pytest.raises(ValueError, match="Target length"):
            create_grover_circuit(n_qubits=3, target='10')

    def test_qft_circuit(self):
        circuit = create_qft_circuit(n_qubits=4)
        assert isinstance(circuit, QuantumCircuit)
        assert circuit.num_qubits == 4

    def test_phase_estimation_circuit(self):
        circuit = create_phase_estimation_circuit(n_counting_qubits=3)
        assert isinstance(circuit, QuantumCircuit)
        assert circuit.num_qubits == 4
        assert circuit.num_clbits == 3

    def test_vqe_circuit(self):
        circuit = create_vqe_circuit(n_qubits=2)
        assert isinstance(circuit, QuantumCircuit)
        assert circuit.num_qubits == 2

    def test_quantum_walk_circuit(self):
        circuit = create_quantum_walk_circuit(steps=3)
        assert isinstance(circuit, QuantumCircuit)
        assert circuit.num_qubits == 4

    def test_error_correction_circuit(self):
        circuit = create_error_correction_circuit()
        assert isinstance(circuit, QuantumCircuit)
        assert circuit.num_qubits == 5
        assert circuit.num_clbits == 1

    def test_deutsch_jozsa_circuit(self):
        circuit = create_deutsch_jozsa_circuit(n_qubits=3, oracle_type="balanced")
        assert isinstance(circuit, QuantumCircuit)
        assert circuit.num_qubits == 4
        assert circuit.num_clbits == 3

    def test_deutsch_jozsa_constant(self):
        circuit = create_deutsch_jozsa_circuit(n_qubits=3, oracle_type="constant")
        assert isinstance(circuit, QuantumCircuit)

    def test_deutsch_jozsa_invalid_oracle(self):
        with pytest.raises(ValueError, match="Unknown oracle type"):
            create_deutsch_jozsa_circuit(oracle_type="invalid")

    def test_bernstein_vazirani_circuit(self):
        circuit = create_bernstein_vazirani_circuit(secret="101")
        assert isinstance(circuit, QuantumCircuit)
        assert circuit.num_qubits == 4
        assert circuit.num_clbits == 3

    def test_simon_circuit(self):
        circuit = create_simon_circuit(secret="110")
        assert isinstance(circuit, QuantumCircuit)
        assert circuit.num_qubits == 6
        assert circuit.num_clbits == 3


class TestCircuitExecution:

    def test_entanglement_execution(self, simulator):
        circuit = create_entanglement_circuit(n_pairs=1)
        counts = run_circuit(simulator, circuit, shots=2048)
        for state in counts:
            assert state in ("00", "11"), f"Unexpected state: {state}"

    def test_grover_finds_target(self, simulator):
        target = '101'
        circuit = create_grover_circuit(n_qubits=3, target=target)
        counts = run_circuit(simulator, circuit, shots=2048)
        top_state = max(counts, key=counts.get)
        assert top_state == target, f"Grover didn't find target. Top: {top_state}"

    def test_deutsch_jozsa_balanced(self, simulator):
        circuit = create_deutsch_jozsa_circuit(n_qubits=3, oracle_type="balanced")
        counts = run_circuit(simulator, circuit, shots=1024)
        assert "000" not in counts, "Balanced oracle incorrectly identified as constant"

    def test_deutsch_jozsa_constant(self, simulator):
        circuit = create_deutsch_jozsa_circuit(n_qubits=3, oracle_type="constant")
        counts = run_circuit(simulator, circuit, shots=1024)
        assert list(counts.keys()) == ["000"], (
            f"Constant oracle not identified. Got: {counts}"
        )

    def test_bernstein_vazirani_finds_secret(self, simulator):
        secret = "101"
        circuit = create_bernstein_vazirani_circuit(secret=secret)
        counts = run_circuit(simulator, circuit, shots=1024)
        top_state = max(counts, key=counts.get)
        assert top_state == secret, f"BV didn't find secret. Top: {top_state}"

    def test_error_correction_succeeds(self, simulator):
        circuit = create_error_correction_circuit()
        counts = run_circuit(simulator, circuit, shots=1024)
        assert len(counts) == 1, f"Error correction not deterministic. Got: {counts}"
        assert sum(counts.values()) == 1024


class TestAdvancedQuantumApp:

    def test_initialization(self, app):
        assert app.simulator is not None
        assert app.results_history == []

    def test_execute_circuit(self, app):
        circuit = create_entanglement_circuit(n_pairs=1)
        counts = app.execute_circuit(circuit, shots=512, name="test")
        assert isinstance(counts, dict)
        assert len(counts) > 0
        assert len(app.results_history) == 1
        assert app.results_history[0]["name"] == "test"
        assert app.results_history[0]["shots"] == 512

    def test_get_all_demos(self, app):
        demos = app.get_all_demos()
        assert len(demos) == 11
        for name, circuit, palette_key in demos:
            assert isinstance(name, str)
            assert isinstance(circuit, QuantumCircuit)
            assert isinstance(palette_key, str)

    def test_analyze_entanglement(self, app):
        circuit = create_entanglement_circuit(n_pairs=1)
        ent = app.analyze_entanglement(circuit)
        assert isinstance(ent, float)
        assert ent >= 0


class TestUtils:

    def test_format_counts(self):
        counts = {"00": 512, "11": 512}
        result = format_counts(counts, shots=1024)
        assert "|00⟩" in result or "|11⟩" in result
        assert "50.00%" in result

    def test_format_header(self):
        header = format_header("Test Title")
        assert "Test Title" in header
        assert "═" in header

    def test_calculate_fidelity(self):
        counts = {"101": 900, "000": 100, "111": 24}
        fidelity = calculate_fidelity(counts, "101", shots=1024)
        assert abs(fidelity - 900 / 1024) < 1e-6

    def test_calculate_fidelity_missing_state(self):
        counts = {"00": 1024}
        fidelity = calculate_fidelity(counts, "11", shots=1024)
        assert fidelity == 0.0
