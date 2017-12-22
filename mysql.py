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
    __table__ = Table('trains', metadata, autoload=True)

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
   return session.query(Stations).filter(Stations.station_name == station_name).first().station_id

def find_segment_fare(segment_id):
    return session.query(Segments).filter(Segments.segment_id == segment_id).first().seg_fare

def find_fare_adjustment(fare_type):
    return session.query(Fare_Types).filter(Fare_Types.fare_type == fare_type).first().fare_rate

def segment_list(station_n, station_s):
    # Create a list of segments
    segments = []
    if station_n < station_s:
        for i in range(station_n, station_s):
            segments += [i]
    else:
        for i in range(station_s, station_n):
            segments += [i]
    return segments

def find_full_fare(list_of_segs, list_of_pass):
    rate = 0
    fare = 0
    for i, inst in enumerate(session.query(Fare_Types).filter(True)):
        rate += list_of_pass[i] * inst.fare_rate
    for seg in list_of_segs:
        trip_seg = session.query(Segments).filter(Segments.segment_id == seg)
        fare += trip_seg.first().seg_fare
    fare *= rate
    return fare


def find_trains(station_start, station_end, passengers, day):
    station_start_id = find_station(station_start)
    station_end_id = find_station(station_end)
    num_passengers = sum(passengers)
    segments = segment_list(station_start_id, station_end_id)
    fare = find_full_fare(segments, passengers)
    trip_direction = 0 if station_start_id < station_end_id else 1
    trains_free = {}
    # print(station_start,", ", station_end, ": ", segments)
    for instance in session.query(Trains).filter(Trains.train_direction == trip_direction):
        trains_free[instance.train_id] = True
        for seg in segments:
            seats = session.query(Seats_Free).filter(Seats_Free.train_id == instance.train_id
                                                    and Seats_Free.seat_free_date == day
                                                    and Seats_Free.segment_id == seg).first().freeseat
            if seats < num_passengers:
                trains_free[instance.train_id] = False
    # print("Trains: ", trains_free)
    # print("Fare: ", fare)
    trains_free["fare"] = fare
    return trains_free

first = find_trains('Boston, MA - South Station', 'Washington, DC - Union Station', [5,0,0,0,0], '2018-06-01')
second = find_trains('Wilmington, DE - J.R. Biden, Jr. Station', 'Boston, MA - South Station',  [0,100,100,100,100], '2017-12-30')

for key, value in first.items():
    if(key != 'fare'):
        print("Train ",key,": ",value)
    else:
        print("Full Fare: ", value)