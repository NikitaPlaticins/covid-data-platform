import os
from dotenv import load_dotenv
import snowflake.connector
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

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
    DATE,
    SUM(CASES) AS TOTAL_CASES
FROM NYT_US_COVID19
GROUP BY DATE
ORDER BY DATE;
"""

cursor = conn.cursor()
cursor.execute(query)

rows = cursor.fetchall()
columns = [col[0] for col in cursor.description]

df = pd.DataFrame(rows, columns=columns)

cursor.close()
conn.close()

df["DATE"] = pd.to_datetime(df["DATE"])

df["DAY"] = np.arange(len(df))

X = df[["DAY"]]
y = df["TOTAL_CASES"]

model = LinearRegression()
model.fit(X, y)

future_days = np.arange(len(df), len(df) + 30)

future_predictions = model.predict(future_days.reshape(-1, 1))

future_dates = pd.date_range(
    start=df["DATE"].iloc[-1] + pd.Timedelta(days=1),
    periods=30
)

forecast = pd.DataFrame({
    "DATE": future_dates,
    "TOTAL_CASES": future_predictions
})

fig = px.line(
    df,
    x="DATE",
    y="TOTAL_CASES",
    title="COVID-19 Cases Over Time"
)

fig.add_scatter(
    x=forecast["DATE"],
    y=forecast["TOTAL_CASES"],
    mode="lines",
    name="Forecast"
)

fig.write_html("forecast.html")
fig.show()
