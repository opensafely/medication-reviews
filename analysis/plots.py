import pandas as pd
from utilities import plot_measures

df = pd.read_csv("output/joined/measure_smr_population_rate.csv", parse_dates=["date"])

plot_measures(df, filename="smr_population_rate", title="", column_to_plot="value", y_label="Rate")
