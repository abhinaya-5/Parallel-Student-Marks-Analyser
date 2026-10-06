import matplotlib.pyplot as plt
import os
import time

from modules.parallel_analysis import parallel_analysis


def calculate_performance(serial_time, parallel_time, number_of_processes):

    speedup = serial_time / parallel_time

    efficiency = (speedup / number_of_processes) * 100

    return speedup, efficiency


def benchmark_parallel(df, process_counts):

    results = []

    for process_count in process_counts:

        print(
            f"\nTesting with {process_count} processes..."
        )

        start_time = time.perf_counter()

        _, parallel_time = parallel_analysis(
            df,
            number_of_processes=process_count
        )

        end_time = time.perf_counter()

        measured_time = end_time - start_time

        results.append({
            "processes": process_count,
            "time": measured_time
        })

        print(
            f"Execution time: {measured_time:.4f} seconds"
        )

    return results


def create_performance_graph(
    serial_time,
    benchmark_results
):

    process_labels = ["Serial"]
    execution_times = [serial_time]

    for result in benchmark_results:

        process_labels.append(
            f"{result['processes']} Processes"
        )

        execution_times.append(
            result["time"]
        )

    plt.figure(figsize=(10, 6))

    plt.bar(
        process_labels,
        execution_times
    )

    plt.xlabel("Processing Method")

    plt.ylabel("Execution Time (seconds)")

    plt.title(
        "Serial vs Parallel Execution Time"
    )

    plt.xticks(rotation=20)

    plt.tight_layout()

    os.makedirs("results", exist_ok=True)

    plt.savefig(
        "results/performance_comparison.png"
    )

    plt.show()

    print(
        "\nPerformance graph saved successfully!"
    )