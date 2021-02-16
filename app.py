import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
from datetime import datetime, timedelta 

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite",connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0/start_date(eg.2016-08-23)<br/>"
        f"/api/v1.0/start_date(eg.2016-08-23)/end_date(eg.2017-08-23)"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
   

    """Return a list of dates and precipitation"""
    # Query all measurements
    results = session.query(Measurement.date,Measurement.prcp).all()

    dictionary = dict(results)

    return jsonify(dictionary )
   

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
   

    """Return a list of stations"""
    # Query all measurements
    results = session.query(Station.station).all()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)  
    

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    

    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    # print(type(max_date))
    last_year = (datetime.strptime(max_date[0], '%Y-%m-%d') - timedelta(days=365)).strftime('%Y-%m-%d')
    last_year_temp = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= last_year, Measurement.station == 'USC00519281').\
         order_by(Measurement.tobs).all()

    temp = []
    for date, tobs in last_year_temp:
        prev_year_temp = {}
        prev_year_temp["date"] = date
        prev_year_temp["tobs"] = tobs
        temp.append(prev_year_temp)

    return jsonify(temp)
    session.close()

@app.route("/api/v1.0/<start>")    
def start_date(start):
    # Create our session (link) from Python to the DB
   

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    temp= list(np.ravel(results ))

    min_temp = temp[0]
    max_temp = temp[1]
    avg_temp = temp[2]
    temp_dict = {'Min temp': min_temp, 'Max temp': max_temp, 'Avg temp': avg_temp}

    return jsonify(temp_dict)
    session.close()


@app.route("/api/v1.0/<start>/<end>")    
def start_end_date(start,end):
    # Create our session (link) from Python to the DB
    

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    temp= list(np.ravel(results ))

    min_temp = temp[0]
    max_temp = temp[1]
    avg_temp = temp[2]
    temp_dict = {'Min temp': min_temp, 'Max temp': max_temp, 'Avg temp': avg_temp}

    return jsonify(temp_dict)                 
    
if __name__ == '__main__':
    app.run(debug=True)
