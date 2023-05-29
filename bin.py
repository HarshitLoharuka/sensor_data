import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from aiohttp import web
from datetime import datetime, timedelta

Base = declarative_base()


class WeatherData(Base):
    __tablename__ = 'weather_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sensor_id = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


engine = db.create_engine('postgresql://root:password@localhost/weather_db_name')
Session = sessionmaker(bind=engine)


async def add_data(request):
    try:
        data = await request.json()
        sensor_id = data.get('sensor_id')
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        wind_speed = data.get('wind_speed')

        if not sensor_id or not temperature or not humidity or not wind_speed:
            return web.json_response({'error': 'Incomplete data'}, status=400)

        async with Session() as session:
            weather_data = WeatherData(
                sensor_id=sensor_id,
                temperature=temperature,
                humidity=humidity,
                wind_speed=wind_speed
            )
            session.add(weather_data)
            session.commit()

        return web.json_response({'message': 'Data added successfully'}, status=201)
    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)


async def query_data(request):
    try:
        sensor_id = request.query.get('sensor_id')
        metrics = request.query.get('metrics')
        statistic = request.query.get('statistic')
        start_date = request.query.get('start_date')
        end_date = request.query.get('end_date')

        if not sensor_id or not metrics or not statistic:
            return web.json_response({'error': 'Incomplete query parameters'}, status=400)

        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')

        if not end_date:
            end_date = datetime.utcnow()
        else:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        async with Session() as session:
            query = session.query()
            for metric in metrics.split(','):
                column = getattr(WeatherData, metric)
                aggregation_func = getattr(db.func, statistic)(column).label(metric)
                query = query.add_columns(aggregation_func)

            query = query.filter(WeatherData.sensor_id == sensor_id,
                                 WeatherData.timestamp >= start_date,
                                 WeatherData.timestamp <= end_date)

            result = query.first()

            if not result:
                return web.json_response({'error': 'No data found'}, status=404)

            result_dict = {}
            metrics_list = metrics.split(',')
            for i in range(len(metrics_list)):
                result_dict[metrics_list[i]] = result[i]

            return web.json_response({'result': result_dict}, status=200)
    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)


app = web.Application()
app.router.add_post('/api/add-data', add_data)
app.router.add_get('/api/query-data', query_data)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    web.run_app(app)
