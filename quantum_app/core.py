import time
from typing import Dict, List, Optional, Tuple

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, DensityMatrix, entropy

from quantum_app.algorithms import (
    create_entanglement_circuit,
    create_teleportation_circuit,
    create_grover_circuit,
    create_qft_circuit,
    create_phase_estimation_circuit,
    create_vqe_circuit,
    create_quantum_walk_circuit,
    create_error_correction_circuit,
    create_deutsch_jozsa_circuit,
    create_bernstein_vazirani_circuit,
    create_simon_circuit,
)
from quantum_app.visualization import plot_histogram_premium, plot_comparison
from quantum_app.utils import (
    logger,
    format_counts,
    format_header,
    format_circuit_info,
    print_summary,
)


class AdvancedQuantumApp:

    def __init__(self):
        self.simulator = AerSimulator()
        self.results_history: List[Dict] = []
        logger.info("AdvancedQuantumApp initialized with AerSimulator")

    def execute_circuit(self, circuit: QuantumCircuit,
                         shots: int = 1024,
                         name: Optional[str] = None) -> Dict[str, int]:
        start_time = time.perf_counter()

        compiled_circuit = transpile(circuit, self.simulator)
        job = self.simulator.run(compiled_circuit, shots=shots)
        result = job.result()
        counts = result.get_counts()

        execution_time = time.perf_counter() - start_time

        self.results_history.append({
            "name": name or circuit.name,
            "circuit": circuit.name,
            "counts": counts,
            "shots": shots,
            "execution_time": execution_time,
            "num_qubits": circuit.num_qubits,
            "depth": circuit.depth(),
        })

        return counts

    def analyze_entanglement(self, circuit: QuantumCircuit) -> float:
        statevector = Statevector.from_instruction(
            circuit.remove_final_measurements(inplace=False)
        )
        density_matrix = DensityMatrix(statevector)
        return entropy(density_matrix, base=2)

    def visualize(self, counts: Dict[str, int], title: str = "Quantum Results",
                   save_path: Optional[str] = None,
                   palette_key: Optional[str] = None,
                   show: bool = True) -> Optional[str]:
        return plot_histogram_premium(
            counts, title=title, save_path=save_path,
            palette_key=palette_key, show=show,
        )

    def get_all_demos(self) -> List[Tuple[str, QuantumCircuit, str]]:
        return [
            ("Quantum Entanglement (Bell States)",
             create_entanglement_circuit(n_pairs=2), "entanglement"),
            ("Quantum Teleportation",
             create_teleportation_circuit(), "teleportation"),
            ("Grover's Search Algorithm (target: |101⟩)",
             create_grover_circuit(n_qubits=3, target='101'), "grover"),
            ("Quantum Fourier Transform",
             create_qft_circuit(n_qubits=4), "qft"),
            ("Quantum Phase Estimation",
             create_phase_estimation_circuit(n_counting_qubits=3), "phase_estimation"),
            ("Variational Quantum Eigensolver",
             create_vqe_circuit(n_qubits=2), "vqe"),
            ("Quantum Random Walk",
             create_quantum_walk_circuit(steps=3), "quantum_walk"),
            ("Quantum Error Correction (3-qubit)",
             create_error_correction_circuit(), "error_correction"),
            ("Deutsch-Jozsa Algorithm",
             create_deutsch_jozsa_circuit(n_qubits=3), "deutsch_jozsa"),
            ("Bernstein-Vazirani Algorithm (secret: 101)",
             create_bernstein_vazirani_circuit(secret="101"), "bernstein_vazirani"),
            ("Simon's Algorithm (secret: 110)",
             create_simon_circuit(secret="110"), "simon"),
        ]

    def run_comprehensive_demo(self, shots: int = 2048,
                                 save_images: bool = False,
                                 images_dir: str = "images",
                                 show_plots: bool = True) -> None:
        print("═" * 80)
        print("🌌  ADVANCED QUANTUM COMPUTING APPLICATION v2.0")
        print("═" * 80)
        print(f"   Simulator: AerSimulator")
        print(f"   Shots per algorithm: {shots:,}")
        print(f"   Algorithms: {len(self.get_all_demos())}")
        print("═" * 80)

        all_results = {}

        for name, circuit, palette_key in self.get_all_demos():
            print(format_header(name))

            print(format_circuit_info(circuit, name))
            print()

            print("  Circuit Diagram:")
            diagram_lines = str(circuit.draw(output='text')).split('\n')
            for line in diagram_lines:
                print(f"    {line}")

            counts = self.execute_circuit(circuit, shots=shots, name=name)
            all_results[name] = counts

            print(f"\n  📊 Measurement Results (top 5):")
            print(format_counts(counts, shots))

            exec_time = self.results_history[-1]["execution_time"]
            print(f"\n  ⏱  Execution time: {exec_time:.4f}s")

            save_path = None
            if save_images:
                safe_name = palette_key or name.lower().replace(" ", "_")
                save_path = f"{images_dir}/{safe_name}_histogram.png"

            self.visualize(
                counts, title=name, save_path=save_path,
                palette_key=palette_key, show=show_plots,
            )

            if save_path:
                print(f"  💾 Saved: {save_path}")

        print_summary(self.results_history)

        print("\n✅ All quantum algorithms executed successfully!")

    def run_custom_ghz(self, n_qubits: int = 3, shots: int = 4096,
                        save_images: bool = False,
                        images_dir: str = "images",
                        show_plots: bool = True) -> Dict[str, int]:
        print(format_header(f"Custom GHZ State ({n_qubits} qubits)", emoji="🎯"))

        qc = QuantumCircuit(n_qubits, n_qubits, name="GHZ State")
        qc.h(0)
        for i in range(1, n_qubits):
            qc.cx(0, i)
        qc.measure(range(n_qubits), range(n_qubits))

        print(format_circuit_info(qc, f"GHZ-{n_qubits}"))
        print(f"\n  Circuit Diagram:")
        diagram_lines = str(qc.draw(output='text')).split('\n')
        for line in diagram_lines:
            print(f"    {line}")

        counts = self.execute_circuit(qc, shots=shots, name=f"GHZ State ({n_qubits}q)")

        print(f"\n  📊 Measurement Results:")
        print(format_counts(counts, shots))

        save_path = None
        if save_images:
            save_path = f"{images_dir}/ghz_state_histogram.png"

        self.visualize(
            counts, title=f"GHZ State ({n_qubits} qubits)",
            save_path=save_path, palette_key="ghz",
            show=show_plots,
        )

        return counts
