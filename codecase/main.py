
import pandas as pd

try:
    df = pd.read_csv("Codebase/marks.csv", skipinitialspace=True)

    print("Student Data:")
    print(df)
    required_columns = ["RollNo", "Name", "Maths", "Physics", "Programming"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing column: {column}")
    mark_columns = ["Maths", "Physics", "Programming"]

    for column in mark_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    valid_rows = (
        df["RollNo"].notna()
        & df["Name"].notna()
        & df[mark_columns].notna().all(axis=1)
        & df[mark_columns].ge(0).all(axis=1)
        & df[mark_columns].le(100).all(axis=1)
    )

    invalid_rows = df[~valid_rows]

    if not invalid_rows.empty:
        for _, row in invalid_rows.iterrows():
            print(f"warning: Row for roll {int(row['RollNo'])} skipped - marks must be between 0 and 100.")

    df = df[valid_rows].copy()
    df["Total"] = df[mark_columns].sum(axis=1)
    df["percentage"] = ((df["Total"] / 300) * 100).round(2)

    def calculate_grade(percentage):
        if percentage >= 90:
            return "A+"
        elif percentage >= 80:
            return "A"
        elif percentage >= 70:
            return "B"
        elif percentage >= 60:
            return "C"
        elif percentage >= 50:
            return "D"
        elif percentage >= 40:
            return "E"
        else:
            return "F"

    df["Grade"] = df["percentage"].apply(calculate_grade)
    def calculate_result(row):
        if (
            row["Maths"] < 40
            or row["Physics"] < 40
            or row["Programming"] < 40
        ):
            return "FAIL"
        else:
            return "PASS"

    df["Result"] = df.apply(calculate_result, axis=1)

    print("\nFinal Marksheet:")
    print(df)

    df.to_csv("Codebase/final_marksheet.csv", index=False, float_format="%.2f")
    print("\nMarksheet saved successfully!")

        
    search_roll = int(input("\nEnter Roll Number: "))

    student = df[df["RollNo"] == search_roll]

    if not student.empty:
        print("\nStudent Marksheet:")
        print(student)
    else:
        print("Student not found!")

except FileNotFoundError:
    print("Error: marks.csv file not found.")

except ValueError as error:
    print("Error:", error)
    
