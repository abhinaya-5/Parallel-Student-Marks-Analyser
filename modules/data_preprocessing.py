import pandas as pd


def load_student_data():
    file_path = "dataset/student_marks.csv"

    df = pd.read_csv(file_path)

    print("Dataset loaded successfully!")
    print("Number of students:", len(df))
    print("Number of columns:", len(df.columns))

    return df


def prepare_data(df):
    marks_columns = [
        "Maths",
        "DBMS",
        "OS",
        "Java"
    ]

    for column in marks_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(subset=marks_columns)

    return df