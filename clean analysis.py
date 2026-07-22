import pandas as pd
import matplotlib.pyplot as plt

# ====================================================
# 1. Load data
# ====================================================
lct = pd.read_csv(
    "Data set/ukpn-low-carbon-technologies-lsoa.csv"
)

population = pd.read_excel(
    "Data set/population_change.xlsx",
    header=2,
)

households = pd.read_excel(
    "Data set/households.xlsx",
    header=2,
)

# ====================================================
# 2. Clean demographic data
# ====================================================

# Rename the population columns to shorter, consistent names.
population = population.rename(
    columns={
        "LA code": "local_authority_code",
        "LA name": "local_authority",
        "Usual resident population, 2021": "population",
    }
)

# Keep only the population columns needed for this analysis.
population = population[
    [
        "local_authority_code",
        "local_authority",
        "population",
    ]
].copy()


# Rename the household columns.
households = households.rename(
    columns={
        "LA code": "local_authority_code",
        "Number of households with at least one usual resident, 2021": "households",
    }
)

# Keep only the household columns needed for this analysis.
households = households[
    [
        "local_authority_code",
        "households",
    ]
].copy()


# Combine population and household figures using the official local-authority code.
demographics = population.merge(
    households,
    on="local_authority_code",
    how="inner",
    validate="one_to_one",
)

# Remove spreadsheet footer rows or other records that do not contain all the fields required for the analysis.
demographics = demographics.dropna(
    subset=[
        "local_authority_code",
        "local_authority",
        "population",
        "households",
    ]
).copy()

# ============================================================
# 3. Prepare London technology data
# ============================================================

# Keep only records belonging to London boroughs.
london_lct = lct[
    lct["County Council"] == "London"
    ].copy()


# Summarise connections by borough and technology.
london_summary = (
    london_lct.groupby(
        [
            "local_authority_code", 
            "local_authority",
            "Type"
        ]
    )["LCT Connections"]
    .sum()
    .reset_index()
)

# Reshape data in pivot table: each row is one London borough, each technology becomes a separate column, each cell contains the number of connections
london_tech = london_summary.pivot_table(
    index=[
        "local_authority_code",
        "local_authority",
    ],
    columns="Type",
    values="LCT Connections",
    fill_value=0,
)

# Turn the authority code and borough name from index levels
# back into ordinary columns.
london_analysis = london_tech.reset_index()


# ====================================================
# 4. Merge London technology and demographic data
# ====================================================

# Add population and household figures to each London borough.
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

# Validate the merged London dataset.
assert london_analysis["local_authority_code"].nunique() == 33
assert london_analysis["local_authority_code"].is_unique
assert london_analysis[
    [
        "population",
        "households",
    ]
].isna().sum().sum() == 0

# ====================================================
# 5. Calculate totals and normalized rates
# ====================================================

# Store the names of the technology columns before adding
# population, household, and calculated columns.
technology_columns = london_tech.columns.tolist()


# Calculate the total number of recorded LCT connections
# in each borough.
london_analysis["total_lct"] = (
    london_analysis[technology_columns]
    .sum(axis=1)
)


# Calculate total LCT connections per 1000 residents.
london_analysis["lct_per_1000_people"] = (
    london_analysis["total_lct"]
    / london_analysis["population"]
    * 1000
)


# Calculate total LCT connections per 1000 households.
london_analysis["lct_per_1000_households"] = (
    london_analysis["total_lct"]
    / london_analysis["households"]
    * 1000
)


# Calculate Solar PV connections per 1000 households.
london_analysis["solar_per_1000_households"] = (
    london_analysis["Solar PV"]
    / london_analysis["households"]
    * 1000
)


# Calculate heat-pump connections per 1000 households.
london_analysis["heat_pumps_per_1000_households"] = (
    london_analysis["Heat Pump"]
    / london_analysis["households"]
    * 1000
)


# Calculate battery-storage connections per 1000 households.
london_analysis["batteries_per_1000_households"] = (
    london_analysis["Battery Storage"]
    / london_analysis["households"]
    * 1000
)


# Calculate EV charging-point connections per 1000 households.
london_analysis["ev_per_1000_households"] = (
    london_analysis["EV Charging Point"]
    / london_analysis["households"]
    * 1000
)

# ====================================================
# 6. London technology overview
# ====================================================

# Calculate the total number of connections for each technology across all London boroughs.
technology_connection_totals = (
    london_tech.sum(axis=0)
    .sort_values(ascending=False)
)

print("\nTotal London connections by technology:")
print(technology_connection_totals)

# Visualise total London connections by technology.
fig, ax = plt.subplots(figsize=(9, 6))

technology_connection_totals.sort_values().plot(
    kind="barh",
    ax=ax,
)

for container in ax.containers:
    ax.bar_label(
        container,
        fmt="{:,.0f}",
        padding=3,
    )

ax.set_xlim(
    0,
    technology_connection_totals.max() * 1.15,
)

