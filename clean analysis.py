import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# 1. Configuration
# ============================================================

LCT_FILE = "Data set/ukpn-low-carbon-technologies-lsoa.csv"
MIN_CONNECTIONS_FOR_SHARE_COMPARISON = 500


# ============================================================
# 2. Load and validate data
# ============================================================

lct = pd.read_csv(LCT_FILE)

print("Dataset shape:", lct.shape)
print("\nColumns:")
print(lct.columns.tolist())

print("\nMissing values:")
print(lct.isna().sum())


# ============================================================
# 3. Overall UK Power Networks region summaries
# ============================================================

# Count how many dataset rows exist for each technology.
# A row represents a technology recorded in an LSOA, not one connection.
technology_row_counts = lct["Type"].value_counts()

# Sum the actual number of recorded connections for each technology.
technology_connection_totals = (
    lct.groupby("Type")["LCT Connections"].sum().sort_values(ascending=False)
)

# Rank local authorities by their total number of LCT connections.
authority_totals = (
    lct.groupby("local_authority")["LCT Connections"].sum().sort_values(ascending=False)
)

print("\nTechnology row counts:")
print(technology_row_counts)

print("\nTechnology connection totals:")
print(technology_connection_totals)

print("\nTop 20 local authorities by LCT connections:")
print(authority_totals.head(20))


# ============================================================
# 4. London analysis
# ============================================================

# Restrict the analysis to London boroughs.
london_lct = lct[lct["County Council"] == "London"].copy()

print("\nNumber of London boroughs represented:")
print(london_lct["local_authority"].nunique())


# Summarise connections by borough and technology.
london_summary = (
    london_lct.groupby(["local_authority", "Type"])["LCT Connections"]
    .sum()
    .reset_index()
)

# Reshape the summary so each borough is one row and each technology
# is one column. Missing borough/technology combinations become zero.
london_tech = london_summary.pivot_table(
    index="local_authority",
    columns="Type",
    values="LCT Connections",
    fill_value=0,
)

# Calculate each borough's overall total for ranking.
london_totals = london_tech.sum(axis=1).sort_values(ascending=False)

# Select the ten boroughs with the largest overall LCT totals.
top10_borough_names = london_totals.head(10).index
top10_london_tech = london_tech.loc[top10_borough_names]

print("\nTop 10 London boroughs by total LCT connections:")
print(london_totals.head(10))


# ============================================================
# 5. Technology leaders
# ============================================================

# Absolute leaders answer:
# "Which borough has the largest number of each technology?"
absolute_leaders = pd.DataFrame(
    {
        "Borough": london_tech.idxmax(),
        "Technology Connections": london_tech.max(),
    }
)

print("\nAbsolute leader for each technology in London:")
print(absolute_leaders)


# Percentage comparisons can be distorted by boroughs with very few
# connections. Only include boroughs with at least the chosen threshold.
eligible_boroughs = london_tech[
    london_tech.sum(axis=1) >= MIN_CONNECTIONS_FOR_SHARE_COMPARISON
]

eligible_share = (
    eligible_boroughs.div(
        eligible_boroughs.sum(axis=1),
        axis=0,
    )
    * 100
)

share_leaders = eligible_share.idxmax()
share_values = eligible_share.max()

share_leader_details = pd.DataFrame(
    {
        "Borough": share_leaders,
        "Share (%)": share_values.round(2),
    }
)

# Look up the absolute technology count for each percentage leader.
share_leader_details["Technology Connections"] = [
    eligible_boroughs.loc[borough, technology]
    for technology, borough in share_leaders.items()
]

# Add the borough's overall total to make the denominator visible.
share_leader_details["Total LCT Connections"] = share_leader_details["Borough"].map(
    eligible_boroughs.sum(axis=1)
)

print(
    f"\nHighest technology shares among boroughs with at least "
    f"{MIN_CONNECTIONS_FOR_SHARE_COMPARISON} total connections:"
)
print(share_leader_details)


# ============================================================
# 6. Charts
# ============================================================

fig, (ax1, ax2) = plt.subplots(
    ncols=2,
    figsize=(16, 7),
)

# Chart 1: overall connection totals by technology.
technology_connection_totals.sort_values().plot(
    kind="barh",
    ax=ax1,
)

for container in ax1.containers:
    ax1.bar_label(
        container,
        fmt="{:,.0f}",
        padding=3,
    )

ax1.set_xlim(
    0,
    technology_connection_totals.max() * 1.15,
)
ax1.set_title("Low Carbon Technology Connections by Type")
ax1.set_xlabel("Total Connections")
ax1.set_ylabel("Technology")


# Chart 2: technology composition of the leading London boroughs.
# Reverse the row order so the highest-ranked borough appears at the top.
top10_london_tech.iloc[::-1].plot(
    kind="barh",
    stacked=True,
    ax=ax2,
)

ax2.set_title("Technology Mix of the Top 10 London Boroughs")
ax2.set_xlabel("Total Connections")
ax2.set_ylabel("London Borough")
ax2.legend(
    title="Technology",
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
)

plt.tight_layout()
plt.show()
