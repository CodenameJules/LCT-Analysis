import pandas as pd
import matplotlib.pyplot as plt

# ====================================================
# 1. Load Data
# ====================================================
lct = pd.read_csv("Data set/ukpn-low-carbon-technologies-lsoa.csv")
capacity = pd.read_csv("Data set/ukpn_primary_postcode_area.csv")

# density = pd.read_excel("Data set/population_and_area.xlsx", header=5)
population = pd.read_excel(
    "Data set/population_change.xlsx",
    header=2,
)

households = pd.read_excel("Data set/households.xlsx", header=2)


# ====================================================
# 2. Quick Data Set Checks
# ====================================================
print(lct.head())
print(lct.columns)
print()


# ====================================================
# 3. Summary Tables
# ====================================================
print("What technologies are there? and how many instances (rows) of each?")
print(lct["Type"].value_counts())
print()
print("What 20 local authorities have the most LCT conncentions?")
print(
    lct.groupby("local_authority")["LCT Connections"]
    .sum()
    .sort_values(ascending=False)
    .head(20)
)
print()
print("What type of technology have the most conncentions?")
print(lct.groupby("Type")["LCT Connections"].sum().sort_values(ascending=False))
print()
print("How many missing values in each column?")
print(lct.isna().sum())
print()


# ====================================================
# 4. Chart for top local authorities and types of connections
# ====================================================
# Top 10 Local authorities with most LCT connections
top10loc = (
    lct.groupby("local_authority")["LCT Connections"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# Top 10 types of tech with most LCT Connections
top10tech = (
    lct.groupby("Type")["LCT Connections"].sum().sort_values(ascending=False).head(10)
)

# Graph
## Local Authories
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(14, 6))

top10loc.sort_values().plot(kind="barh", ax=ax1)

ax1.set_title("Top 10 Local Authorities by Low Carbon Technology Connections")
ax1.set_xlabel("Total LCT Connections")
ax1.set_ylabel("Local Authority")

## Types of Tech
top10tech.sort_values().plot(kind="barh", ax=ax2)

for container in ax2.containers:
    ax2.bar_label(container, fmt="{:,.0f}", padding=3)

ax2.set_xlim(0, top10tech.max() * 1.15)

ax2.set_title("Low Carbon Technology Connections by Type")
ax2.set_xlabel("Total LCT Connections")
ax2.set_ylabel("Type")

plt.tight_layout()
plt.show()


# ====================================================
# 5. Analysis
# ====================================================
authority_tech = (
    lct.groupby(["local_authority", "Type"])["LCT Connections"].sum().reset_index()
)
# quick check
# print("Technology mix within local Authorities")
# print(authority_tech.head(20))

# print("Looking at Bromley")
bromley = authority_tech[authority_tech["local_authority"] == "Bromley"]
print("bromley:")
print(bromley)
print()

# ====================================================
# 5.1 Compare two authoritie's mixes
# ====================================================
print("Compare tech mixes")
bromley = authority_tech[authority_tech["local_authority"] == "Bromley"].sort_values(
    "LCT Connections", ascending=False
)

print(bromley)

eSuffolk = authority_tech[
    authority_tech["local_authority"] == "East Suffolk"
].sort_values("LCT Connections", ascending=False)

print(eSuffolk)

# Calculate %
authority_tech["authority_total"] = authority_tech.groupby("local_authority")[
    "LCT Connections"
].transform("sum")
authority_tech["tech_share"] = (
    authority_tech["LCT Connections"] / authority_tech["authority_total"] * 100
)

comparison = authority_tech[
    authority_tech["local_authority"].isin(["Bromley", "East Suffolk"])
].sort_values(["local_authority", "tech_share"], ascending=[True, False])

print(comparison.round({"tech_share": 2}))


# Looking at London Boroughs

london_lct = lct[
    lct["County Council"] == "London"
]  # Only keeps rows with London as the County Council

print(
    london_lct["local_authority"].unique()
)  # Print all local authorities in London that are included

# Total LCTs within each local authority in desc order
london_totals = (
    london_lct.groupby("local_authority")["LCT Connections"]
    .sum()
    .sort_values(ascending=False)
)

print(london_totals)

# Graph for london authorities total LCT

fig, ax = plt.subplots(figsize=(10, 8))

london_totals.sort_values().plot(kind="barh", ax=ax)

ax.set_title("Low Carbon Technology Connections by London Borough")
ax.set_xlabel("Total LCT Connections")
ax.set_ylabel("London Borough")

plt.tight_layout()
plt.show()


# Look at bromley's tech mix
bromley = london_lct[london_lct["local_authority"] == "Bromley"]

bromley_summary = (
    bromley.groupby("Type")["LCT Connections"].sum().sort_values(ascending=False)
)

print("Bromley Tech Mix:")
print(bromley_summary)

fig, ax = plt.subplots(figsize=(8, 5))

bromley_summary.sort_values().plot(kind="barh", ax=ax)

ax.set_title("Technology Mix in Bromley")
ax.set_xlabel("Total LCT Connections")
ax.set_ylabel("Technology")

for container in ax.containers:
    ax.bar_label(container, fmt="{:,.0f}", padding=5)

plt.tight_layout()
plt.show()


# London Pivot Table for LCT mixes

london_summary = (
    london_lct.groupby(["local_authority", "Type"])["LCT Connections"]
    .sum()
    .reset_index()  # Groupby turns columns into indexes, and this resets it into columns and pivot_table() uses column names
)
london_pivot = london_summary.pivot_table(
    index="local_authority", columns="Type", values="LCT Connections", fill_value=0
)
print("Tech Mixes across London Boroughs")
print(london_pivot)

# Add a 'total' column
london_pivot["Total"] = london_pivot.sum(
    axis=1
)  # axis 0 = go down by row, axis 1 = go across columns

print(london_pivot.sort_values("Total", ascending=False))

# Top 10 Boroughs
top10_london = london_pivot.sort_values("Total", ascending=False).head(10)
print("London borough with most LCT connections")
print(top10_london)

# Stacked bar chart for top 10 boroughs
# Remove Total column before plotting tech mix so that it isn't used as a tech type
top10_london_tech = top10_london.drop(columns="Total")

fig, ax = plt.subplots(figsize=(14, 7))

top10_london_tech.plot(kind="barh", stacked=True, ax=ax)

ax.set_title("Technology Mix of Top 10 London Boroughs by LCT Connections")
ax.set_xlabel("Total LCT Connections")
ax.set_ylabel("London Borough")

plt.tight_layout()
plt.show()

# Calculate %
top10_london_share = (
    top10_london_tech.div(
        top10_london_tech.sum(axis=1),  # calculates the total of each row
        axis=0,  # divides each row by its own row total
    )
    * 100
)

print()
print("Tech Mix (%) across Top 10 London Boroughs")
print(top10_london_share.round(2))
print()

# Looking at all London Boroughs:

print("Leading London boroughs for each technology")
london_tech = london_pivot.drop(columns="Total")

absolute_leaders = london_tech.idxmax()
absolute_values = london_tech.max()

print(absolute_leaders)
print("Number of LCT connections in the leading boroughs")
print(absolute_values)

print()

print("London boroughs with the highest % of each technology")
london_share = london_tech.div(london_tech.sum(axis=1), axis=0) * 100

share_leaders = london_share.idxmax()
share_values = london_share.max().round(2)

print(share_leaders)
print("Percentage of each technology within the leading boroughs mix")
print(share_values)


share_leader_details = (
    pd.DataFrame(  # creates a new table from the two existing Series:
        {"Borough": share_leaders, "Highest Share (%)": share_values}
    )
)

share_leader_details["Total LCT Connections"] = share_leader_details["Borough"].map(
    london_tech.sum(axis=1)  # calculates the total LCT connections for every borough.
)

print(share_leader_details)
print()

# Needs minimum 500 LCT connections to be considered (to not skew the data too much)
eligible_boroughs = london_tech[london_tech.sum(axis=1) >= 500]

eligible_share = eligible_boroughs.div(eligible_boroughs.sum(axis=1), axis=0) * 100
print("Leading boroughs with a minimum of 500 total connections")
print(eligible_share.idxmax())
print(eligible_share.max().round(2))


print()
eligible_leaders = eligible_share.idxmax()
eligible_share_values = eligible_share.max().round(2)

leader_details = pd.DataFrame(
    {"Borough": eligible_leaders, "Share (%)": eligible_share_values}
)

leader_details["Technology Connections"] = [
    eligible_boroughs.loc[borough, technology]
    for technology, borough in eligible_leaders.items()
]

leader_details["Total LCT Connections"] = leader_details["Borough"].map(
    eligible_boroughs.sum(axis=1)
)
print()
print(leader_details)


# ====================================================
# 6. Looking at capacity
# ====================================================
print("\nCapacity info:")  # How many rows? What data types? Missing values?
print(capacity.info())

print(
    "\nCapacity describe:"
)  # Numeric: Mins, Maxs, averges, quartiles, Texts: number of unique values, most common value
capacity_columns = [
    "Firm Capacity Winter",
    "Firm Capacity Summer",
    "Unutilised Capacity",
]

print(capacity[capacity_columns].describe())


print("\nCapacity number of missing values:")
print(capacity.isna().sum())

print("\nNumber of DemandRAD")
print(capacity["DemandRAG (Red Amber Green)"].value_counts(dropna=False))

print("\nNumber of Seasons of constraint")
print(capacity["Seasonofconstraint"].value_counts(dropna=False))


# ====================================================
# 7. Borough's population and number of households
# ====================================================

# Clean and format datasets
population = population.rename(
    columns={
        "LA code": "local_authority_code",
        "LA name": "local_authority",
        "Usual resident population, 2021": "population",
    }
)

population = population[
    [
        "local_authority_code",
        "local_authority",
        "population",
    ]
].copy()


households = households.rename(
    columns={
        "LA code": "local_authority_code",
        "LA name": "local_authority",
        "Number of households with at least one usual resident, 2021": "households",
    }
)

households = households[
    [
        "local_authority_code",
        "households",
    ]
].copy()

# Merge datasets
demographics = population.merge(
    households,
    on="local_authority_code",
    how="inner",
    validate="one_to_one",
)

# print(demographics.head())
# print(demographics.shape)
# print(demographics.isna().sum())
# print()
# print(demographics.dtypes)

# print()
# print(
#     demographics[
#         demographics[
#             [
#                 "local_authority_code",
#                 "local_authority",
#                 "population",
#                 "households",
#             ]
#         ].isna().any(axis=1)
#     ]
# )

print()

demographics = demographics.dropna(
    subset=[
        "local_authority_code",
        "local_authority",
        "population",
        "households",
    ]
).copy()

# print(demographics.shape)
# print(demographics.isna().sum())

london_analysis = london_tech.reset_index() # turns local authority from the index into a normal column

# there is no local authority code in london_tech, creating a lookup from the original London data
london_codes = (
    london_lct[
        ["local_authority", "local_authority_code"]
    ]
    .drop_duplicates()
)

# Merge into analysis table
london_analysis = london_analysis.merge(
    london_codes,
    on="local_authority",
    how="left",
    validate="one_to_one",
)

# Merge in population and households 
london_analysis = london_analysis.merge(
    demographics[
        [
            "local_authority_code",
            "population",
            "households",
        ]
    ],
    on="local_authority_code",
    how="left",
    validate="one_to_one",
)

print(london_analysis.head())
print(london_analysis.isna().sum())

# Add total LCT connections
technology_columns = london_tech.columns.tolist()

london_analysis["total_lct"] = (
    london_analysis[technology_columns].sum(axis=1)
)

# Calculate normalised rates
london_analysis["lct_per_1000_people"] = (
    london_analysis["total_lct"]
    / london_analysis["population"]
    * 1000
)

london_analysis["lct_per_1000_households"] = (
    london_analysis["total_lct"]
    / london_analysis["households"]
    * 1000
)

# For specific technologies
london_analysis["solar_per_1000_households"] = (
    london_analysis["Solar PV"]
    / london_analysis["households"]
    * 1000
)

london_analysis["heat_pumps_per_1000_households"] = (
    london_analysis["Heat Pump"]
    / london_analysis["households"]
    * 1000
)

london_analysis["batteries_per_1000_households"] = (
    london_analysis["Battery Storage"]
    / london_analysis["households"]
    * 1000
)

london_analysis["ev_per_1000_people"] = (
    london_analysis["EV Charging Point"]
    / london_analysis["population"]
    * 1000
)

# Print top boroughs by raw total
print(
    london_analysis[
        ["local_authority", "total_lct"]
    ]
    .sort_values("total_lct", ascending=False)
    .head(10)
)

# Print top boroughs by household-normalised rate
print(
    london_analysis[
        [
            "local_authority",
            "lct_per_1000_households",
        ]
    ]
    .sort_values(
        "lct_per_1000_households",
        ascending=False,
    )
    .head(10)
)

