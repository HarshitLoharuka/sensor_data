# Weather Data API

This is a simple API for adding and querying weather data using Python and SQLAlchemy.

## Requirements

- Python 3.6 or above
- PostgreSQL database

## Installation

1. Clone the repository:

git@github.com:HarshitLoharuka/sensor_data.git


2. Install the dependencies:

sqlalchemy
aiohttp
psycopg2-binary


3. Set up the database:

- Create a PostgreSQL database for storing the weather data.
- Update the database connection string in the code (`engine = db.create_engine('postgresql://root:password@localhost/weather_db_name')`) with your actual database credentials and database name.

4. Run the application:

python bin.py


The API server will start running on `http://localhost:8080`.

To add weather data, send a POST request to the following endpoint:

POST /api/add-data

The request body should be a JSON object with the following properties:

{
  "sensor_id": 1,
  "temperature": 25.5,
  "humidity": 60.2,
  "wind_speed": 12.3
}

All properties are required. If the request is successful, you will receive a JSON response with a success message.


To query weather data, send a GET request to the following endpoint:

GET /api/query-data?sensor_id=1&metrics=temperature,humidity&statistic=avg

The query parameters are as follows:

sensor_id: The ID of the sensor to query data for (required).
metrics: Comma-separated list of metrics to retrieve (e.g., temperature,humidity) (required).
statistic: The type of aggregation to perform on the metrics (e.g., avg, min, max) (required).
start_date (optional): The start date for the data range (format: YYYY-MM-DD). If not provided, it defaults to 30 days ago.
end_date (optional): The end date for the data range (format: YYYY-MM-DD). If not provided, it defaults to the current date.

If the query is successful and data is found, you will receive a JSON response with the queried data.



