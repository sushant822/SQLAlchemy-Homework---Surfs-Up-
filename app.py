import numpy as np
import sqlalchemy
import datetime
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import timedelta
from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

#Home Page
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br"
        f"/api/v1.0/<start>/<end><br>")

choosen_date = "2017-04-22"

#Precipitation page
@app.route("/api/v1.0/precipitation")
def precipitation():
    precp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > choosen_date).all()

    precp_list = []
    for x in precp_data:
        precp_dict = {}
        precp_dict[x[0]] = x[1]
        precp_list.append(precp_dict)
    session.close()
    return jsonify(precp_list)

#Stations page
@app.route("/api/v1.0/stations")
def stations():
    station_data = session.query(Station).all()
    station_list = []
    for x in station_data:
        station_dict = {}
        station_dict['station'] = x.station
        station_dict['name'] = x.name
        station_dict['latitude'] = x.latitude
        station_dict['longitude'] = x.longitude
        station_dict['elevation'] = x.elevation
        station_list.append(station_dict)
    session.close()
    return jsonify(station_list)
    
station_count = (session.query(Measurement.station, func.count(Measurement.station))
                .group_by(Measurement.station)
                .order_by(func.count(Measurement.station).desc())
                .all())
station_highest = station_count[0][0]

#Temperature page
@app.route("/api/v1.0/tobs")
def temperature():
    temperature_station_data = session.query(Measurement.tobs).filter(Measurement.station == station_highest).filter(Measurement.date >= choosen_date).all()
    temperature_list = []
    for x in temperature_station_data:
        temperature_dict = {}
        temperature_dict['tobs'] = x.tobs
        temperature_list.append(temperature_dict)
    session.close()
    return jsonify(temperature_list)

#start_date page
@app.route("/api/v1.0/<start_date>")
def startdate(start_date):
    temperature_start_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    stat_sd = []
    for min_data, max_data, avg_data in temperature_start_data:
        stat_dict_sd = {}
        stat_dict_sd["Tmin"] = min_data
        stat_dict_sd["Tavg"] = avg_data
        stat_dict_sd["Tmax"] = max_data
        stat_sd.append(stat_dict_sd)
    session.close()
    return jsonify(stat_sd)

#start_date_end_date page
@app.route("/api/v1.0/<start_date>/<end_date>")
def enddate(start_date, end_date):
    temperature_end_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    stat_ed = []
    for min_data, max_data, avg_data in temperature_end_data:
        stat_dict_ed = {}
        stat_dict_ed["Tmin"] = min_data
        stat_dict_ed["Tavg"] = avg_data
        stat_dict_ed["Tmax"] = max_data
        stat_ed.append(stat_dict_ed)
    session.close()
    return jsonify(stat_ed)

if __name__ == '__main__':
    app.run(debug=True)