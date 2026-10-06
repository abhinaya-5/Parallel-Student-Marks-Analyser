import time
import math
import pandas as pd
import matplotlib.pyplot as plt
from multiprocessing import Pool


# -----------------------------------------
# CPU-INTENSIVE CALCULATION
# -----------------------------------------

def heavy_calculation(value):

    result = 0.0

    for i in range(20000):

        x = value + i

        result += (
            math.sqrt(x + 1)
            * math.sin(x)
            * math.cos(x)
        )

    return result


# -----------------------------------------
# SERIAL PROCESSING
# -----------------------------------------

def serial_processing(values):

    start_time = time.perf_counter()

    results = []

    for value in values:

        results.append(
            heavy_calculation(value)
        )

    end_time = time.perf_counter()

    return end_time - start_time


# -----------------------------------------
# PARALLEL WORKER
# -----------------------------------------

def parallel_worker(value):

    return heavy_calculation(value)


# -----------------------------------------
# PARALLEL PROCESSING
# -----------------------------------------

def parallel_processing(values, number_of_processes):

    start_time = time.perf_counter()

    with Pool(
        processes=number_of_processes
    ) as pool:

        results = pool.map(
            parallel_worker,
            values
        )

    end_time = time.perf_counter()

    return end_time - start_time


# -----------------------------------------
# MAIN PROGRAM
# -----------------------------------------

if __name__ == "__main__":

    print("\n======================================")
    print(" CPU-INTENSIVE PARALLEL TEST")
    print("======================================")

    # Load student dataset

    df = pd.read_csv(
        "dataset/student_marks.csv"
    )

    # Use Total_Marks as input

    values = df["Total_Marks"].tolist()

    print(
        "\nNumber of students:",
        len(values)
    )

    # -------------------------------------
    # SERIAL TEST
    # -------------------------------------

    print("\nRunning serial processing...")

    serial_time = serial_processing(
        values
    )

    print(
        "Serial execution time:",
        round(serial_time, 4),
        "seconds"
    )

    # -------------------------------------
    # PARALLEL TESTS
    # -------------------------------------

    process_counts = [2, 4, 8]

    results = []

    for process_count in process_counts:

        print(
            f"\nRunning with "
            f"{process_count} processes..."
        )

        parallel_time = parallel_processing(
            values,
            process_count
        )

        speedup = (
            serial_time / parallel_time
        )

        efficiency = (
            speedup / process_count
        ) * 100

        results.append({
            "Processes": process_count,
            "Parallel Time": parallel_time,
            "Speedup": speedup,
            "Efficiency": efficiency
        })

        print(
            "Parallel execution time:",
            round(parallel_time, 4),
            "seconds"
        )

        print(
            "Speedup:",
            round(speedup, 2),
            "x"
        )

        print(
            "Efficiency:",
            round(efficiency, 2),
            "%"
        )

    # -------------------------------------
    # RESULTS TABLE
    # -------------------------------------

    results_df = pd.DataFrame(
        results
    )

    print("\n======================================")
    print(" FINAL PERFORMANCE RESULTS")
    print("======================================")

    print(
        results_df.to_string(
            index=False
        )
    )

    # -------------------------------------
    # GRAPH 1
    # -------------------------------------

    plt.figure(figsize=(9, 6))

    plt.bar(
        results_df["Processes"].astype(str),
        results_df["Parallel Time"]
    )

    plt.xlabel(
        "Number of Processes"
    )

    plt.ylabel(
        "Execution Time (seconds)"
    )

    plt.title(
        "Parallel Execution Time"
    )

    plt.tight_layout()

    plt.savefig(
        "results/cpu_parallel_execution_time.png"
    )

    plt.close()

    # -------------------------------------
    # GRAPH 2
    # -------------------------------------

    plt.figure(figsize=(9, 6))

    plt.plot(
        results_df["Processes"],
        results_df["Speedup"],
        marker="o"
    )

    plt.xlabel(
        "Number of Processes"
    )

    plt.ylabel(
        "Speedup"
    )

    plt.title(
        "Parallel Processing Speedup"
    )

    plt.xticks(
        process_counts
    )

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        "results/cpu_speedup.png"
    )

    plt.close()

    print(
        "\nGraphs saved successfully!"
    )