from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import pymysql
pymysql.install_as_MySQLdb()

engine = create_engine('mysql://root@localhost/railroad1')
engine.execute("USE railroad1")

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
    __table__ = Table('trips', metadata, autoload=True)

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

#def find_trains(station_start, station_end, passengers, day):
#    station_start_id = find_station(station_start)
#    station_end_id = find_station(station_end)
#    num_passengers = sum(passengers)
#    trip_direction = 0 if station_start_id < station_end_id else 1

#    for instance in session.query(Trains).filter(Train.train_direction = trip_direction):
#        pass
        # TODO: Finish this function (stopped to push progress)

######## helper function
def get_station_train_deprture(train_id, station_id):
    return session.query(Stops_At).filter(Stops_At.train_id == train_id and Stops_At.station_id == station_id).first().time_out

def get_station_train_arrival(train_id, station_id):
    return session.query(Stops_At).filter(Stops_At.train_id == train_id and Stops_At.station_id == station_id).first().time_in

######## cancel reservation.

# return a list of list, in each inner list, there are reservation_id,
# trip.data, trip_train_id and fare
def get_my_trips(email):
    try:
        id = session.query(Passengers).filter(Passengers.email == email).first().passenger_id
    except AttributeError:
        #return false if user not exist.
        return False

    # get all my reservations
    reservations = session.query(Reservations).filter(Reservations.paying_passenger_id == id)

    all_trip = []

    for res in reservations:
        trip = session.query(Trips).filter(Trips.reservation_id == res.reservation_id).first()
        # calculate train direction
        if trip.trip_seg_start < trip.trip_seg_ends:
            # going north
            station_start_id = trip.trip_seg_start
            station_end_id = trip.trip_seg_ends + 1
        else:
            #going south
            station_start_id = trip.trip_seg_start + 1
            station_end_id = trip.trip_seg_ends
        # get the name of stations
        station_start_name = session.query(Stations).filter(Stations.station_id == station_start_id).first().station_name
        station_end_name = session.query(Stations).filter(Stations.station_id == station_end_id).first().station_name

        # get arrival time
        time = session.query(Stops_At).filter(Stops_At.train_id == trip.trip_train_id and
                             Stops_At.station_id == station_start_id).first().time_in

        list = [trip.reservation_id, trip.trip_train_id, station_start_name, station_end_name, str(time), str(trip.fare)]

        all_trip.append(list)

    return all_trip


def cancel_res(reservation_id):
    # TODO: increase seat_free HOLD HOLD

    # delete trip first
    trip = session.query(Trips).filter(Trips.reservation_id == reservation_id).first()
    session.delete(trip)
    # delete reservation
    reservation = session.query(Reservations).filter(Reservations.reservation_id == reservation_id).first()
    session.delete(reservation)

    # commit
    session.commit()

print(get_station_train_arrival(1, 2))

