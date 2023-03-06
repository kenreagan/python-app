from flask import Blueprint, request, render_template, request
from src.connector import DatabaseContext
import pandas as pd
from src.utils import DatabaseTableMixin
from src.models import EarthQuakes
from sqlalchemy import and_

app_routes = Blueprint("views", __name__)

@app_routes.route('/')
def home():
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    location = request.args.get("location")

    if location:
        with DatabaseContext() as context:
           dataObj = context.session.query(EarthQuakes).filter(EarthQuakes.place.contains(location)).all()
    elif longitude:
        with DatabaseContext() as context:
            dataObj = context.session.query(EarthQuakes).filter(
                    and_(
                        EarthQuakes.latitude == latitude,
                        EarthQuakes.dmin <= 10
                    )
                ).all()
    elif latitude:
        with DatabaseContext() as context:
            dataObj = context.session.query(EarthQuakes).filter(
                    and_(
                        EarthQuakes.longitude == longitude,
                        EarthQuakes.dmin <= 10
                        )
                    ).all()
    elif latitude and longitude:
        with DatabaseContext() as context:
            dataObj = context.session.query(EarthQuakes).filter(
                        and_(
                            EarthQuakes.latitude == latitude,
                            EarthQuakes.longitude == longitude,
                            EarthQuakes.dmin <= 10
                        )
                    ).all()
    else:
        with DatabaseContext() as context:
            dataObj = context.session.query(EarthQuakes).filter_by().all()
    
    resDetails = {
            "records": [
                item.to_json() for item in iter(dataObj)
            ]
        }

    dataFrame = pd.DataFrame(resDetails["records"])
    dataFrame = dataFrame.sample(frac=1, random_state=1).reset_index()

    data = dataFrame.iloc[:1000, :]
    return render_template("index.html", data=data)


