import time
import logging
import functools
from typing import Dict, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-8s │ %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("quantum_app")


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.debug(f"{func.__name__} completed in {elapsed:.4f}s")
        return result, elapsed
    return wrapper


def format_counts(counts: Dict[str, int], shots: int, top_n: int = 5) -> str:
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    lines = []

    max_count = max(counts.values()) if counts else 1

    for state, count in sorted_counts:
        probability = (count / shots) * 100
        bar_length = int((count / max_count) * 30)
        bar = "█" * bar_length + "░" * (30 - bar_length)
        lines.append(f"  |{state}⟩  {bar}  {count:>5} ({probability:>6.2f}%)")

    return "\n".join(lines)


def format_header(title: str, width: int = 80, emoji: str = "🔬") -> str:
    border = "═" * width
    return f"\n{border}\n{emoji}  {title}\n{border}"


def format_circuit_info(circuit, name: str) -> str:
    lines = [
        f"  Circuit: {name}",
        f"  Qubits:  {circuit.num_qubits}",
        f"  Depth:   {circuit.depth()}",
        f"  Gates:   {sum(circuit.count_ops().values())}",
    ]

    ops = circuit.count_ops()
    if ops:
        gate_list = ", ".join(f"{gate}×{count}" for gate, count in sorted(ops.items()))
        lines.append(f"  Ops:     {gate_list}")

    return "\n".join(lines)


def calculate_fidelity(counts: Dict[str, int], expected_state: str,
                        shots: int) -> float:
    return counts.get(expected_state, 0) / shots


def print_summary(results_history: list) -> None:
    border = "═" * 80
    print(f"\n{border}")
    print("📊  EXECUTION SUMMARY")
    print(border)
    print(f"  {'Algorithm':<35} {'Shots':>7} {'Time (s)':>10} {'Top State':>12}")
    print(f"  {'─' * 35} {'─' * 7} {'─' * 10} {'─' * 12}")

    for entry in results_history:
        name = entry.get("name", entry.get("circuit", "Unknown"))[:35]
        shots = entry["shots"]
        exec_time = entry["execution_time"]
        top_state = max(entry["counts"], key=entry["counts"].get) if entry["counts"] else "N/A"
        print(f"  {name:<35} {shots:>7} {exec_time:>10.4f} |{top_state}⟩")

    print(border)
    total_time = sum(e["execution_time"] for e in results_history)
    print(f"  Total execution time: {total_time:.4f}s")
    print(f"  Algorithms executed:  {len(results_history)}")
    print(border)
