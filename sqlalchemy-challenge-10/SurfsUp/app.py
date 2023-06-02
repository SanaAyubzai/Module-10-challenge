# Import the dependencies.

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")

def welcome():
    return (
        f"Use this app to check out the Climate in Hawaii.  Surf's Up! <br/>"    
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/tobs_pastyear_most-active-station  <br/>"
        f"/api/v1.0/start <br/>"
        f"/api/v1.0/end <br/>"
        f"/api/v1.0/start/end"
    )

# Convert query results from the precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp (precipitation) as the value.
# Create our session (link) from Python to the DB

# This ia a route definition in in Flask to return preciitation from the last year from the dataset.
@app.route("/api/v1.0/precipitation")

def precipitation():
    session = Session(engine)
    prior_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prior_year).all()
    session.close()

    precip = {date: prcp for date, prcp in precipitation}

    return jsonify(precip)
 
# This ia a route definition in in Flask to return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")

def station():
    session = Session(engine)
    distinct_stations = session.query(Measurement.station).distinct().all()
    session.close()
    stations = list(np.ravel(distinct_stations))
    return jsonify(stations=stations)

# This ia a route definition in in Flask to return temperature observations from the last year from the dataset.

@app.route("/api/v1.0/tobs")

def tobs():
    session = Session(engine)
    distinct_tobs = session.query(Measurement.tobs).distinct().all()
    session.close()
    tobs = list(np.ravel(distinct_tobs))
    return jsonify(tobs)


# This ia a route definition in in Flask to return temperature observations from the last year from the dataset.

@app.route("/api/v1.0/tobs_pastyear_most-active-station")


def tobs_pastyear_most_activestation():
    session = Session(engine)

    # Define the prior year date range
    prior_year_start = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prior_year_end = dt.date(2017, 8, 23)
    
    # Query the most active station
    most_active_station = "USC00519281"

    # Query the dates and temperature observations for the most active station within the prior year
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= prior_year_start).\
        filter(Measurement.date <= prior_year_end).all()

    # Create a list of dictionaries to store the results
    observations = []
    for date, tobs in results:
        observation = {
            'date': date,
            'tobs': tobs
        }
        observations.append(observation)

    return jsonify(observations)


if __name__ == "__main__":
    app.run(debug=True)
