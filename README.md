# London Low-Carbon Technology Analysis

A Python data analysis project exploring how recorded low-carbon technology connections vary across London boroughs.

The analysis compares raw connection totals with rates per 1,000 households to account for differences in borough size. It also identifies which boroughs lead in Solar PV, EV charging points, battery storage, and heat pumps.

## Project question

**How are recorded low-carbon technology connections distributed across London boroughs, and how do borough rankings change after adjusting for household numbers?**

## Key findings

- **Solar PV** is the most common technology in the London data, with 33,910 recorded connections.

- **EV charging points** are the second most common, with 28,857 connections.

- **Bromley** has the highest total number of recorded low-carbon technology connections findings

- **Solar PV** is the most common technology in the London.

- **Havering** ranks first after adjusting for the number of households.

- **Kingston upon Thames** rises from 12th by raw total to 3rd by connections per 1,000 households.

- **Barnet** falls from 4th by raw total to 13th after household normalisation.

- Different boroughs lead different technologies:
  - Waltham Forest leads Solar PV per 1,000 households.
  - Havering leads EV charging points per 1,000 households.
  - Richmond upon Thames leads battery storage and heat pumps per 1,000 households.

- Bromley appears in the top five for all four major technologies, indicating a relatively broad technology mix.

These findings show that raw totals alone can favour larger boroughs and may not reflect the concentration of recorded connections relative to borough size.

## Data sources

The project uses data from:

### UK Power Networks

**Low Carbon Technologies Connected by LSOA**

This dataset contains recorded low-carbon technology connections at Lower Layer Super Output Area level, including:

- Solar PV
- EV charging points
- Battery storage
- Heat pumps
- Wind
- Micro CHP
- Mini CHP
- Vehicle-to-grid charging

Source: `https://ukpowernetworks.opendatasoft.com/explore/assets/ukpn-low-carbon-technologies-lsoa/`

### Office for National Statistics

The analysis uses 2021 Census data for:

- Usual resident population
- Number of households with at least one usual resident

Sources:

- Population: `https://www.ons.gov.uk/visualisations/dvc1914/fig2/datadownload.xlsx"`
- Households: `https://www.ons.gov.uk/visualisations/dvc1914/fig7/datadownload.xlsx`

## Methodology

### 1. Data preparation

The UK Power Networks data was filtered to records where the county council was listed as London.

LSOA-level records were then aggregated by:

- Local authority code
- London borough
- Technology type

The data was reshaped into a borough-level table with one column for each technology.

### 2. Demographic data

Population and household datasets were cleaned and merged using official local-authority codes.

Using codes rather than borough names reduces the risk of mismatches caused by spelling or formatting differences.

### 3. Normalised rates

Raw totals were supplemented with the following measures:

- Total LCT connections per 1,000 residents
- Total LCT connections per 1,000 households
- Solar PV connections per 1,000 households
- EV charging LCT connections per 1,000 households
- Solar PV connections per -point connections per 1,000 households
- Battery-storage connections per 1,000 households
- Heat-pump connections per 1,000 households

The main borough comparison uses households as the denominator because the selected technologies are closely connected to housing and household-level infrastructure.

### 4. Ranking comparison

Boroughs were ranked using:

1. Total recorded LCT connections
2. Recorded LCT connections per 1,000 households

The difference between the two rankings was calculated to identify which boroughs rose or fell most after adjusting for household numbers.

## Results

### London connections by technology

| Technology              | Recorded connections |
| ----------------------- | -------------------: |
| Solar PV                |               33,910 |
| EV Charging Point       |               28,857 |
| Battery Storage         |                7,177 |
| Heat Pump               |                4,681 |
| Micro CHP               |                   38 |
| Wind                    |                   37 |
| Mini CHP                |                    2 |
| V2G – EV Charging Point |                    2 |

### Absolute technology leaders

| Technology              | Leading borough      | Connections |
| ----------------------- | -------------------- | ----------: |
| Solar PV                | Bromley              |       2,260 |
| EV Charging Point       | Bromley              |       2,977 |
| Battery Storage         | Bromley              |         621 |
| Heat Pump               | Bromley              |         338 |
| Micro CHP               | Newham               |           6 |
| Mini CHP                | Kingston upon Thames |           2 |
| V2G – EV Charging Point | Enfield              |           2 |
| Wind                    | Croydon              |          28 |

### Top boroughs by connections per 1,000 households

| Rank | Borough              | Connections per 1,000 households |
| ---: | -------------------- | -------------------------------: |
|    1 | Havering             |                            47.22 |
|    2 | Bromley              |                            45.64 |
|    3 | Kingston upon Thames |                            44.57 |
|    4 | Harrow               |                            44.34 |
|    5 | Richmond upon Thames |                            43.11 |

### Largest ranking changes

The largest upward movement was recorded by **Kingston upon Thames**, which rose nine places after household normalisation.

The largest downward movement was recorded by **Barnet**, which fell nine places.

This demonstrates that borough size has a meaningful effect on rankings based only on raw connection totals.

## Visualisations

The analysis produces three main figures:

1. Total London connections by technology
2. Top ten boroughs by raw total compared with connections per 1,000 households
3. Leading boroughs for Solar PV, EV charging points, battery storage, and heat pumps

## Tools and libraries

- Python
- pandas
- matplotlib
- Microsoft Excel data
- Visual Studio Code
- Git and GitHub

## Repository structure

```text
uk-lct-analysis/
│
├── clean analysis.py
├── experiments.py
├── analysis_notes.md
├── .gitignore
└── Data set/
    ├── ukpn-low-carbon-technologies-lsoa.csv
    ├── population_change.xlsx
    └── households.xlsx
```

The `Data set` folder is excluded from GitHub because the raw UK Power Networks files exceed GitHub’s standard file-size limits.

## Running the analysis

### 1. Clone the repository

```bash
git clone <repository-url>
cd uk-lct-analysis
```

### 2. Install the required packages

```bash
pip install pandas matplotlib openpyxl
```

### 3. Download the datasets

Download the required UK Power Networks and ONS datasets and place them inside a folder named:

```text
Data set
```

The filenames used by the script are:

```text
ukpn-low-carbon-technologies-lsoa.csv
population_change.xlsx
households.xlsx
```

### 4. Run the script

```bash
python "clean analysis.py"
```

## Limitations

- The analysis measures **recorded UK Power Networks connections**, not necessarily unique installations, devices, households, or individual adoption decisions.
- Connections per 1,000 households should therefore be interpreted as a measure of connection concentration rather than a definitive household adoption rate.
- Population and household figures are taken from the 2021 Census, while the UK Power Networks data may cover a different reporting period.
- Household numbers do not account for housing type, tenure, income, vehicle ownership, or access to off-street parking.
- The analysis is descriptive and does not establish why borough differences exist.
- The UK Power Networks service area does not cover the whole United Kingdom, so wider results should not be interpreted as nationally representative.

## Possible extensions

Future work could include:

- Comparing LCT rates with income or deprivation
- Adding housing type and tenure data
- Incorporating vehicle ownership for EV analysis
- Exploring access to off-street parking
- Mapping borough-level results
- Linking primary-substation capacity to LCT growth through geospatial analysis
- Examining changes over time if historical connection data becomes available

## Conclusion

London’s recorded low-carbon technology connections are unevenly distributed across boroughs.

Bromley leads by total volume, but Havering ranks first after adjusting for household numbers. Kingston upon Thames also performs considerably better after normalisation, while Barnet and Croydon fall in the rankings.

Different boroughs lead different technologies, suggesting that London’s low-carbon transition varies not only in scale but also in technology composition.
