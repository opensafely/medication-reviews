import nbformat as nbf


nb = nbf.v4.new_notebook()
demographics = ["sex", "ethnicity", "region", "imd", "age_band"]
measure_name="DMARDS"
imports = """\
import pandas as pd
from IPython.display import Image, display, HTML
from IPython.display import Markdown as md

title = "OpenSAFELY Interactive: Prescribing of DMARDs and Medication Reviews"
codelist_1_description = "medication review"
codelist_2_description = "DMARD prescription"
codelist_1_link="https://www.opencodelists.org/codelist/nhsd-primary-care-domain-refsets/medrvw_cod/20200812/"
codelist_2_link="https://www.opencodelists.org/codelist/opensafely/dmards/2020-06-23/"
logic = "AND"
logic_description = "Logic"
demographics = "sex, ethnicity, region, imd and age band"
measure_name="medication_review"
population="all registered adults"

%matplotlib inline
"""

header = """\
display(
md(f"# {title}"),
md(f"The below analysis shows the rate of coding of **{codelist_1_description} {logic} {codelist_2_description}** in **{population}**. This analysis uses data available in OpenSAFELY-TPP (~40% of England) between 2019-01-01 and 2022-01-01."),
md(f"A {codelist_1_description} is defined each month as all patients with a code recorded from [this codelist]({codelist_1_link})). A {codelist_2_description} is defined each month as anyone with a code recorded from [this codelist]({codelist_2_link}) that occurs **{logic_description}**"),
md(f"A practice level decile chart of this measure is provided, as well as a plot of the populatioin level rate and a breakdown of this measure by **{demographics}**."),
md(f"The top 5 codes for both codelists across the entire study period is also shown."),
)
"""

decile_chart = """\
display(Image(filename=f'joined/deciles_chart_practice_rate.png'))
"""


top_5_1 = """\
top_5_1_codes = pd.read_csv(f'joined/top_5_code_table_1.csv')
display(HTML(top_5_1_codes.to_html(index=False)))
"""

top_5_2 = """\
top_5_2_codes = pd.read_csv(f'joined/top_5_code_table_2.csv')
display(HTML(top_5_2_codes.to_html(index=False)))
"""

population_plot = """\
display(Image(filename=f'joined/plot_measures.jpeg'))
"""


nb["cells"] = [
    nbf.v4.new_code_cell(imports),
    nbf.v4.new_code_cell(header),
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
    md(f"## Breakdown by {demographics[i]}"),
    )
   
    """
    nb["cells"].append(nbf.v4.new_code_cell(cell_counts))

    cell_plot = """\
    display(Image(filename=f'joined/plot_measures_{demographics[i]}.jpeg'))
    i+=1
    """
    nb["cells"].append(nbf.v4.new_code_cell(cell_plot))


nbf.write(nb, f"output/report/report.ipynb")