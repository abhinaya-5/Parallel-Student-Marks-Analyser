import pandas as pd
import time


def serial_analysis(df):

    start_time = time.perf_counter()

    results = []

    for _, student in df.iterrows():

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

    end_time = time.perf_counter()

    execution_time = end_time - start_time

    result_df = pd.DataFrame(results)

    return result_df, execution_time