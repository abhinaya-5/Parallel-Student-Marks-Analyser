from modules.data_preprocessing import load_student_data, prepare_data
from modules.serial_analysis import serial_analysis
from modules.parallel_analysis import parallel_analysis
from modules.performance import (
    calculate_performance,
    benchmark_parallel,
    create_performance_graph
)


if __name__ == "__main__":

    # Load dataset
    df = load_student_data()

    # Prepare dataset
    df = prepare_data(df)

    print("\nData preparation completed successfully!")

    # -----------------------------------
    # SERIAL PROCESSING
    # -----------------------------------

    serial_result, serial_time = serial_analysis(df)

    print("\nSerial analysis completed successfully!")

    print(
        "Serial execution time:",
        serial_time,
        "seconds"
    )

    # -----------------------------------
    # PARALLEL PROCESSING
    # -----------------------------------

    number_of_processes = 4

    parallel_result, parallel_time = parallel_analysis(
        df,
        number_of_processes=number_of_processes
    )

    print("\nParallel analysis completed successfully!")

    print(
        "Parallel execution time:",
        parallel_time,
        "seconds"
    )

    # -----------------------------------
    # SPEEDUP AND EFFICIENCY
    # -----------------------------------

    speedup, efficiency = calculate_performance(
        serial_time,
        parallel_time,
        number_of_processes
    )

    print("\n========== PERFORMANCE ==========")

    print(
        "Number of processes:",
        number_of_processes
    )

    print(
        "Serial time:",
        serial_time,
        "seconds"
    )

    print(
        "Parallel time:",
        parallel_time,
        "seconds"
    )

    print(
        "Speedup:",
        round(speedup, 4),
        "x"
    )

    print(
        "Efficiency:",
        round(efficiency, 2),
        "%"
    )

    print("=================================")

    # -----------------------------------
    # TEST DIFFERENT PROCESS COUNTS
    # -----------------------------------

    process_counts = [2, 4, 8]

    benchmark_results = benchmark_parallel(
        df,
        process_counts
    )

    # -----------------------------------
    # DISPLAY BENCHMARK RESULTS
    # -----------------------------------

    print("\n====== PROCESS COMPARISON ======")

    for result in benchmark_results:

        print(
            result["processes"],
            "processes :",
            round(result["time"], 4),
            "seconds"
        )

    print("===============================")

    # -----------------------------------
    # CREATE GRAPH
    # -----------------------------------

    create_performance_graph(
        serial_time,
        benchmark_results
    )