ax.set_title("London Low-Carbon Technology Connections by Type")
ax.set_xlabel("Total Recorded Connections")
ax.set_ylabel("Technology")

plt.tight_layout()

# Save chart as PNG
# fig.savefig(
#     "images/london_connections_by_technology.png",
#     dpi=300,
#     bbox_inches="tight",
# )

plt.show()

# Identify the borough with the highest absolute number of connections for each technology.
absolute_leaders = pd.DataFrame(
    {
        "Borough": london_tech.idxmax(),
        "Technology Connections": london_tech.max(),
    }
)

# Extract only the readable borough name from the two-level index returned by idxmax().
absolute_leaders["Borough"] = absolute_leaders[
    "Borough"
].apply(
    lambda index_value: index_value[1]
)

print("\nAbsolute leader for each technology in London:")
print(absolute_leaders)



# ====================================================
# 7. Compare raw and normalized borough rankings
# ====================================================

# Create a table ranked by total recorded LCT connections.
raw_ranking = (
    london_analysis[
        [
            "local_authority",
            "total_lct",
        ]
    ]
    .sort_values(
        "total_lct",
        ascending=False,
    )
    .reset_index(drop=True)
)

# Add rank numbers beginning at 1.
raw_ranking["raw_rank"] = (
    raw_ranking.index + 1
)


# Create a second table ranked by LCT connections per 1,000 households.
household_ranking = (
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
    .reset_index(drop=True)
)

# Add normalized rank numbers beginning at 1.
household_ranking["household_rank"] = (
    household_ranking.index + 1
)

# Combine both rankings into one row per borough.
ranking_comparison = raw_ranking.merge(
    household_ranking,
    on="local_authority",
    how="inner",
    validate="one_to_one",
)

# Calculate how many ranking positions each borough gains or loses after adjusting for household numbers.
ranking_comparison["rank_change"] = (
    ranking_comparison["raw_rank"]
    - ranking_comparison["household_rank"]
)


print("\nRaw and household-normalized ranking comparison:")
ranking_display = ranking_comparison[
    [
        "local_authority",
        "total_lct",
        "raw_rank",
        "lct_per_1000_households",
        "household_rank",
        "rank_change",
    ]
].copy()

ranking_display["lct_per_1000_households"] = (
    ranking_display["lct_per_1000_households"].round(2)
)

print(
    ranking_display
    .sort_values("household_rank")
    .head(10)
)

# ====================================================
# 8. Visualise raw and normalised rankings
# ====================================================

# Select the ten highest-ranked boroughs for each measure.
# Sorting in ascending order places the largest value at the
# top of each horizontal bar chart.
top10_raw = raw_ranking.head(10).sort_values(
    "total_lct",
    ascending=True,
)

top10_household_rate = household_ranking.head(10).sort_values(
    "lct_per_1000_households",
    ascending=True,
)


# Create one figure containing two separate chart axes.
fig, (ax1, ax2) = plt.subplots(
    ncols=2,
    figsize=(16, 7),
)


# ----------------------------------------------------
# Left chart: raw LCT totals
# ----------------------------------------------------
ax1.barh(
    top10_raw["local_authority"],
    top10_raw["total_lct"],
)

# Add the raw connection total beside each bar.
for container in ax1.containers:
    ax1.bar_label(
        container,
        fmt="{:,.0f}",
        padding=4,
    )

# Add space for the labels.
ax1.set_xlim(
    0,
    top10_raw["total_lct"].max() * 1.18,
)

ax1.set_title(
    "Top 10 by Total LCT Connections"
)
ax1.set_xlabel("Total LCT Connections")


# ----------------------------------------------------
# Right chart: household-normalised rates
# ----------------------------------------------------
ax2.barh(
    top10_household_rate["local_authority"],
    top10_household_rate["lct_per_1000_households"],
)

# Add the normalised rate beside each bar.
for container in ax2.containers:
    ax2.bar_label(
        container,
        fmt="{:.1f}",
        padding=4,
    )

# Add space for the labels.
ax2.set_xlim(
    0,
    top10_household_rate[
        "lct_per_1000_households"
    ].max()
    * 1.18,
)

ax2.set_title(
    "Top 10 per 1,000 Households"
)
ax2.set_xlabel(
    "LCT Connections per 1,000 Households"
)

# Add one overall title describing the comparison.
fig.suptitle(
    "London Borough LCT Rankings: Raw Totals vs Household-Normalised Rates",
    fontsize=15,
)

plt.tight_layout()

# Save chart as PNG
# fig.savefig(
#     "images/raw_vs_normalised_rankings.png",
#     dpi=300,
#     bbox_inches="tight",
# )

plt.show()


# ====================================================
# 9. Identify the largest ranking changes
# ====================================================

# Select the five boroughs that rise the most after
# adjusting for the number of households.
biggest_risers = (
    ranking_comparison.nlargest(
        5,
        "rank_change",
    )[
        [
            "local_authority",
            "raw_rank",
            "household_rank",
            "rank_change",
        ]
    ]
    .copy()
)

