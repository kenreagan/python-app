from flask import Blueprint, request, render_template, request
from src.connector import DatabaseContext
import pandas as pd
from src.utils import DatabaseTableMixin
from src.models import EarthQuakes
from sqlalchemy import and_
import time
import redis

app_routes = Blueprint("views", __name__)

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

r = redis.Redis(connection_pool=pool)

@app_routes.route('/')
def home():
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    location = request.args.get("location")

    if location:
        # Check if the object exists in the Cache
        if 'location' in r:
            start_longitude_cache = time.time()
            dataObj = r.get("location")
            end_longitude_cache = time.time()

            print(f"Time taken for Cache: {end_longitude_cache - start_longitude_cache}s")
        else:
            with DatabaseContext() as context:
                start_time = time.time()
                dataObj = context.session.query(
                        EarthQuakes
                    ).filter(
                        EarthQuakes.place.contains(
                            location
                        )
                    ).all()

                end_time = time.time()
                print(f"Time taken for Qeury: {endtime-startime}s")

                # add the results objects to Cache
                r.set("location", dataObj)

    elif longitude:
        # Check if the object exists in the Cache
        if 'longitude' in r:
            start_longitude_cache = time.time()
            dataObj = r.get("longitude")
            end_longitude_cache = time.time()

            print(f"Time taken for Cache: {end_longitude_cache - start_longitude_cache}s")
        else:
            with DatabaseContext() as context:
                start_time = time.time()
                dataObj = context.session.query(EarthQuakes).filter(
                        and_(
                            EarthQuakes.longitude == longitude,
                            EarthQuakes.dmin <= 10
                        )
                    ).all()
                end_time = time.time()

                print(f"Time taken for query: {end_time - start_time}}s")
                # add the results objects to Cache
                r.set("longitude", dataObj)

    elif latitude:
        # Check if item exists in the Cache
        if 'longitude' in r:
            start_longitude_cache = time.time()
            dataObj = r.get("longitude")
            end_longitude_cache = time.time()

            print(f"Time taken for Cache: {end_longitude_cache - start_longitude_cache}s")
        else:
            start_time = time.time()
            with DatabaseContext() as context:
                dataObj = context.session.query(EarthQuakes).filter(
                        and_(
                            EarthQuakes.latitude == latitude,
                            EarthQuakes.dmin <= 10
                            )
                        ).all()
                end_time = time.time()
                print(f"Time taken for query: {end_time - start_time}s")
                # add the results objects to Cache
    elif latitude and longitude:
        # Check if item exists in the Cache
        if 'longitude' in r and 'latitude' in r:
            start_longitude_cache = time.time()
            longObj = r.get("longitude")
            latObj = r.get("latitude")

            dataObj = longObj + latObj

            end_longitude_cache = time.time()

            print(f"Time taken for cache: {end_longitude_cache - start_longitude_cache}s")
        else:
            start_time = time.time()
            with DatabaseContext() as context:
                dataObj = context.session.query(EarthQuakes).filter(
                            and_(
                                EarthQuakes.latitude == latitude,
                                EarthQuakes.longitude == longitude,
                                EarthQuakes.dmin <= 10
                            )
                        ).all()
                end_time = time.time()

                print(f"Time taken for query: {end_time - start_time}s")
                # add the results objects to Cache
    else:
        with DatabaseContext() as context:
            dataObj = context.session.query(EarthQuakes).filter_by().all()
            # add the results objects to Cache
    
    resDetails = {
            "records": [
                item.to_json() for item in iter(dataObj)
            ]
        }

    dataFrame = pd.DataFrame(resDetails["records"])
    dataFrame = dataFrame.sample(frac=1, random_state=1).reset_index()

    data = dataFrame.iloc[:1000, :]
    return render_template("index.html", data=data)


