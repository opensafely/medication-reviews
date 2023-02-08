import argparse
import nbformat as nbf
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--codelist-1-description",
        type=str,
        help="Description of codelist 1",
        required=True,
    )
    parser.add_argument(
        "--codelist-2-description",
        type=str,
        help="Description of codelist 2",
        required=True,
    )
    parser.add_argument(
        "--codelist-1-link",
        type=str,
        help="Link to codelist 1",
        required=True,
    )
    parser.add_argument(
        "--codelist-2-link",
        type=str,
        help="Link to codelist 2",
        required=True,
    )
    parser.add_argument(
        "--report-title",
        type=str,
        help="Title of report",
        required=True,
    )
    parser.add_argument(
        "--measure-name",
        type=str,
        help="Name of measure",
        required=True,
    )
    parser.add_argument(
        "--population",
        type=str,
        help="Name of population",
        required=True,
    )
    parser.add_argument(
        "--measure-description",
        type=str,
        help="Description of measure",
        required=True,
    )
    # demographics argument - allow multiple and append
    parser.add_argument(
        "--demographics",
        action="append",
        type=str,
        help="Demographics to include in report",
        required=True,
    )

    return parser.parse_args()


def main():
    args = parse_args()
    codelist_1_description = args.codelist_1_description
    codelist_1_link = args.codelist_1_link
    codelist_2_description = args.codelist_2_description
    codelist_2_link = args.codelist_2_link
    title = args.report_title
    demographics = args.demographics
    demographics_string = ", ".join(demographics)
    population = args.population
    measure_description = args.measure_description
 
    if not Path("output/report").exists():
        Path("output/report").mkdir(parents=True, exist_ok=True)

    nb = nbf.v4.new_notebook()
    
    
    imports = """
    import pandas as pd
    import json
    from IPython.display import Image, display, HTML
    from IPython.display import Markdown as md

    
    title = '{title}'
    demographics = {demographics}
    codelist_1_description = '{codelist_1_description}'
    codelist_2_description = '{codelist_2_description}'
    codelist_1_link = '{codelist_1_link}'
    codelist_2_link = '{codelist_2_link}'
 
    population = '{population}'
    measure_description = '{measure_description}'
    demographics_string = '{demographics_string}'

    demographics_map = {{
        'sex': 'Sex',
        'ethnicity': 'Ethnicity',
        'region': 'Region',
        'imd': 'Index of Multiple Deprivation',
        'age_band': 'Age band',
    }}


    %matplotlib inline
    """

    header = """\
    
    demographics_string = demographics_string.replace("age_band", "age band")
    display(
    md(f"# {title}"),
    md(f"The below analysis shows the rate of coding of **{codelist_1_description} AND {codelist_2_description}** in **{population}**. This analysis uses data available in OpenSAFELY-TPP (~40% of England) between 2019-01-01 and 2022-11-01."),
    md(f"A {codelist_1_description} is defined each month as all patients with a code recorded from [this codelist]({codelist_1_link}). A {codelist_2_description} is defined each month as anyone with a code recorded from [this codelist]({codelist_2_link}) that occurs **{measure_description}**"),
    md(f"A practice level decile chart of this measure is provided, as well as a plot of the populatioin level rate and a breakdown of this measure by **{demographics_string}**."),
    md(f"The top 5 codes for both codelists across the entire study period is also shown."),
    )

    """

    events_summary = """\
    display(
    md(f"## Measure summary"),
    )
    display(Image(filename=f'../../analysis/report/measure_diagram.png'))
    with open(f'event_counts.json') as f:
        events_summary = json.load(f)
    events_summary = pd.DataFrame(events_summary, index=[0])
    events_summary = events_summary.rename(columns={"total_events": "Total events", "total_patients": "Total patients", "events_in_latest_period": "Events in latest period", "total_practices": "Total practices"})
    num_practices = events_summary["Total practices"][0]
    events_summary = events_summary.drop(columns=["Total practices"])
    display(HTML(events_summary.to_html(index=False)))

    """

    decile_chart = """\
    display(
    md(f"## Practice level variation"),
    md(f"Practice level variation in this measure is shown below as a decile chart. Each month, practices are ranked by their rate of coding of **{codelist_1_description} AND {codelist_2_description}**, from which deciles of activity are calculated."),
    md(f"The decile chart below is based on data from {num_practices} practices."),
    )
    display(Image(filename=f'joined/deciles_chart_practice_rate_deciles.png'))
    """


    top_5_1 = """\
    display(
    md(f"## Most common codes"),
    md(f"#### {codelist_1_description.capitalize()}"),

    )
    top_5_1_codes = pd.read_csv(f'joined/top_5_code_table_1.csv')
    display(HTML(top_5_1_codes.to_html(index=False)))
    """

    top_5_2 = """\
    display(
    md(f"#### {codelist_2_description.capitalize()}"),
    )
    top_5_2_codes = pd.read_csv(f'joined/top_5_code_table_2.csv')
    display(HTML(top_5_2_codes.to_html(index=False)))
    """

    population_plot = """\
    display(
    md(f"## Population level rate"),
    )
    display(Image(filename=f'plot_measures.jpeg'))
    """

    nb["cells"] = [
        nbf.v4.new_code_cell(
            imports.format(demographics=demographics, 
            demographics_string=demographics_string,
            title=title,    
                codelist_1_description=codelist_1_description,
                codelist_2_description=codelist_2_description,
                codelist_1_link=codelist_1_link,
                codelist_2_link=codelist_2_link,
                population=population,  
                measure_description=measure_description,
            )),
        nbf.v4.new_code_cell(header),
        nbf.v4.new_code_cell(events_summary),
        nbf.v4.new_code_cell(decile_chart),
        nbf.v4.new_code_cell(top_5_1),
        nbf.v4.new_code_cell(top_5_2),
        nbf.v4.new_code_cell(population_plot),
    ]

    counter = """\
    i=0
    """

    nb["cells"].append(nbf.v4.new_code_cell(counter))

    for d in range(len(demographics)):
        cell_counts = """\
        display(
        md(f"## Breakdown by {demographics_map[demographics[i]]}"),
        )
    
        """
        nb["cells"].append(nbf.v4.new_code_cell(cell_counts))

        cell_plot = """\
        display(Image(filename=f'plot_measures_{demographics[i]}.jpeg'))
        i+=1
        """
        nb["cells"].append(nbf.v4.new_code_cell(cell_plot))


    with open("output/report/report.ipynb", "w") as f:
        nbf.write(nb, f)
if __name__ == "__main__":
    main()

