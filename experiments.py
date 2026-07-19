import pandas as pd
import matplotlib.pyplot as plt

# ====================================================
# 1. Load Data
# ====================================================
# UKPN Low carbon technology dataset
# Each row represents a technology record for a particular LSOA (Lower Layer Super Output Area).
lct = pd.read_csv("Data set/ukpn-low-carbon-technologies-lsoa.csv")

# UKPN primary substation capacity dataset
# contains network-capacity information for primary substations rather than local-authority-level information
capacity = pd.read_csv("Data set/ukpn_primary_postcode_area.csv")

# ONS population density data
# density = pd.read_excel("Data set/population_and_area.xlsx", header=5)

# ONS population data (2021)
population = pd.read_excel(
    "Data set/population_change.xlsx",
    header=2, # second row is used as header with column names
)

# ONS number of households data
households = pd.read_excel("Data set/households.xlsx", header=2)


# ====================================================
# 2. Quick Data Set Checks
# ====================================================
# Display the first five rows and the column names to see what the dataset looks like, see naming conventions, etc
print("Quick check of dataset's first five rows and column names:")
print(lct.head()) # Display the first five rows of the LCT dataset
print(lct.columns) # Display every column name in the LCT dataset.
print()


# ====================================================
# 3. Summary Tables
# ====================================================
# Count how many rows belong to each technology type.
# Important:
# These are row counts, not total LCT connection counts. A row can contain more than one connection.
print("What technologies are there? and how many instances (rows) of each?")
print(lct["Type"].value_counts())

# Calculate the top 20 total number of LCT connections of the local authorities.
print("\nWhat 20 local authorities have the most LCT conncentions?")
print(
    lct.groupby("local_authority")["LCT Connections"]
    .sum()
    .sort_values(ascending=False)
    .head(20)
)

# Calculate the total number of connections belonging to each technology across all local authorities
print("\nWhat type of technology have the most conncentions?")
print(lct.groupby("Type")["LCT Connections"]
      .sum()
      .sort_values(ascending=False)
)

# Count missing values separately for every LCT column.
print("\nHow many missing values in each column?")
print(lct.isna()
      .sum()
)
print()


# ====================================================
# 4. Chart for top local authorities and types of connections
# ====================================================

# ----------------------------------------------------
# 4.1 Prepare the local-authority chart data
# ----------------------------------------------------

