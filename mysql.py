from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import pymysql
pymysql.install_as_MySQLdb()

engine = create_engine('mysql://root@localhost/F17336Pteam6')
engine.execute("USE F17336Pteam6")

Base = declarative_base()
metadata = MetaData(bind=engine)

class Fare_Types(Base):
    __table__ = Table('fare_types', metadata, autoload=True)

class Passengers(Base):
    __table__ = Table('passengers', metadata, autoload=True)

class Reservations(Base):
    __table__ = Table('reservations', metadata, autoload=True)

class Seats_Free(Base):
    __table__ = Table('seats_free', metadata, autoload=True)

class Segments(Base):
    __table__ = Table('segments', metadata, autoload=True)

class Stations(Base):
    __table__ = Table('stations', metadata, autoload=True)

class Stops_At(Base):
    __table__ = Table('stops_at', metadata, autoload=True)

class Trains(Base):
    __table__ = Table('stations', metadata, autoload=True)

class Trips(Base):
    __table__ = Table('stations', metadata, autoload=True)

Session = sessionmaker(bind=engine)
session = Session()

def find_or_create_passenger(email, first_name, last_name):
    passenger_id = -1
    for instance in session.query(Passengers):
        if instance.passenger_email == email:
            passenger_id = instance.passenger_id

    if passenger_id == -1:
        passenger = Passengers(passenger_email = email, passenger_fname = first_name, passenger_lname = last_name)
        passenger_id = passenger.passenger_id
        session.add(passenger)
        session.commit()
    return(passenger_id)

def find_station(station_name):
    for instance in session.query(Stations):
        if instance.station_name == station_name:
            return instance.station_id

def find_segment_fare(segment_id):
    return session.query(Segments).filter(Segments.segment_id == segment_id).first().seg_fare

def find_fare_adjustment(fare_type):
    return session.query(Fare_Types).filter(Fare_Types.fare_type == fare_type).first().fare_rate

def find_trains(station_start, station_end, passengers, day):
    station_start_id = find_station(station_start)
    station_end_id = find_station(station_end)
    num_passengers = sum(passengers)
    trip_direction = 0 if station_start_id < station_end_id else 1

    for instance in session.query(Trains).filter(Train.train_direction = trip_direction):
        pass
        # TODO: Finish this function (stopped to push progress)
