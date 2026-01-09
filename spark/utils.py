from pyspark.sql.functions import col


def remove_outliers_iqr(df, col_name, k=1.5):
    q1, q3 = df.approxQuantile(col_name, [0.25, 0.75], 0.01)
    iqr = q3 - q1
    lower = q1 - k * iqr
    upper = q3 + k * iqr
    print(f"{col_name} -> Q1={q1}, Q3={q3}, IQR={iqr}, bounds=({lower}, {upper})")
    return df.filter((col(col_name) >= lower) & (col(col_name) <= upper))
