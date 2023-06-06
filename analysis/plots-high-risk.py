import pandas as pd
from utilities import *

if not (OUTPUT_DIR / "figures").exists():
    Path.mkdir(OUTPUT_DIR / "figures")

columnlookupdict={
    "addictive_meds": "addictivemeds_last12m",
    "dmards": "dmards_last12m",
    "highrisk_meds": "highriskmeds_last12m",
    "teratogenic_meds": "teratogenicmeds_last12m"
}

df_addictive = pd.read_csv(OUTPUT_DIR / f"redacted-standardised/redacted_standardised_measure_allmedrv12m_addictive_meds_rate.csv", parse_dates=["date"])
df_dmards = pd.read_csv(OUTPUT_DIR / f"redacted-standardised/redacted_standardised_measure_allmedrv12m_dmards_rate.csv", parse_dates=["date"])
df_teratogenic = pd.read_csv(OUTPUT_DIR / f"redacted-standardised/redacted_standardised_measure_allmedrv12m_teratogenic_meds_rate.csv", parse_dates=["date"])
df_highrisk = pd.read_csv(OUTPUT_DIR / f"redacted-standardised/redacted_standardised_measure_allmedrv12m_highrisk_meds_rate.csv", parse_dates=["date"])


df_addictive['addictivemeds_last12m'] = df_addictive['addictivemeds_last12m'].fillna('missing')
df_dmards['dmards_last12m'] = df_dmards['dmards_last12m'].fillna('missing')
df_teratogenic['teratogenicmeds_last12m'] = df_teratogenic['teratogenicmeds_last12m'].fillna('missing')
df_highrisk['highriskmeds_last12m'] = df_highrisk['highriskmeds_last12m'].fillna('missing')

#Rename col of interest to consistant name
df_addictive=df_addictive.rename(columns={"addictivemeds_last12m": "HighRiskMedrv12m"})
df_dmards=df_dmards.rename(columns={"dmards_last12m": "HighRiskMedrv12m"})
df_teratogenic=df_teratogenic.rename(columns={"teratogenicmeds_last12m": "HighRiskMedrv12m"})
df_highrisk=df_highrisk.rename(columns={"highriskmeds_last12m": "HighRiskMedrv12m"})

#Get only where value =1
df_addictive=df_addictive.loc[df_addictive['HighRiskMedrv12m'] == 1]
df_dmards=df_dmards.loc[df_dmards['HighRiskMedrv12m'] == 1]
df_teratogenic=df_teratogenic.loc[df_teratogenic['HighRiskMedrv12m'] == 1]
df_highrisk=df_highrisk.loc[df_highrisk['HighRiskMedrv12m'] == 1]

#Change binary catagory to text
df_addictive=convert_binary(df_addictive, 'HighRiskMedrv12m', 'Addictive medicine', 'No record of prescription for an addictive medicine')
df_dmards=convert_binary(df_dmards, 'HighRiskMedrv12m', 'DMARD', 'No record of prescription for a DMARD')
df_teratogenic=convert_binary(df_teratogenic, 'HighRiskMedrv12m', 'Teratogenic medication', 'No record of prescription for a teratogenic medication')
df_highrisk=convert_binary(df_highrisk, 'HighRiskMedrv12m', 'Any high risk medication', 'No record of prescription for a high risk medication')

#Calculate rates
calculate_rate(df_addictive, 'had_anymedrev12m', 'population', rate_per=100, round_rate=False)
calculate_rate(df_dmards, 'had_anymedrev12m', 'population', rate_per=100, round_rate=False)
calculate_rate(df_teratogenic, 'had_anymedrev12m', 'population', rate_per=100, round_rate=False)
calculate_rate(df_highrisk, 'had_anymedrev12m', 'population', rate_per=100, round_rate=False)

#Combine to single DF
plt.figure(figsize=(15, 8))

plt.plot(df_addictive["date"], df_addictive["rate"])
plt.plot(df_dmards["date"], df_dmards["rate"])
plt.plot(df_teratogenic["date"], df_teratogenic["rate"])
plt.plot(df_highrisk["date"], df_highrisk["rate"])

x_labels = sorted(df_highrisk["date"].unique())

plt.ylabel("Percentage of people who recieved a medication review within the previous 12 months")
plt.xlabel("Date")
plt.xticks(x_labels, rotation="vertical")

#Format dates for x-axis
dtFmt = mdates.DateFormatter('%B %Y') # define the date formatting
plt.gca().xaxis.set_major_formatter(dtFmt) # apply the format to the desired axis 

all_df=pd.concat([df_addictive, df_dmards, df_teratogenic, df_highrisk])

plt.ylim(
    bottom=0,
    top=100
    if all_df['rate'].isnull().values.all()
    else all_df['rate'].max() * 1.05,
)
xpadding=15*86400000000000
plt.xlim([x_labels[0]-xpadding, x_labels[-1]+xpadding]) #Force x axis to include all dates from csv even if data redacted
#plt.autoscale(axis='x')

plt.grid()

plt.legend(['Addictive medication', 'DMARD', 'Teratogenic medication', 'Any high risk medication'], bbox_to_anchor=(1.04, 1), loc="upper left",  fontsize="16")



plt.vlines(
    x=[pd.to_datetime("2020-03-23")],
    ymin=0,
    ymax=all_df['rate'].max() * 1.05,
    colors="orange",
    ls=(0, (5, 10)),
    label="First National Lockdown",
)

plt.vlines(
    x=[pd.to_datetime("2020-11-05")],
    ymin=0,
    ymax=all_df['rate'].max() * 1.05,
    colors="orange",
    ls=(0, (5, 10)),
    label="Second National Lockdown",
)

plt.vlines(
    x=[pd.to_datetime("2021-01-05")],
    ymin=0,
    ymax=all_df['rate'].max() * 1.05, 
    colors="orange",
    ls=(0, (5, 10)),
    label="Third National Lockdown",
)


plt.tight_layout()

outputfilename = OUTPUT_DIR / f"figures/allmedrv12m_combinedhighrisk_rate_percentage.png"

plt.savefig(outputfilename)
plt.close()

#Add column for rate per 1000 patients
#calculate_rate(df, numerator_col, 'population', rate_per=100, round_rate=False)
#plot_measures(df, filename=f"{med_review}_{breakdownby}_rate_percentage", title="", column_to_plot="rate", y_label=f"Percentage of people who received a {med_review_dict[med_review]}", category=breakdownbycol)
