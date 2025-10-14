"""
Advanced Quantum Computing Application
Aplikasi Quantum Computing Canggih dengan Multiple Algorithms
"""

import numpy as np # type: ignore
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile # type: ignore
from qiskit_aer import AerSimulator # type: ignore
from qiskit.visualization import plot_histogram, plot_bloch_multivector, circuit_drawer # type: ignore
from qiskit.quantum_info import Statevector, DensityMatrix, entropy # type: ignore
from qiskit.circuit.library import QFT, GroverOperator # type: ignore
import matplotlib.pyplot as plt # type: ignore
from typing import List, Dict, Tuple
import time

class AdvancedQuantumApp:
    """Aplikasi Quantum Computing dengan berbagai algoritma canggih"""
    
    def __init__(self):
        self.simulator = AerSimulator()
        self.results_history = []
        
    def create_superposition(self, n_qubits: int) -> QuantumCircuit:
        """Membuat superposisi quantum untuk n qubits"""
        qc = QuantumCircuit(n_qubits)
        qc.h(range(n_qubits))  # Hadamard gate untuk semua qubit
        return qc
    
    def quantum_entanglement(self, n_pairs: int = 2) -> QuantumCircuit:
        """
        Membuat Bell States - Quantum Entanglement
        Mendemonstrasikan fenomena keterikatan quantum
        """
        qc = QuantumCircuit(n_pairs * 2, n_pairs * 2)
        
        for i in range(n_pairs):
            # Buat superposisi
            qc.h(i * 2)
            # Buat entanglement dengan CNOT
            qc.cx(i * 2, i * 2 + 1)
            
        qc.barrier()
        qc.measure(range(n_pairs * 2), range(n_pairs * 2))
        
        return qc
    
    def quantum_teleportation(self) -> QuantumCircuit:
        """
        Implementasi Quantum Teleportation Protocol
        Mentransfer state quantum dari satu qubit ke qubit lain
        """
        qc = QuantumCircuit(3, 3)
        
        # Persiapan state yang akan di-teleport (contoh: |+⟩)
        qc.h(0)
        qc.barrier()
        
        # Buat Bell pair (entanglement antara qubit 1 dan 2)
        qc.h(1)
        qc.cx(1, 2)
        qc.barrier()
        
        # Protokol teleportasi
        qc.cx(0, 1)
        qc.h(0)
        qc.barrier()
        
        # Pengukuran
        qc.measure([0, 1], [0, 1])
        qc.barrier()
        
        # Koreksi kondisional
        qc.cx(1, 2)
        qc.cz(0, 2)
        qc.measure(2, 2)
        
        return qc
    
    def grover_search(self, n_qubits: int = 3, target: str = '101') -> QuantumCircuit:
        """
        Algoritma Grover untuk pencarian quantum
        Kompleksitas: O(√N) vs klasik O(N)
        """
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        # Inisialisasi superposisi
        qc.h(range(n_qubits))
        
        # Oracle untuk target (simplified)
        def oracle(circuit, target_bits):
            # Tandai state target dengan phase flip
            for i, bit in enumerate(target_bits):
                if bit == '0':
                    circuit.x(i)
            circuit.h(n_qubits - 1)
            circuit.mcx(list(range(n_qubits - 1)), n_qubits - 1)
            circuit.h(n_qubits - 1)
            for i, bit in enumerate(target_bits):
                if bit == '0':
                    circuit.x(i)
        
        # Diffusion operator
        def diffusion(circuit, n):
            circuit.h(range(n))
            circuit.x(range(n))
            circuit.h(n - 1)
            circuit.mcx(list(range(n - 1)), n - 1)
            circuit.h(n - 1)
            circuit.x(range(n))
            circuit.h(range(n))
        
        # Iterasi Grover (optimal: π/4 * √(2^n))
        iterations = int(np.pi / 4 * np.sqrt(2 ** n_qubits))
        for _ in range(iterations):
            oracle(qc, target)
            qc.barrier()
            diffusion(qc, n_qubits)
            qc.barrier()
        
        qc.measure(range(n_qubits), range(n_qubits))
        return qc
    
    def quantum_fourier_transform(self, n_qubits: int = 4) -> QuantumCircuit:
        """
        Quantum Fourier Transform (QFT)
        Fundamental untuk algoritma Shor dan phase estimation
        """
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        # Persiapan state awal (contoh)
        qc.x(0)
        qc.barrier()
        
        # Implementasi QFT
        qc.append(QFT(n_qubits, do_swaps=False), range(n_qubits))
        
        # Swap qubits
        for i in range(n_qubits // 2):
            qc.swap(i, n_qubits - i - 1)
        
        qc.barrier()
        qc.measure(range(n_qubits), range(n_qubits))
        
        return qc
    
    def quantum_phase_estimation(self, n_counting_qubits: int = 3) -> QuantumCircuit:
        """
        Quantum Phase Estimation Algorithm
        Digunakan untuk menemukan eigenvalue dari unitary operator
        """
        n_qubits = n_counting_qubits + 1
        qc = QuantumCircuit(n_qubits, n_counting_qubits)
        
        # Persiapan eigenstate (qubit terakhir)
        qc.x(n_counting_qubits)
        
        # Hadamard pada counting qubits
        qc.h(range(n_counting_qubits))
        qc.barrier()
        
        # Controlled unitary operations (contoh: T gate)
        for i in range(n_counting_qubits):
            for _ in range(2 ** i):
                qc.cp(np.pi / 4, i, n_counting_qubits)
        
        qc.barrier()
        
        # Inverse QFT
        qc.append(QFT(n_counting_qubits, inverse=True), range(n_counting_qubits))
        
        qc.measure(range(n_counting_qubits), range(n_counting_qubits))
        
        return qc
    
    def variational_quantum_eigensolver(self, n_qubits: int = 2) -> QuantumCircuit:
        """
        Variational Quantum Eigensolver (VQE)
        Algoritma hybrid quantum-klasik untuk ground state
        """
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        # Ansatz layer 1
        for i in range(n_qubits):
            qc.ry(np.pi / 4, i)
        
        # Entangling layer
        for i in range(n_qubits - 1):
            qc.cx(i, i + 1)
        qc.barrier()
        
        # Ansatz layer 2
        for i in range(n_qubits):
            qc.ry(np.pi / 3, i)
        
        qc.measure(range(n_qubits), range(n_qubits))
        
        return qc
    
    def quantum_walk(self, steps: int = 3) -> QuantumCircuit:
        """
        Quantum Random Walk
        Demonstrasi superposisi dalam pergerakan quantum
        """
        position_qubits = 3
        coin_qubit = 1
        n_qubits = position_qubits + coin_qubit
        
        qc = QuantumCircuit(n_qubits, position_qubits)
        
        # Inisialisasi posisi tengah
        qc.x(1)
        
        for _ in range(steps):
            # Coin flip (Hadamard)
            qc.h(0)
            qc.barrier()
            
            # Conditional shift
            qc.cx(0, 1)
            qc.x(0)
            qc.cx(0, 2)
            qc.x(0)
            qc.barrier()
        
        qc.measure(range(1, n_qubits), range(position_qubits))
        
        return qc
    
    def quantum_error_correction(self) -> QuantumCircuit:
        """
        Bit Flip Error Correction Code (3-qubit)
        Mendemonstrasikan koreksi error quantum dasar
        """
        qc = QuantumCircuit(5, 1)
        
        # Encode: |ψ⟩ → |ψψψ⟩
        qc.cx(0, 1)
        qc.cx(0, 2)
        qc.barrier()
        
        # Simulasi error (flip qubit 1)
        qc.x(1)
        qc.barrier()
        
        # Syndrome measurement
        qc.cx(0, 3)
        qc.cx(1, 3)
        qc.cx(1, 4)
        qc.cx(2, 4)
        qc.barrier()
        
        # Correction
        qc.ccx(3, 4, 0)
        qc.measure(0, 0)
        
        return qc
    
    def execute_circuit(self, circuit: QuantumCircuit, shots: int = 1024) -> Dict:
        """Eksekusi circuit dan return hasil"""
        start_time = time.time()
        
        compiled_circuit = transpile(circuit, self.simulator)
        job = self.simulator.run(compiled_circuit, shots=shots)
        result = job.result()
        counts = result.get_counts()
        
        execution_time = time.time() - start_time
        
        # Simpan ke history
        self.results_history.append({
            'circuit': circuit.name,
            'counts': counts,
            'shots': shots,
            'execution_time': execution_time
        })
        
        return counts
    
    def analyze_entanglement(self, circuit: QuantumCircuit) -> float:
        """Analisis tingkat entanglement menggunakan entropy"""
        statevector = Statevector.from_instruction(circuit.remove_final_measurements(inplace=False))
        density_matrix = DensityMatrix(statevector)
        
        # Von Neumann entropy
        return entropy(density_matrix, base=2)
    
    def visualize_results(self, counts: Dict, title: str = "Quantum Results"):
        """Visualisasi hasil pengukuran"""
        plt.figure(figsize=(12, 6))
        plot_histogram(counts, title=title, figsize=(12, 6), color='#FF6B6B')
        plt.tight_layout()
        plt.show()
    
    def run_comprehensive_demo(self):
        """Menjalankan demo komprehensif semua algoritma"""
        print("=" * 80)
        print("🌌 ADVANCED QUANTUM COMPUTING APPLICATION")
        print("=" * 80)
        
        demos = [
            ("Quantum Entanglement (Bell States)", self.quantum_entanglement(2)),
            ("Quantum Teleportation", self.quantum_teleportation()),
            ("Grover's Search Algorithm", self.grover_search(3, '101')),
            ("Quantum Fourier Transform", self.quantum_fourier_transform(4)),
            ("Quantum Phase Estimation", self.quantum_phase_estimation(3)),
            ("Variational Quantum Eigensolver", self.variational_quantum_eigensolver(2)),
            ("Quantum Walk", self.quantum_walk(3)),
            ("Quantum Error Correction", self.quantum_error_correction())
        ]
        
        for name, circuit in demos:
            print(f"\n{'=' * 80}")
            print(f"🔬 Running: {name}")
            print(f"{'=' * 80}")
            
            # Tampilkan circuit
            print(f"\n📊 Circuit Diagram:")
            print(circuit.draw(output='text'))
            
            # Eksekusi
            counts = self.execute_circuit(circuit, shots=2048)
            
            # Analisis
            print(f"\n📈 Results:")
            sorted_counts = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5])
            for state, count in sorted_counts.items():
                probability = (count / 2048) * 100
                print(f"   |{state}⟩: {count} times ({probability:.2f}%)")
            
            # Visualisasi
            self.visualize_results(counts, title=name)
            
            print(f"\n⏱️  Execution time: {self.results_history[-1]['execution_time']:.4f} seconds")
        
        print(f"\n{'=' * 80}")
        print("✅ All quantum algorithms executed successfully!")
        print(f"{'=' * 80}")

# ===========================
# MAIN EXECUTION
# ===========================

if __name__ == "__main__":
    # Inisialisasi aplikasi
    app = AdvancedQuantumApp()
    
    # Jalankan demo komprehensif
    app.run_comprehensive_demo()
    
    # Contoh penggunaan individual
    print("\n\n" + "=" * 80)
    print("🎯 CUSTOM QUANTUM CIRCUIT EXAMPLE")
    print("=" * 80)
    
    # Buat circuit custom
    custom_circuit = QuantumCircuit(3, 3)
    custom_circuit.h(0)
    custom_circuit.cx(0, 1)
    custom_circuit.cx(1, 2)
    custom_circuit.measure([0, 1, 2], [0, 1, 2])
    
    print("\nCustom GHZ State Circuit:")
    print(custom_circuit.draw(output='text'))
    
    results = app.execute_circuit(custom_circuit, shots=4096)
    app.visualize_results(results, title="Custom GHZ State")
    
    print("\n🎉 Quantum Computing Demo Complete!")