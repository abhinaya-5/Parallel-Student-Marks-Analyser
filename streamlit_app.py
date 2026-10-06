import streamlit as st
import pandas as pd
import time
import math
from multiprocessing import Pool

from modules.data_preprocessing import load_student_data, prepare_data
from modules.serial_analysis import serial_analysis
from modules.parallel_analysis import parallel_analysis
from modules.performance import calculate_performance


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
# PARALLEL WORKER
# -----------------------------------------

def parallel_worker(value):

    return heavy_calculation(value)


# -----------------------------------------
# SERIAL CPU TEST
# -----------------------------------------

def cpu_serial_processing(values):

    start_time = time.perf_counter()

    for value in values:
        heavy_calculation(value)

    end_time = time.perf_counter()

    return end_time - start_time


# -----------------------------------------
# PARALLEL CPU TEST
# -----------------------------------------

def cpu_parallel_processing(
    values,
    number_of_processes
):

    start_time = time.perf_counter()

    with Pool(
        processes=number_of_processes
    ) as pool:

        pool.map(
            parallel_worker,
            values
        )

    end_time = time.perf_counter()

    return end_time - start_time
st.set_page_config(
    page_title="Parallel Student Marks Analyzer",
    page_icon="📊",
    layout="wide"
)


# -----------------------------------------
# TITLE
# -----------------------------------------

st.title("📊 Parallel Student Marks Analyzer")

st.write(
    "A Parallel Computing application for analyzing "
    "student performance using serial and parallel processing."
)


# -----------------------------------------
# LOAD DATASET
# -----------------------------------------

df = load_student_data()
df = prepare_data(df)


# -----------------------------------------
# CALCULATE BASIC STATISTICS
# -----------------------------------------

total_students = len(df)

subject_columns = [
    "Maths",
    "DBMS",
    "OS",
    "Java"
]

average_marks = (
    df[subject_columns]
    .mean()
    .mean()
)

total_average = df[subject_columns].sum(axis=1) / 4

pass_count = (total_average >= 50).sum()

pass_percentage = (
    pass_count / total_students
) * 100


# -----------------------------------------
# STUDENT STATISTICS
# -----------------------------------------

st.subheader("📈 Student Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Students",
        total_students
    )

with col2:
    st.metric(
        "Average Marks",
        f"{average_marks:.2f}"
    )

with col3:
    st.metric(
        "Pass Percentage",
        f"{pass_percentage:.2f}%"
    )


# -----------------------------------------
# SUBJECT-WISE AVERAGE
# -----------------------------------------

st.subheader("📚 Subject-wise Average Marks")

subject_average = df[subject_columns].mean()

st.bar_chart(subject_average)


# -----------------------------------------
# GRADE DISTRIBUTION
# -----------------------------------------

st.subheader("🏆 Grade Distribution")

def calculate_grade(average):

    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"


grades = total_average.apply(calculate_grade)

grade_counts = grades.value_counts()

grade_order = [
    "A+",
    "A",
    "B",
    "C",
    "D",
    "F"
]

grade_counts = grade_counts.reindex(
    grade_order,
    fill_value=0
)

st.bar_chart(grade_counts)


# -----------------------------------------
# DATASET PREVIEW
# -----------------------------------------

