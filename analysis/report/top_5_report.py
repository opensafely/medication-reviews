import pandas as pd
import numpy as np
import argparse

def write_csv(df, path, **kwargs):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, **kwargs)

def group_low_values(df, count_column, code_column, threshold):
    """Suppresses low values and groups suppressed values into
    a new row "Other".

    Args:
        df: A measure table of counts by code.
        count_column: The name of the count column in the measure table.
        code_column: The name of the code column in the codelist table.
        threshold: Redaction threshold to use
    Returns:
        A table with redacted counts
    """

    # get sum of any values <= threshold
    suppressed_count = df.loc[df[count_column] <= threshold, count_column].sum()
    suppressed_df = df.loc[df[count_column] > threshold, count_column]

    # if suppressed values >0 ensure total suppressed count > threshold.
    # Also suppress if all values 0
    if (suppressed_count > 0) | (
        (suppressed_count == 0) & (len(suppressed_df) != len(df))
    ):

        # redact counts <= threshold
        df.loc[df[count_column] <= threshold, count_column] = np.nan

        # If all values 0, suppress them
        if suppressed_count == 0:
            df.loc[df[count_column] == 0, :] = np.nan

        else:
            # if suppressed count <= threshold redact further values
            while suppressed_count <= threshold:
                suppressed_count += df[count_column].min()
                df.loc[df[count_column].idxmin(), :] = np.nan

        # drop all rows where count column is null
        df = df.loc[df[count_column].notnull(), :]

        # add suppressed count as "Other" row (if > threshold)
        if suppressed_count > threshold:
            suppressed_count = {code_column: "Other", count_column: suppressed_count}
            df = pd.concat([df, pd.DataFrame([suppressed_count])], ignore_index=True)

    return df

def round_values(x, base=5):
    rounded = x
    if isinstance(x, (int, float)):
        if np.isnan(x):
            rounded = np.nan
        else:
            rounded = int(base * round(x / base))
    return rounded

def create_top_5_code_table(
    df, code_df, code_column, term_column, low_count_threshold, rounding_base, nrows=5
):
    """Creates a table of the top 5 codes recorded with the number of events and % makeup of each code.
    Args:
        df: A measure table.
        code_df: A codelist table.
        code_column: The name of the code column in the codelist table.
        term_column: The name of the term column in the codelist table.
        measure: The measure ID.
        low_count_threshold: Value to use as threshold for disclosure control.
        rounding_base: Base to round to.
        nrows: The number of rows to display.
    Returns:
        A table of the top `nrows` codes.
    """

    # cast both code columns to str
    df[code_column] = df[code_column].astype(int).astype(str)
    code_df[code_column] = code_df[code_column].astype(int).astype(str)

    

    # sum event counts over patients
    event_counts = df.sort_values(ascending=False, by="num")

    event_counts = group_low_values(
        event_counts, "num", code_column, low_count_threshold
    )

    # round

    event_counts["num"] = event_counts["num"].apply(
        lambda x: round_values(x, rounding_base)
    )

    # calculate % makeup of each code
    total_events = event_counts["num"].sum()
    event_counts["Proportion of codes (%)"] = round(
        (event_counts["num"] / total_events) * 100, 2
    )

  
    # Gets the human-friendly description of the code for the given row
    # e.g. "Systolic blood pressure".
    code_df[code_column] = code_df[code_column].astype(str)
    code_df = code_df.set_index(code_column).rename(
        columns={term_column: "Description"}
    )

    event_counts = event_counts.set_index(code_column).join(code_df).reset_index()

    # set description of "Other column" to something readable
    event_counts.loc[event_counts[code_column] == "Other", "Description"] = "-"

    # Rename the code column to something consistent
    event_counts.rename(columns={code_column: "Code"}, inplace=True)

    # drop events column
    event_counts = event_counts.loc[
        :, ["Code", "Description", "Proportion of codes (%)"]
    ]
    # return top n rows
    return event_counts.head(5)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--codelist-1-path",
        type=str,
        help="Path to codelist for event 1",
    )
    parser.add_argument(
        "--codelist-2-path",
        type=str,
        help="Path to codelist for event 2",
    )
    args = parser.parse_args()
    return args

    
def main():
    args = parse_args()
    codelist_1_path = args.codelist_1_path
    codelist_2_path = args.codelist_2_path

    code_df = pd.read_csv(f"output/report/joined/measure_event_1_code_rate.csv")
    codelist = pd.read_csv(f"{codelist_1_path}")
    
    events_per_code = code_df.groupby("event_1_code")[["event_measure"]].sum().reset_index()
    events_per_code.columns = ["code", "num"]

   
    top_5_code_table = create_top_5_code_table(
        df=events_per_code,
        code_df=codelist,
        code_column="code",
        term_column="term",
        low_count_threshold=7,
        rounding_base=7,
    )
    top_5_code_table.to_csv(f"output/report/joined/top_5_code_table_1.csv", index=False)


    code_df_2 = pd.read_csv(f"output/report/joined/measure_event_2_code_rate.csv")

    

    codelist_2 = pd.read_csv(f"{codelist_2_path}")
  
    # map snomed_id to vpid using codelist_2
    code_df_2 = code_df_2.merge(codelist_2, left_on="event_2_code",right_on="snomed_id", how="left")
   

    # set vpid to index
    code_df_2 = code_df_2.set_index("vpid")

    # group code_df_2 by vpid
    code_df_2 = code_df_2.groupby("vpid")[["event_measure", "population"]].sum().reset_index()
    
    # drop all columns except event_2_code and event_measure
    code_df_2 = code_df_2[["vpid", "event_measure"]]
    # events_per_code = code_df_2.groupby("event_2_code")[["event_measure"]].sum().reset_index()
    code_df_2.columns = ["code", "num"]


    # group codelist_2 by vpid
    codelist_2 = codelist_2.groupby("vpid")[["bnf_name"]].first().reset_index()


    codelist_2 = codelist_2.rename(columns={"vpid": "code"})
     

    top_5_code_table = create_top_5_code_table(
        df=code_df_2,
        code_df=codelist_2,
        code_column="code",
        term_column="bnf_name",
        low_count_threshold=7,
        rounding_base=7,
    )
   
    top_5_code_table.to_csv(f"output/report/joined/top_5_code_table_2.csv", index=False)


if __name__ == "__main__":
    main()
