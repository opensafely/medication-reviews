import nbformat as nbf
from pathlib import Path

# if output/report dir doesn't exist, create it
if not Path("output/report").exists():
    Path("output/report").mkdir(parents=True, exist_ok=True)


nb = nbf.v4.new_notebook()
demographics = ["sex", "ethnicity", "region", "imd", "age_band"]
measure_name="DMARDS"
imports = """\
import pandas as pd
import json
from IPython.display import Image, display, HTML
from IPython.display import Markdown as md

title = "OpenSAFELY Interactive: Prescribing of DMARDs and Medication Reviews"
codelist_1_description = "medication review"
codelist_2_description = "DMARD prescription"
codelist_1_link="https://www.opencodelists.org/codelist/nhsd-primary-care-domain-refsets/medrvw_cod/20200812/"
codelist_2_link="https://www.opencodelists.org/codelist/opensafely/dmards/2020-06-23/"
logic = "AND"
logic_description = "up to 12 months before a recorded medication review"
demographics = ["sex", "ethnicity", "region", "imd", "age_band"]
demographics_map = {
    "sex": "Sex",
    "ethnicity": "Ethnicity",
    "region": "Region",
    "imd": "Index of Multiple Deprivation",
    "age_band": "Age band",
}
measure_name="medication_review"
population="all registered adults"

%matplotlib inline
"""

header = """\
demographics_string = ", ".join(demographics)
demographics_string = demographics_string.replace("age_band", "age band")
display(
md(f"# {title}"),
md(f"The below analysis shows the rate of coding of **{codelist_1_description} {logic} {codelist_2_description}** in **{population}**. This analysis uses data available in OpenSAFELY-TPP (~40% of England) between 2019-01-01 and 2022-11-01."),
md(f"A {codelist_1_description} is defined each month as all patients with a code recorded from [this codelist]({codelist_1_link}). A {codelist_2_description} is defined each month as anyone with a code recorded from [this codelist]({codelist_2_link}) that occurs **{logic_description}**"),
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
md(f"Practice level variation in this measure is shown below as a decile chart. Each month, practices are ranked by their rate of coding of **{codelist_1_description} {logic} {codelist_2_description}**, from which deciles of activity are calculated."),
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
    nbf.v4.new_code_cell(imports),
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