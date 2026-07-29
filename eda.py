import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
import snowflake.connector
import pandas as pd

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

df = pd.read_sql_query(query, conn)

plt.figure(figsize=(10,5))
plt.bar(df["STATE"], df["TOTAL_CASES"])
plt.xticks(rotation=45)
plt.title("Top 10 States by COVID-19 Cases")
plt.xlabel("State")
plt.ylabel("Total Cases")
plt.tight_layout()

plt.savefig("top10_states_cases.png")
plt.show()

print(df.head())

print("\nDataset information")
print(df.info())

print("\nMissing values")
print(df.isnull().sum())

print("\nStatistics")
print(df.describe())

conn.close()
