import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import plotly.graph_objects as go

def plot_measures(
    df,
    filename: str,
    column_to_plot: str,
    y_label: str,
    as_bar: bool = False,
    category: str = None,
):
    """Produce time series plot from measures table.  One line is plotted for each sub
    category within the category column. Saves output in 'output' dir as jpeg file.
    Args:
        df: A measure table
        column_to_plot: Column name for y-axis values
        y_label: Label to use for y-axis
        as_bar: Boolean indicating if bar chart should be plotted instead of line chart. Only valid if no categories.
        category: Name of column indicating different categories
    """
    plt.figure(figsize=(15, 8))
    if category:
        df[category] = df[category].fillna("Missing")
        for unique_category in sorted(df[category].unique()):

            # subset on category column and sort by date
            df_subset = df[df[category] == unique_category].sort_values("date")

            plt.plot(df_subset["date"], df_subset[column_to_plot])
    else:
        if as_bar:
            df.plot.bar("date", column_to_plot, legend=False)
        else:
            plt.plot(df["date"], df[column_to_plot])

    x_labels = sorted(df["date"].unique())

    plt.ylabel(y_label)
    plt.xlabel("Date")
    plt.xticks(x_labels, rotation="vertical")
    plt.ylim(
        bottom=0,
        top=100
        if df[column_to_plot].isnull().values.all()
        else df[column_to_plot].max() * 1.05,
    )

    if category:
        plt.legend(
            sorted(df[category].unique()), bbox_to_anchor=(1.04, 1), loc="upper left"
        )

    plt.tight_layout()

    plt.savefig(f"output/{filename}.jpeg")
    plt.close()


def plot_measures_interactive(df, filename, column_to_plot, category=False, y_label='Rate per 1000'):
    fig = go.Figure()

    if category:
        for unique_category in df[category].unique():

            df_subset = df[df[category] == unique_category]
            fig.add_trace(go.Scatter(
                x=df_subset['date'], y=df_subset[column_to_plot], name=unique_category))

    else:
        fig.add_trace(go.Scatter(
            x=df['date'], y=df[column_to_plot]))

    # Set title
    # fig.update_layout(
    #     title_text=title,
    #     hovermode='x',
    #     title_x=0.5,


    # )

    fig.update_yaxes(title=y_label)
    fig.update_xaxes(title="Date")

    # Add range slider
    fig.update_layout(
        xaxis=go.layout.XAxis(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),

                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    # save plotly plot
    fig.write_html(f"output/{filename}.html")
   

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--breakdowns", help="codelist to use")
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    if args.breakdowns != "":

        breakdowns = args.breakdowns.split(",")
    else:
        breakdowns = []
    
  
    df = pd.read_csv(f"output/report/joined/measure_total_rate.csv", parse_dates=["date"])
    
  

    plot_measures(
    df,
        filename=f"report/plot_measures",
        column_to_plot="value",
        y_label="Rate per 1000",
        as_bar=False,
        category=None,
    )

    plot_measures_interactive(df, filename=f"report/plot_measures", column_to_plot="event_measure", category=None, y_label="Count")
  
    for breakdown in breakdowns:
        df = pd.read_csv(
            f"output/report/joined/measure_{breakdown}_rate.csv", parse_dates=["date"]
        )

       

    
        plot_measures(
            df,
            filename=f"report/plot_measures_{breakdown}",
            column_to_plot="value",
            y_label="Rate per 1000",
            as_bar=False,
            category=breakdown,
        )
    
if __name__ == "__main__":
    main()