# Add a label explaining the direction of movement.
biggest_risers["movement"] = "Rose"


# Select the five boroughs that fall the most after
# adjusting for the number of households.
biggest_fallers = (
    ranking_comparison.nsmallest(
        5,
        "rank_change",
    )[
        [
            "local_authority",
            "raw_rank",
            "household_rank",
            "rank_change",
        ]
    ]
    .copy()
)

# Add a label explaining the direction of movement.
biggest_fallers["movement"] = "Fell"


# Combine the risers and fallers into one summary table.
ranking_movers = pd.concat(
    [
        biggest_risers,
        biggest_fallers,
    ],
    ignore_index=True,
)

print("\nLargest ranking changes after household normalisation:")
print(ranking_movers)

# ====================================================
# 10. Compare normalised adoption by technology
# ====================================================

# Match each readable technology name to its corresponding
# connections-per-1,000-households column.
technology_metrics = {
    "Solar PV": "solar_per_1000_households",
    "EV Charging Points": "ev_per_1000_households",
    "Battery Storage": "batteries_per_1000_households",
    "Heat Pumps": "heat_pumps_per_1000_households",
}


# Create an empty list that will hold one small ranking table
# for each technology.
technology_ranking_tables = []


# Repeat the ranking process for every technology in the dictionary.
for technology_name, metric_column in technology_metrics.items():

    # Select the five boroughs with the highest rate for
    # the current technology.
    top_boroughs = (
        london_analysis[
            [
                "local_authority",
                metric_column,
            ]
        ]
        .nlargest(
            5,
            metric_column,
        )
        .copy()
    )

    # Rename the metric column so every technology table has
    # the same column structure.
    top_boroughs = top_boroughs.rename(
        columns={
            metric_column: "connections_per_1000_households",
        }
    )

    # Record which technology these rows represent.
    top_boroughs["technology"] = technology_name

    # Add ranking positions from 1 to 5.
    top_boroughs["technology_rank"] = range(
        1,
        len(top_boroughs) + 1,
    )

    # Add the completed table to the list.
    technology_ranking_tables.append(top_boroughs)


# Stack the four technology-ranking tables into one table.
technology_leaders = pd.concat(
    technology_ranking_tables,
    ignore_index=True,
)
# Round to 2 decimals.
technology_leaders["connections_per_1000_households"] = (
    technology_leaders[
        "connections_per_1000_households"
    ].round(2)
)

print("\nTop boroughs by normalised technology connections:")

for technology_name in technology_metrics:
    technology_table = technology_leaders[
        technology_leaders["technology"] == technology_name
    ][
        [
            "technology_rank",
            "local_authority",
            "connections_per_1000_households",
        ]
    ].rename(
        columns={
            "technology_rank": "Rank",
            "local_authority": "Borough",
            "connections_per_1000_households": "Connections per 1,000 households",
        }
    )

    print(f"\n{technology_name}")
    print(technology_table.to_string(index=False))
# ----------------------------------------------------
# Visualise the leading boroughs for each technology
# ----------------------------------------------------

# Create one figure containing four chart panels.
fig, axes = plt.subplots(
    nrows=2,
    ncols=2,
    figsize=(14, 8),
)

# Convert the two-dimensional collection of axes into a simple
# one-dimensional sequence that is easier to loop through.
axes = axes.flatten()


# Create one chart for each technology.
for ax, (technology_name, metric_column) in zip(
    axes,
    technology_metrics.items(),
):

    # Select the five boroughs with the highest rate.
    #
    # Sorting from smallest to largest places the highest value
    # at the top of the horizontal chart.
    chart_data = (
        london_analysis[
            [
                "local_authority",
                metric_column,
            ]
        ]
        .nlargest(
            5,
            metric_column,
        )
        .sort_values(
            metric_column,
            ascending=True,
        )
    )

    # Draw the horizontal bars.
    ax.barh(
        chart_data["local_authority"],
        chart_data[metric_column],
        height=0.4,
    )

    # Add the rate beside each bar.
    for container in ax.containers:
        ax.bar_label(
            container,
            fmt="{:.1f}",
            padding=4,
        )

    # Leave additional horizontal space for the labels.
    ax.set_xlim(
        0,
        chart_data[metric_column].max() * 1.18,
    )

    # Add the chart title and axis labels.
    ax.set_title(technology_name)
    ax.set_xlabel("Connections per 1,000 Households")


# Add one title for the complete four-chart figure.
fig.suptitle(
    "Leading London Boroughs by Low-Carbon Technology",
    fontsize=16,
)

# Leave room at the top for the overall title.
plt.tight_layout(
    rect=[0, 0, 1, 0.96]
)

# Save chart as PNG
# fig.savefig(
#     "images/technology_leaders_by_household.png",
#     dpi=300,
#     bbox_inches="tight",
# )

plt.show()
