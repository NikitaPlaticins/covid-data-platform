import os
from dotenv import load_dotenv
import snowflake.connector
import pandas as pd
import plotly.graph_objects as go

load_dotenv()

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)

query = """
SELECT
    STATE,
    SUM(CASES) AS TOTAL_CASES,
    SUM(DEATHS) AS TOTAL_DEATHS,
    COUNT(DISTINCT COUNTY) AS COUNTIES
FROM NYT_US_COVID19
GROUP BY STATE;
"""

cursor = conn.cursor()
cursor.execute(query)

rows = cursor.fetchall()
columns = [col[0] for col in cursor.description]

df = pd.DataFrame(rows, columns=columns)

cursor.close()
conn.close()


df["MORTALITY_RATE"] = (df["TOTAL_DEATHS"] / df["TOTAL_CASES"]) * 100
df["AVG_CASES"] = df["TOTAL_CASES"] / df["COUNTIES"]
df["AVG_DEATHS"] = df["TOTAL_DEATHS"] / df["COUNTIES"]

datasets = [
    ("Top Cases", "TOTAL_CASES", "Total Cases"),
    ("Top Deaths", "TOTAL_DEATHS", "Total Deaths"),
    ("Mortality Rate (%)", "MORTALITY_RATE", "Mortality Rate (%)"),
    ("Average Cases per County", "AVG_CASES", "Average Cases"),
    ("Average Deaths per County", "AVG_DEATHS", "Average Deaths")
]

fig = go.Figure()

for i, (label, column, ylabel) in enumerate(datasets):

    top = df.sort_values(column, ascending=False).head(10)

    fig.add_trace(
        go.Bar(
            x=top["STATE"],
            y=top[column],
            visible=(i == 0),
            name=label
        )
    )

buttons = []

for i, (label, column, ylabel) in enumerate(datasets):

    visible = [False] * len(datasets)
    visible[i] = True

    buttons.append(
        dict(
            label=label,
            method="update",
            args=[
                {"visible": visible},
                {
                    "yaxis": {"title": ylabel}
                }
            ]
        )
    )

fig.update_layout(
    title="COVID-19 Interactive Dashboard",
    title_x=0.5,
    xaxis_title="State",
    yaxis_title="Total Cases",
    template="plotly_white",
    updatemenus=[
        dict(
            buttons=buttons,
            direction="down",
            showactive=True,
            x=0.02,
            y=1.15,
            xanchor="left",
            yanchor="top"
        )
    ]
)

fig.write_html("dashboard.html")

print("Dashboard saved as dashboard.html")

fig.show()