# # Calculate the ten local authorities with the largest total number of LCT connections.
# Top 10 Local authorities with most LCT connections
# Already did this for the top 20, but oh well
top10loc = (
    lct.groupby("local_authority")["LCT Connections"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# ----------------------------------------------------
# 4.2 Prepare the technology chart data
# ----------------------------------------------------
# Calculate the ten technology types with the largest total number of connections.
# Count and sort tech with by LCT Connections
# Already did this, but oh well
top10tech = (
    lct.groupby("Type")["LCT Connections"]
    .sum()
    .sort_values(ascending=False)
)

# ----------------------------------------------------
# 4.3 Prepare figure for the two charts
# ----------------------------------------------------
# Create one figure containing two axes positioned side by side.
# ax1 will be the left chart, ax2 will be the right chart
# ncols=2: create two chart columns
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(14, 6))


# ----------------------------------------------------
# Local-authority chart
# ----------------------------------------------------
# Sorting it to make it from smallest and the top and largest at the bottom in the horizontal barchart
top10loc.sort_values().plot(kind="barh", ax=ax1)

ax1.set_title("Top 10 Local Authorities by Low Carbon Technology Connections")
ax1.set_xlabel("Total LCT Connections")
ax1.set_ylabel("Local Authority")

# ----------------------------------------------------
# Technology-type chart
# ----------------------------------------------------
# Sorting it to make it from smallest and the top and largest at the bottom in the horizontal barchart
top10tech.sort_values().plot(kind="barh", ax=ax2)

# bar_label writes the numeric total beside each bar. {:,.0f} formats the values with commas and no decimal places.
for container in ax2.containers:
    ax2.bar_label(container, fmt="{:,.0f}", padding=3)

# Extend the horizontal axis beyond the largest value, + 15% extra space for the labels
ax2.set_xlim(0, top10tech.max() * 1.15)

ax2.set_title("Low Carbon Technology Connections by Type")
ax2.set_xlabel("Total LCT Connections")
ax2.set_ylabel("Type")

plt.tight_layout() # Automatically improve spacing so chart elements do not overlap.
plt.show()


# ====================================================
# 5. Analysis
# ====================================================

# ----------------------------------------------------
# 5.1 Create an authority-by-technology summary
# ----------------------------------------------------

# Group and calculate the total of the original LCT records by: 1. local authority, 2. technology type
authority_tech = (
    lct.groupby(["local_authority", "Type"])["LCT Connections"]
    .sum()
    .reset_index() # converts the grouped index back into normal columns
)
# quick check for the first 20 rows 
# print("Technology mix within local Authorities")
# print(authority_tech.head(20))


# ----------------------------------------------------
# 5.2 Quick check of a random borough's technology records
# ----------------------------------------------------
# The result contains one row for each technology recorded in Bromley.
bromley = authority_tech[authority_tech["local_authority"] == "Bromley"]
print("bromley:")
print(bromley)
print()

# ====================================================
# 6. Compare two authoritie's mixes
# ====================================================
# This section compares the technology composition of Bromley with the technology composition of East Suffolk.

# Filter for and sort its technologies from the largest connection total to the smallest.
bromley = authority_tech[authority_tech["local_authority"] == "Bromley"
].sort_values("LCT Connections", ascending=False
)
eSuffolk = authority_tech[
    authority_tech["local_authority"] == "East Suffolk"
].sort_values("LCT Connections", ascending=False
)

print("Compare tech mixes:")
print(bromley)
print(eSuffolk)

# ====================================================
# 7. Calculate each technology's percentage share
# ====================================================
# For every row, calculate the total number of connections in that row's local authority.
# transform("sum") returns a result with the same number of rows as authority_tech.
#   This allows the authority total to be placed beside every technology row belonging to that authority.
authority_tech["authority_total"] = authority_tech.groupby("local_authority")["LCT Connections"
    ].transform("sum"
)
# Divide each technology's connection count by its authority's total and multiply by 100 to get a percentage.
authority_tech["tech_share"] = (
    authority_tech["LCT Connections"] / authority_tech["authority_total"
    ] * 100
)

# ----------------------------------------------------
# 7.1 Compare two authorities' tech mixes
# ----------------------------------------------------
# Keep only Bromley and East Suffolk
comparison = authority_tech[
    authority_tech["local_authority"].isin(["Bromley", "East Suffolk"])
    ].sort_values(["local_authority", "tech_share"], # sorted first by authority name, then largest technology share to the smallest.
    ascending=[True, False]
)

print(comparison.round({"tech_share": 2})) # round % to two decimals


# ====================================================
# 8. Looking at London boroughs
# ====================================================
# Only keep rows with London as the County Council
london_lct = lct[
    lct["County Council"] == "London"
]  

# Print all local authorities in London that are included
# print(
#     london_lct["local_authority"].unique()
# )  

# ----------------------------------------------------
# 8.1 Calculate total LCT connections for each London borough
# ----------------------------------------------------
# Total LCTs within each local authority in desc order
london_totals = (
    london_lct.groupby("local_authority")["LCT Connections"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTotal LCT connections in each London local authority:")
print(london_totals)

# ----------------------------------------------------
# 8.2 Chart total LCT connections for every London borough
# ----------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 8)) # prep figure

london_totals.sort_values().plot(kind="barh", ax=ax) # sort totals and draw h bar

ax.set_title("Low Carbon Technology Connections by London Borough")
ax.set_xlabel("Total LCT Connections")
ax.set_ylabel("London Borough")

plt.tight_layout()
plt.show()


# ====================================================
# 9. Examine Bromley's technology mix
# ====================================================
bromley = london_lct[london_lct["local_authority"] == "Bromley"] # Already did this withe the full authority list, but oh well
 
# Group, calculate and sort
bromley_summary = (
    bromley.groupby("Type")["LCT Connections"]
    .sum()
    .sort_values(ascending=False)
)

print("\nBromley Tech Mix:")
print(bromley_summary)

# Create a chart for Bromley's technology totals.
fig, ax = plt.subplots(figsize=(8, 5))

bromley_summary.sort_values().plot(kind="barh", ax=ax)

ax.set_title("Technology Mix in Bromley")
ax.set_xlabel("Total LCT Connections")
ax.set_ylabel("Technology")

for container in ax.containers:
    ax.bar_label(container, fmt="{:,.0f}", padding=5)

plt.tight_layout()
plt.show()



# ====================================================
# 10. Build the main London technology table
# ====================================================

# Aggregate by official authority code, borough name, and technology.
# Keeping the code here gives us a reliable key for later merges.
london_summary = (
    london_lct.groupby(
        [
            "local_authority_code", # ID for demographic merges
            "local_authority", # readable name
            "Type", # separates different technologies
        ]
    )["LCT Connections"]
    .sum()
    .reset_index() # turn index into normal columns
)

# Reshape into one row per borough and one column per technology.
london_tech = london_summary.pivot_table(
    index=[
        "local_authority_code",
        "local_authority",
    ],
    columns="Type",
    values="LCT Connections",
    fill_value=0, # missing values will become 0s instead of NaN
)

# ----------------------------------------------------
# 10.1 Rank boroughs by their total LCT connections
# ----------------------------------------------------
london_totals = (
    london_tech.sum(axis=1) # adds across all technology columns in each row, without inserting a non-technology "totals" column
    .sort_values(ascending=False)
)
# Take the first ten index values from the ranked totals.
# Because london_tech uses a two-level index, each index value contains both the authority code and the authority name.
top10_london_index = london_totals.head(10).index

# Use those index values to select the ten highest-total boroughs from the technology table.
top10_london_tech = london_tech.loc[top10_london_index]

# Create a copy for plotting.
# The original top10_london_tech table retains its official authority-code-and-name index for calculations.
top10_london_plot = top10_london_tech.copy()

# Replace the plotting copy's two-level index with only the readable local-authority names.
top10_london_plot.index = (
    top10_london_plot.index.get_level_values(
        "local_authority"
    )
)

# ----------------------------------------------------
# 10.2 Create a stacked chart of the top ten boroughs
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 7))

top10_london_plot.iloc[::-1].plot( #iloc[::-1] reverses the row order so the highest-ranked borough appears at the top.
    kind="barh",
    stacked=True,
    ax=ax,
)

ax.set_title(
    "Technology Mix of Top 10 London Boroughs by LCT Connections"
)
ax.set_xlabel("Total LCT Connections")
ax.set_ylabel("London Borough")

plt.tight_layout()
plt.show()


# ====================================================
# 11. Calculate technology percentages for the top ten
# ====================================================
# Divide every technology value by its borough's row total.
top10_london_share = (
    top10_london_tech.div( 
        top10_london_tech.sum(axis=1),  # one total for each borough
        axis=0,  # align those totals with the table's row index
    )
    * 100 # convert into %
)
print("\nTech Mix (%) across Top 10 London Boroughs")
print(top10_london_share.round(2)) # round to 2 decimals


# ====================================================
# 12. Find absolute technology leaders across London
# ====================================================
# finds the row index with the highest value in every technology column.
absolute_leaders = london_tech.idxmax() 

# London_tech has a two-level index, a tuple containing: 1. the authority code, 2. the authority name
# Extract the readable authority name from each index tuple.
absolute_leader_names = absolute_leaders.apply(
    lambda index_value: index_value[1]
)
print("\nLeading London boroughs for each technology")
print(absolute_leader_names)

# find the highest numeric connection value in each technology column.
absolute_values = london_tech.max()

print("\nNumber of LCT connections in the leading boroughs")
print(absolute_values)

# ====================================================
# 13. Find percentage-share leaders across London
# ====================================================
# Convert every borough's technology counts into percentages of that borough's complete LCT mix.
london_share = london_tech.div(london_tech.sum(axis=1),axis=0) * 100

# For each technology, find the borough whose technology percentage is the highest.
share_leaders = london_share.idxmax()

# Find the corresponding highest percentage and round it to two decimal places.
share_values = london_share.max().round(2)

print("\nLondon boroughs with the highest % of each technology")
print(share_leaders)

print("\nPercentage of each technology within the leading boroughs mix")
print(share_values)


# ----------------------------------------------------
# 13.1 Put the percentage leaders into a display table
# ----------------------------------------------------
# Construct a DataFrame from the two existing Series. Each row represents one technology.
share_leader_details = (
    pd.DataFrame(  # creates a new table from the two existing Series:
        {"Borough": share_leaders, "Highest Share (%)": share_values}
    )
)
# Calculate the total LCT connections in every borough.
# The Borough column contains index tuples matching london_tech's two-level index, so map() can use those tuples to look up the corresponding borough totals.
share_leader_details["Total LCT Connections"] = share_leader_details["Borough"].map(
    london_tech.sum(axis=1)  # calculates the total LCT connections for every borough.
)
print("\nPercentage leaders:")
print(share_leader_details)



# ====================================================
# 14. Repeat the share analysis with a minimum threshold
# ====================================================
# Keep only boroughs with at least 500 total LCT connections (to not skew the data too much)
eligible_boroughs = london_tech[london_tech.sum(axis=1) >= 500]

#  Convert the eligible boroughs' technology counts into row-level percentages.
eligible_share = eligible_boroughs.div(eligible_boroughs.sum(axis=1), axis=0) * 100

# Store the leading borough index for each technology.
eligible_leaders = eligible_share.idxmax()

# Store the leading percentage for each technology.
eligible_share_values = eligible_share.max().round(2)


print("\nLeading boroughs with a minimum of 500 total connections:")
print("the borough with the highest eligible percentage for each technology")
print(eligible_leaders)
print("corresponding percentage values")
print(eligible_share_values)
print()


# Create one summary table containing the eligible leaders and their % share
leader_details = pd.DataFrame(
    {"Borough": eligible_leaders, "Share (%)": eligible_share_values}
)

# ----------------------------------------------------
# 14.1 Look up the actual technology count for every leader
# ----------------------------------------------------
# eligible_leaders.items() produces pairs containing: technology and leading borough
# For every pair, .loc[borough, technology] retrieves the value at the matching borough row and technology column.
leader_details["Technology Connections"] = [
    eligible_boroughs.loc[borough, technology]
    for technology, borough in eligible_leaders.items()
]

# Add each leading borough's total number of LCT connections.
# The Borough column contains the same two-part index values used by eligible_boroughs, allowing map() to perform the lookup.
leader_details["Total LCT Connections"] = leader_details["Borough"].map(
    eligible_boroughs.sum(axis=1)
)
print()
print(leader_details)


# ====================================================
# 15. Looking at capacity
# ====================================================
# This section inspects the primary-substation capacity dataset.
#
# It is currently exploratory and has not yet been joined to the
# London borough analysis.

# ----------------------------------------------------
# 15.1 Inspect the dataset structure
# ----------------------------------------------------
print("\nCapacity info:")  # How many rows? What data types? Missing values?
print(capacity.info())

# ----------------------------------------------------
# 15.2 Inspect the numeric capacity columns
# ----------------------------------------------------
# Store the names of the three numeric columns being examined.
# Keeping them in a list avoids repeating the column names in several separate selections.
capacity_columns = [
    "Firm Capacity Winter",
    "Firm Capacity Summer",
    "Unutilised Capacity",
]

print("\nCapacity describe:") 
 #describe() reports Numeric: Mins, Maxs, averges, quartiles, Texts: number of unique values, most common value
print(capacity[capacity_columns].describe())

# ----------------------------------------------------
# 15.4 Inspect missing values
# ----------------------------------------------------
print("\nCapacity number of missing values:")
print(capacity.isna().sum())


# ----------------------------------------------------
# 15.5 Inspect demand-capacity classifications
# ----------------------------------------------------
# Count the number of primary areas in each Red-Amber-Green demand category.
print("\nNumber of DemandRAD")
print(capacity["DemandRAG (Red Amber Green)"].value_counts(dropna=False)) # dropna=False includes missing values in the displayed count.


# ----------------------------------------------------
# 15.6 Inspect seasons of constraint
# ----------------------------------------------------
# Count how many primary areas are constrained in winter or summer.

print("\nNumber of Seasons of constraint")
print(capacity["Seasonofconstraint"].value_counts(dropna=False))


# ====================================================
# 16. Borough's population and number of households
# ====================================================
# This section prepares the ONS demographic datasets and joins
# them to the London technology table.
#
# Population and household counts allow the analysis to compare
# boroughs of different sizes more fairly.

# ----------------------------------------------------
# 16.1 Clean the population dataset
# ----------------------------------------------------
# Rename the original ONS headings to shorter, consistent names.
# local_authority_code will be the main merge key.
population = population.rename(
    columns={
        "LA code": "local_authority_code",
        "LA name": "local_authority",
        "Usual resident population, 2021": "population",
    }
)

# Keep only the three population columns needed for the analysis.
population = population[
    [
        "local_authority_code",
        "local_authority",
        "population",
    ]
].copy() # creates an independent DataFrame rather than a view of the original table.

# ----------------------------------------------------
# 16.2 Clean the household dataset
# ----------------------------------------------------
# Rename the original ONS headings to match the population table and the UKPN authority-code column.
households = households.rename(
    columns={
        "LA code": "local_authority_code",
        "LA name": "local_authority",
        "Number of households with at least one usual resident, 2021": "households",
    }
)
# Keep only the authority code and household count.
# The authority name is already available in the population table, so it does not need to be retained here.
households = households[
    [
        "local_authority_code",
        "households",
    ]
].copy() # creates an independent DataFrame rather than a view of the original table.

# ----------------------------------------------------
# 16.3 Merge population and household datasets
# ----------------------------------------------------
demographics = population.merge(
    households,
    on="local_authority_code",
    how="inner", # Keeps only authority codes found in both datasets.
    validate="one_to_one", # checks that every authority code appears no more than once in each table.
)

# ----------------------------------------------------
# 16.4 Remove unusable demographic rows
# ----------------------------------------------------
# Drop rows that are missing any of the four fields required for matching or rate calculations.
demographics = demographics.dropna(
    subset=[
        "local_authority_code",
        "local_authority",
        "population",
        "households",
    ]
).copy()

# Optional checks after removing missing demographic rows.
# print(demographics.shape)
# print(demographics.isna().sum())

# ====================================================
# 17. Merge population and households into the London table
# ====================================================
# ----------------------------------------------------
# 17.1 Prepare the London table for the demographic merge
# ----------------------------------------------------
# london_tech currently stores the authority code and authority name in its two-level index.
# reset_index() turns both index levels into ordinary columns.
london_analysis = london_tech.reset_index() 

# ----------------------------------------------------
# 17.2 Merge population and households into the London table
# ----------------------------------------------------
# Select only the demographic fields needed for the London analysis.
# The local-authority name is not selected because london_analysis already contains it.
london_analysis = london_analysis.merge(
    demographics[
        [
            "local_authority_code",
            "population",
            "households",
        ]
    ],
    on="local_authority_code",
    how="left", # Keeps every borough in london_analysis even if no demographic match is found
    validate="one_to_one", # Confirms that each London authority code matches at most one demographic row.
)

# ----------------------------------------------------
# 17.3 Verify the demographic merge
# ----------------------------------------------------
print("\nVerification:")
print(
    london_analysis[
        [
            "local_authority_code",
            "local_authority",
            "population",
            "households",
        ]
    ].head()
)

## Checking missing values
# print(london_analysis.isna().sum())

# ====================================================
# 18. Calculate total LCT connections
# ====================================================
# Create a Python list containing only the technology column names.
# This protects the total calculation from accidentally including population, households, or future calculated columns.
technology_columns = london_tech.columns.tolist()

# Add all technology columns across each borough row.
london_analysis["total_lct"] = (
    london_analysis[technology_columns].sum(axis=1) # axis=1 means calculate horizontally across columns.
)

# ====================================================
# 19 Calculate normalised LCT rates and rates for specific tech
# ====================================================
# Raw totals tend to favour larger boroughs.
# Dividing by population or households allows boroughs of different sizes to be compared more fairly.

# ----------------------------------------------------
# Total LCT connections per 1,000 residents
# ----------------------------------------------------
london_analysis["lct_per_1000_people"] = (
    london_analysis["total_lct"]
    / london_analysis["population"]
    * 1000
)
# ----------------------------------------------------
# Total LCT connections per 1,000 households
# ----------------------------------------------------
london_analysis["lct_per_1000_households"] = (
    london_analysis["total_lct"]
    / london_analysis["households"]
    * 1000
)

# ----------------------------------------------------
# Solar PV connections per 1,000 households
# ----------------------------------------------------
london_analysis["solar_per_1000_households"] = (
    london_analysis["Solar PV"]
    / london_analysis["households"]
    * 1000
)

# ----------------------------------------------------
# Heat-pump connections per 1,000 households
# ----------------------------------------------------
london_analysis["heat_pumps_per_1000_households"] = (
    london_analysis["Heat Pump"]
    / london_analysis["households"]
    * 1000
)

# ----------------------------------------------------
# Battery-storage connections per 1,000 households
# ----------------------------------------------------
london_analysis["batteries_per_1000_households"] = (
    london_analysis["Battery Storage"]
    / london_analysis["households"]
    * 1000
)

# ----------------------------------------------------
# EV charging-point connections per 1,000 residents
# ----------------------------------------------------
# Population is being used as the current denominator.
# A future extension could compare EV connections with registered vehicles, car ownership, or households with access to a car.
london_analysis["ev_per_1000_people"] = (
    london_analysis["EV Charging Point"]
    / london_analysis["population"]
    * 1000
)

# ====================================================
# 20. Compare raw and normalized London rankings
# ====================================================
# ----------------------------------------------------
# Top ten boroughs by raw total
# ----------------------------------------------------
# Select the borough name and total LCT count, sort from largest to smallest, and display the first ten rows.
print("\ntop boroughs by raw total:")
print(
    london_analysis[
        ["local_authority", "total_lct"]
    ]
    .sort_values("total_lct", ascending=False)
    .head(10)
)
# ----------------------------------------------------
# Top ten boroughs by connections per 1,000 households
# ----------------------------------------------------
# This ranking adjusts the total number of connections for the number of households in each borough.
print("\ntop boroughs by household-normalised rate")
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

