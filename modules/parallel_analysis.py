import pandas as pd
import time
from multiprocessing import Pool


def process_chunk(chunk):

    results = []

    for _, student in chunk.iterrows():

        total = (
            student["Maths"]
            + student["DBMS"]
            + student["OS"]
            + student["Java"]
        )

        average = total / 4

        if average >= 90:
            grade = "A+"
        elif average >= 80:
            grade = "A"
        elif average >= 70:
            grade = "B"
        elif average >= 60:
            grade = "C"
        elif average >= 50:
            grade = "D"
        else:
            grade = "F"

        status = "Pass" if average >= 50 else "Fail"

        results.append({
            "Student_ID": student["Student_ID"],
            "Name": student["Name"],
            "Total_Marks": total,
            "Average": average,
            "Grade": grade,
            "Status": status
        })

    return results


def parallel_analysis(df, number_of_processes=4):

    start_time = time.perf_counter()

    # Divide the DataFrame into equal-sized chunks
    chunk_size = len(df) // number_of_processes

    chunks = []

    for i in range(number_of_processes):

        start = i * chunk_size

        if i == number_of_processes - 1:
            end = len(df)
        else:
            end = (i + 1) * chunk_size

        chunks.append(df.iloc[start:end])

    # Process the chunks in parallel
    with Pool(processes=number_of_processes) as pool:

        results = pool.map(process_chunk, chunks)

    # Combine results from all processes
    combined_results = []

    for result in results:
        combined_results.extend(result)

    end_time = time.perf_counter()

    execution_time = end_time - start_time

    result_df = pd.DataFrame(combined_results)

    return result_df, execution_time