st.subheader("👀 Dataset Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)


# -----------------------------------------
# PARALLEL PROCESSING SETTINGS
# -----------------------------------------

st.subheader("⚙️ Parallel Processing Settings")

number_of_processes = st.slider(
    "Number of Processes",
    min_value=2,
    max_value=8,
    value=4,
    step=1
)


# -----------------------------------------
# RUN ANALYSIS BUTTON
# -----------------------------------------

if st.button("🚀 Run Parallel Analysis"):

    with st.spinner(
        "Processing student records..."
    ):

        # Serial processing
        serial_result, serial_time = serial_analysis(
            df
        )

        # Parallel processing
        parallel_result, parallel_time = parallel_analysis(
            df,
            number_of_processes=number_of_processes
        )

        # Performance calculation
        speedup, efficiency = calculate_performance(
            serial_time,
            parallel_time,
            number_of_processes
        )


    # -------------------------------------
    # PERFORMANCE RESULTS
    # -------------------------------------

    st.subheader("⚡ Performance Results")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Serial Time",
            f"{serial_time:.4f} sec"
        )

    with col2:
        st.metric(
            "Parallel Time",
            f"{parallel_time:.4f} sec"
        )

    with col3:
        st.metric(
            "Speedup",
            f"{speedup:.2f} ×"
        )

    with col4:
        st.metric(
            "Efficiency",
            f"{efficiency:.2f}%"
        )


    # -------------------------------------
    # RESULTS TABLE
    # -------------------------------------

    st.subheader("📋 Parallel Analysis Results")

    st.dataframe(
        parallel_result.head(20),
        use_container_width=True
    )


    # -------------------------------------
    # DOWNLOAD RESULTS
    # -------------------------------------

    csv_data = parallel_result.to_csv(
        index=False
    )

    st.download_button(
        label="⬇️ Download Analysis Results",
        data=csv_data,
        file_name="parallel_student_results.csv",
        mime="text/csv"
    )


    # -------------------------------------
    # SERIAL VS PARALLEL GRAPH
    # -------------------------------------

    st.subheader("📊 Serial vs Parallel Execution")

    comparison_data = pd.DataFrame({
        "Processing Method": [
            "Serial",
            "Parallel"
        ],
        "Execution Time": [
            serial_time,
            parallel_time
        ]
    })

    st.bar_chart(
        comparison_data.set_index(
            "Processing Method"
        )
    )


    # -------------------------------------
    # PROJECT INFORMATION
    # -------------------------------------

    st.info(
        f"Parallel processing divided the dataset into "
        f"{number_of_processes} chunks and processed them "
        "using multiple processes."
    )
    # -----------------------------------------
# CPU-INTENSIVE PERFORMANCE TEST
# -----------------------------------------

st.subheader("🔥 CPU-Intensive Parallel Performance")

st.write(
    "This experiment performs a computationally intensive "
    "calculation on the student dataset to demonstrate "
    "the performance benefit of parallel processing."
)

if st.button("⚡ Run CPU Performance Test"):

    values = df["Total_Marks"].tolist()

    with st.spinner(
        "Running CPU-intensive performance test..."
    ):

        cpu_serial_time = cpu_serial_processing(
            values
        )

        cpu_parallel_time = cpu_parallel_processing(
            values,
            number_of_processes
        )

    cpu_speedup = (
        cpu_serial_time / cpu_parallel_time
    )

    cpu_efficiency = (
        cpu_speedup / number_of_processes
    ) * 100

    st.subheader("📊 CPU Performance Results")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Serial Time",
            f"{cpu_serial_time:.2f} sec"
        )

    with col2:
        st.metric(
            "Parallel Time",
            f"{cpu_parallel_time:.2f} sec"
        )

    with col3:
        st.metric(
            "Speedup",
            f"{cpu_speedup:.2f} ×"
        )

    with col4:
        st.metric(
            "Efficiency",
            f"{cpu_efficiency:.2f}%"
        )

    # Execution time comparison

    comparison = pd.DataFrame({
        "Processing Method": [
            "Serial",
            f"Parallel ({number_of_processes} Processes)"
        ],
        "Execution Time": [
            cpu_serial_time,
            cpu_parallel_time
        ]
    })

    st.subheader(
        "⏱️ Serial vs Parallel Execution Time"
    )

    st.bar_chart(
        comparison.set_index(
            "Processing Method"
        )
    )

    # Speedup information

    st.subheader("🚀 Speedup")

    st.write(
        f"Parallel processing achieved "
        f"{cpu_speedup:.2f}× speedup using "
        f"{number_of_processes} processes."
    )

    if cpu_parallel_time < cpu_serial_time:

        st.success(
            "Parallel processing completed faster "
            "than serial processing."
        )

    else:

        st.warning(
            "Parallel processing was slower for "
            "this particular workload."
        )