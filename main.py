import argparse
import sys
from typing import Optional

from quantum_app import AdvancedQuantumApp, __version__
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
from quantum_app.utils import format_header, format_counts, format_circuit_info
from quantum_app.visualization import plot_histogram_premium

ALGORITHMS = {
    "entanglement": {
        "name": "Quantum Entanglement (Bell States)",
        "create": lambda: create_entanglement_circuit(n_pairs=2),
        "palette": "entanglement",
        "description": "Creates entangled Bell pairs demonstrating quantum correlation",
    },
    "teleportation": {
        "name": "Quantum Teleportation",
        "create": lambda: create_teleportation_circuit(),
        "palette": "teleportation",
        "description": "Transfers quantum state using entanglement and classical bits",
    },
    "grover": {
        "name": "Grover's Search Algorithm",
        "create": lambda: create_grover_circuit(n_qubits=3, target='101'),
        "palette": "grover",
        "description": "Quadratic speedup for unstructured search (target: |101⟩)",
    },
    "qft": {
        "name": "Quantum Fourier Transform",
        "create": lambda: create_qft_circuit(n_qubits=4),
        "palette": "qft",
        "description": "Quantum analogue of discrete Fourier transform",
    },
    "phase-estimation": {
        "name": "Quantum Phase Estimation",
        "create": lambda: create_phase_estimation_circuit(n_counting_qubits=3),
        "palette": "phase_estimation",
        "description": "Estimates eigenvalues of unitary operators",
    },
    "vqe": {
        "name": "Variational Quantum Eigensolver",
        "create": lambda: create_vqe_circuit(n_qubits=2),
        "palette": "vqe",
        "description": "Hybrid quantum-classical ground state finder",
    },
    "quantum-walk": {
        "name": "Quantum Random Walk",
        "create": lambda: create_quantum_walk_circuit(steps=3),
        "palette": "quantum_walk",
        "description": "Quantum analogue of classical random walk with ballistic spreading",
    },
    "error-correction": {
        "name": "Quantum Error Correction (3-qubit)",
        "create": lambda: create_error_correction_circuit(),
        "palette": "error_correction",
        "description": "Bit-flip error correction using syndrome measurements",
    },
    "deutsch-jozsa": {
        "name": "Deutsch-Jozsa Algorithm",
        "create": lambda: create_deutsch_jozsa_circuit(n_qubits=3),
        "palette": "deutsch_jozsa",
        "description": "Determines if a function is constant or balanced in one query",
    },
    "bernstein-vazirani": {
        "name": "Bernstein-Vazirani Algorithm",
        "create": lambda: create_bernstein_vazirani_circuit(secret="101"),
        "palette": "bernstein_vazirani",
        "description": "Finds hidden binary string in a single query (secret: 101)",
    },
    "simon": {
        "name": "Simon's Algorithm",
        "create": lambda: create_simon_circuit(secret="110"),
        "palette": "simon",
        "description": "Finds hidden period with exponential speedup (secret: 110)",
    },
}


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="quantum-app",
        description=(
            "🌌 Advanced Quantum Computing Application v{}\n"
            "A comprehensive toolkit featuring 11 quantum algorithms."
        ).format(__version__),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python main.py                          Run all algorithms\n"
            "  python main.py -a grover                Run Grover's search\n"
            "  python main.py -a grover -a qft         Run multiple algorithms\n"
            "  python main.py --save-images             Save histogram images\n"
            "  python main.py --shots 4096 --no-plot    High-shot headless run\n"
            "  python main.py --ghz 5                  Run 5-qubit GHZ state\n"
            "  python main.py --list                   List all algorithms\n"
        ),
    )

    parser.add_argument(
        "--version", action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "-a", "--algorithm", action="append", dest="algorithms",
        choices=list(ALGORITHMS.keys()),
        help="Run specific algorithm(s). Can be specified multiple times.",
    )
    parser.add_argument(
        "--all", action="store_true", default=False,
        help="Run all algorithms (default if no -a specified).",
    )
    parser.add_argument(
        "--shots", type=int, default=2048,
        help="Number of measurement shots per algorithm (default: 2048).",
    )
    parser.add_argument(
        "--save-images", action="store_true", default=False,
        help="Save histogram images to the images/ directory.",
    )
    parser.add_argument(
        "--images-dir", type=str, default="images",
        help="Directory to save images (default: images/).",
    )
    parser.add_argument(
        "--no-plot", action="store_true", default=False,
        help="Disable interactive plot display (useful for headless/CI).",
    )
    parser.add_argument(
        "--ghz", type=int, metavar="N",
        help="Run a custom GHZ state with N qubits.",
    )
    parser.add_argument(
        "--list", action="store_true", default=False,
        help="List all available algorithms and exit.",
    )

    return parser


def list_algorithms() -> None:
    print("═" * 80)
    print("🌌  Available Quantum Algorithms")
    print("═" * 80)
    print(f"  {'Key':<22} {'Algorithm':<35} {'Description'}")
    print(f"  {'─' * 22} {'─' * 35} {'─' * 40}")

    for key, info in ALGORITHMS.items():
        print(f"  {key:<22} {info['name']:<35} {info['description']}")

    print("═" * 80)
    print(f"  Total: {len(ALGORITHMS)} algorithms")
    print("═" * 80)


def run_single_algorithm(app: AdvancedQuantumApp, key: str,
                          shots: int, save_images: bool,
                          images_dir: str, show_plots: bool) -> None:
    info = ALGORITHMS[key]
    name = info["name"]
    palette = info["palette"]
    circuit = info["create"]()

    print(format_header(name))
    print(format_circuit_info(circuit, name))
    print()

    print("  Circuit Diagram:")
    diagram_lines = str(circuit.draw(output='text')).split('\n')
    for line in diagram_lines:
        print(f"    {line}")

    counts = app.execute_circuit(circuit, shots=shots, name=name)

    print(f"\n  📊 Measurement Results (top 5):")
    print(format_counts(counts, shots))

    exec_time = app.results_history[-1]["execution_time"]
    print(f"\n  ⏱  Execution time: {exec_time:.4f}s")

    save_path = None
    if save_images:
        save_path = f"{images_dir}/{palette}_histogram.png"

    app.visualize(
        counts, title=name, save_path=save_path,
        palette_key=palette, show=show_plots,
    )

    if save_path:
        print(f"  💾 Saved: {save_path}")


def main(argv: Optional[list] = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)

    if args.list:
        list_algorithms()
        return 0

    app = AdvancedQuantumApp()
    show_plots = not args.no_plot

    if args.algorithms:
        algo_keys = args.algorithms
    elif args.all or (not args.ghz):
        algo_keys = list(ALGORITHMS.keys())
    else:
        algo_keys = []

    if algo_keys:
        print("═" * 80)
        print(f"🌌  ADVANCED QUANTUM COMPUTING APPLICATION v{__version__}")
        print("═" * 80)
        print(f"   Simulator: AerSimulator")
        print(f"   Shots per algorithm: {args.shots:,}")
        print(f"   Algorithms to run: {len(algo_keys)}")
        if args.save_images:
            print(f"   Save images to: {args.images_dir}/")
        print("═" * 80)

        for key in algo_keys:
            run_single_algorithm(
                app, key, args.shots, args.save_images,
                args.images_dir, show_plots,
            )

        from quantum_app.utils import print_summary
        print_summary(app.results_history)

    if args.ghz:
        app.run_custom_ghz(
            n_qubits=args.ghz, shots=args.shots,
            save_images=args.save_images,
            images_dir=args.images_dir,
            show_plots=show_plots,
        )

    print("\n✅ Quantum Computing Demo Complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
