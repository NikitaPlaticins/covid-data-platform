# COVID-19 Data Integration and Analytics Platform

## Project Overview

This project was developed as part of the Modern Data Engineering Bootcamp.

The application integrates COVID-19 data from Snowflake with annotation data stored in MongoDB Atlas. A FastAPI REST API provides access to the data, while Plotly is used to generate interactive dashboards and data visualizations. Basic forecasting is implemented using Linear Regression from Scikit-learn.

## Technologies

- Snowflake
- MongoDB Atlas
- FastAPI
- Python
- Plotly
- Pandas
- NumPy
- Scikit-learn

## Project Structure

```
covid_project/
│
├── app/
│   ├── main.py
│   ├── mongodb.py
│   ├── snowflake_db.py
│   ├── models.py
│   └── config.py
│
├── dashboard.py
├── forecast.py
├── dashboard.html
├── forecast.html
├── requirements.txt
├── .env.example
├── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/NikitaPlaticins/covid-data-platform.git
cd covid-data-platform
```

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file using `.env.example` as a template.

Fill in:

- Snowflake credentials
- MongoDB connection string

## Running the API

```bash
uvicorn app.main:app --reload
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

## Dashboard

Generate dashboard:

```bash
python dashboard.py
```

## Forecast

Generate forecast:

```bash
python forecast.py
```

## Features

- Snowflake integration
- MongoDB integration
- REST API
- Interactive Swagger documentation
- Interactive Plotly dashboards
- COVID-19 data visualization
- Basic forecasting using Linear Regression

## Author

Nikita Platicins

Modern Data Engineering Bootcamp
