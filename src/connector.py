from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from src.models import Base
import pandas as pd
from sqlalchemy import DateTime, String, Float

load_dotenv(
        os.path.join(
                os.path.abspath(
                        os.path.dirname(
                                __file__
                            )
                    ),
                "config.env"
            )
    )


Base.metadata.create_all(
    create_engine(
        f'sqlite:///earthquake.sqlite'
    )
)


def create_all():
    df = pd.read_csv('all_month.csv')
    df.head(5)
    df.isna().mean()*100
    df = df.fillna(df.median())

    df['time'] = pd.to_datetime(df['time'])
    df['updated'] = pd.to_datetime(df['updated'])

    connection_engine = create_engine("sqlite:///earthquake.sqlite")

    connection = connection_engine.raw_connection()
    dtypes= {
            "id": String(150),
            "time": DateTime,
            "lattitude": Float,
            "longitude": Float,
            "depth": Float,
            "mag": Float,
            "magType": Float,
            "nst": Float,
            "gap": Float,
            "dmin": Float,
            "rms": Float,
            "net": String(20),
            "updated": DateTime,
            "place": String(250),
            "type": String(100),
            "horizontalError": Float,
            "depthError": Float,
            "magError": Float,
            "magNst": Float,
            "status": String(100),
            "locationSquare": String(100),
            "magSource": String(100),
            }
    print(df.head())
    df.to_sql(
                "earthquake", connection, if_exists="append"
            )
    
class DatabaseContext:
    def __init__(self):
        self.engine = create_engine("sqlite:///earthquake.sqlite")
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)

    def __enter__(self):
        self.session = self.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
            self.session.close()
        self.session.close()

    def commit(self):
        self.session.commit()
