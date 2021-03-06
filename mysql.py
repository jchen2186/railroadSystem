from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import datetime

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
    parent = relationship("Trips", backref = backref("Reservations", cascade = "all, delete"))

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
   return session.query(Stations).filter(Stations.station_name == station_name).first().station_id

def find_station_name(station_id):
   return session.query(Stations).filter(Stations.station_id == station_id).first().station_name

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
    return fare * rate


def find_trains(station_start, station_end, passengers, day):
    # station_start_id = find_station(station_start)
    # station_end_id = find_station(station_end)
    station_start_id = int(station_start)
    station_end_id = int(station_end)
    num_passengers = sum(passengers)
    segments = segment_list(station_start_id, station_end_id)
    fare = find_full_fare(segments, passengers)
    trip_direction = 0 if station_start_id < station_end_id else 1
    trains_free = {}
    # print(station_start,", ", station_end, ": ", segments)
    weekdays = datetime.datetime.strptime(day, '%Y-%m-%d').date().weekday()
    if weekdays < 5:
        weekdays = 1
    else:
        weekdays = 0
    for instance in session.query(Trains).filter(Trains.train_direction == trip_direction).filter(Trains.train_days == weekdays):
        trains_free[instance.train_id] = 500
        for seg in segments:
            seats = session.query(Seats_Free).filter(Seats_Free.train_id == instance.train_id).filter(Seats_Free.seat_free_date == day).filter(Seats_Free.segment_id == seg).first().freeseat
            if seats < num_passengers:
                trains_free[instance.train_id] = 0
            else:
                if(seats < trains_free[instance.train_id]):
                    trains_free[instance.train_id] = seats
    return [trains_free, fare, day]

######## helper function
def get_station_train_deprture(train_id, station_id):
    return session.query(Stops_At).filter(Stops_At.train_id == train_id, Stops_At.station_id == station_id).first().time_out

def get_station_train_arrival(train_id, station_id):
    return session.query(Stops_At).filter(Stops_At.train_id == train_id, Stops_At.station_id == station_id).first().time_in

def increase_seat_free(train_id, start_seg_id, end_seg_id, seat_free_date):
    # per-con: there are at least one seat in every segment
    for seg_id in range(start_seg_id, end_seg_id + 1):
        # get segment
        seg = session.query(Seats_Free).filter(Seats_Free.train_id == train_id, Seats_Free.segment_id == seg_id, Seats_Free.seat_free_date == seat_free_date).first()
        # update free seats number
        seg.freeseat = seg.freeseat + 1
        session.commit()

def decrease_seat_free(train_id, start_seg_id, end_seg_id, seat_free_date):
    # per-con: there are at least one seat in every segment
    for seg_id in range(start_seg_id, end_seg_id + 1):
        # get segment
        seg = session.query(Seats_Free).filter(Seats_Free.train_id == train_id, Seats_Free.segment_id == seg_id, Seats_Free.seat_free_date == seat_free_date).first()
        # update free seats number
        seg.freeseat = seg.freeseat - 1
    # commit
    session.commit()

######## cancel reservation.

# return a list of list, in each inner list, there are reservation_id,
# trip.data, trip_train_id and fare
def get_my_trips(email):
    try:
        id = session.query(Passengers).filter(Passengers.email == email).first().passenger_id
    except AttributeError:
        #return False if user not exist.
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
        time = session.query(Stops_At).filter(Stops_At.train_id == trip.trip_train_id,
                             Stops_At.station_id == station_start_id).first().time_in

        list = [trip.reservation_id, trip.trip_train_id, station_start_name, station_end_name, str(time), str(trip.fare)]

        all_trip.append(list)

    return all_trip


def cancel_res(reservation_id):
    # get trip and reservation
    trip = session.query(Trips).filter(Trips.reservation_id == reservation_id).first()
    reservation = session.query(Reservations).filter(Reservations.reservation_id == reservation_id).first()

    # calculate train direction
    if trip.trip_seg_start < trip.trip_seg_ends:
        # going north
        station_start_id = trip.trip_seg_start
        station_end_id = trip.trip_seg_ends + 1
    else:
        #going south
        station_start_id = trip.trip_seg_start + 1
        station_end_id = trip.trip_seg_ends

    # increase seat_free
    increase_seat_free(trip.trip_train_id, station_start_id, station_end_id, trip.trip_date)
    # delete
    session.delete(reservation)
    session.delete(trip)
    # commit
    session.commit()

if __name__ == "__main__":
    first = find_trains(1,25,[5,0,0,0,0], "2018-06-01")
    second = find_trains(20,1, [0,100,100,100,100], '2017-12-30')

    print(first)
    print(second)
