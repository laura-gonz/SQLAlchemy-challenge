# Import the dependencies.

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session 
from sqlalchemy import create_engine, func, inspect 
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

# import requests 

#################################################
# Database Setup
#################################################

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

   
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).all()

    session.close()

    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    session.close()

    results = list(np.ravel(results))

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    latest_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= latest_year).all()

    session.close()
    
    results = list(np.ravel(results))

    return jsonify(results)

@app.route("/api/v1.0/<start>")
def tobs():
    session = Session(engine)

    latest_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= latest_year).all()

    session.close()
    
    results = list(np.ravel(results))

    return jsonify(results)

# # Create a dictionary from the row data and append to a list of all_passengers
    # all_passengers = []
    # for name, age, sex in results:
    #     passenger_dict = {}
    #     passenger_dict["name"] = name
    #     passenger_dict["age"] = age
    #     passenger_dict["sex"] = sex
    #     all_passengers.append(passenger_dict)

if __name__ == '__main__':
    app.run(debug=True)

