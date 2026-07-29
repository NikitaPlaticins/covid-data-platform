import os
from dotenv import load_dotenv
import snowflake.connector
import pandas as pd
import plotly.express as px

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
    SUM(CASES) AS TOTAL_CASES
FROM NYT_US_COVID19
GROUP BY STATE
ORDER BY TOTAL_CASES DESC
LIMIT 10;
"""

cursor = conn.cursor()
cursor.execute(query)

rows = cursor.fetchall()
columns = [col[0] for col in cursor.description]

df = pd.DataFrame(rows, columns=columns)

cursor.close()
conn.close()

fig = px.bar(
    df,
    x="STATE",
    y="TOTAL_CASES",
    title="Top 10 States by COVID-19 Cases",
    labels={
        "STATE": "State",
        "TOTAL_CASES": "Total Cases"
    }
)

fig.write_html("dashboard.html")
fig.show()
