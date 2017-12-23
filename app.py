from flask import Flask, render_template, session, redirect, url_for, flash, request
from forms import GetTrainsForm, ReservationForm, GetReservationsForm, CancelReservationForm
from mysql import *
import os

app = Flask(__name__)
app.secret_key = 'csc336railroad'

@app.route('/', methods=['GET'])
def index():
    form = GetTrainsForm()
    return render_template('index.html', form=form)

@app.route('/search', methods=['GET'])
def search():
    form = GetTrainsForm()

    date = request.args.get('date', default=None, type=str)

    if date:
        date = date.split('-')
        date_year = int(date[0])
        date_month = int(date[1])
        date_day = int(date[2])
    else:
        date_year = None
        date_month = None
        date_day = None

    station_start = request.args.get('station_start', default=None, type=int)
    station_end = request.args.get('station_end', default=None, type=int)
    num_adult = request.args.get('num_adult', default=0, type=int)
    num_child = request.args.get('num_child', default=0, type=int)
    num_senior = request.args.get('num_senior', default=0, type=int)
    num_military = request.args.get('num_military', default=0, type=int)
    num_pets = request.args.get('num_pets', default=0, type=int)

    # print(date_year, date_month, date_day, station_start, station_end, num_adult, num_child, num_senior, num_military, num_pets)

	# Get available trains
    passengers = [num_adult, num_child, num_senior, num_military, num_pets]
    trains = find_trains(station_start, station_end, passengers, date)
    print(trains)

    train_results = [(train_id, find_station_name(station_start), find_station_name(station_end), '', '', trains[1]) for train_id in trains[0]]
    print(train_results)
    # if there are no trains available after filtering the database
    # do this:
    if not len(train_results):
        return render_template('notrainsavailable.html')

    return render_template('index.html', form=form, results=train_results)

# in case a user somehow finds themselves at this route, redirect to index
@app.route('/reservations/', methods=['GET'])
def reservation():
    form = GetTrainsForm()
    return redirect(url_for('index', form=form))

@app.route('/reservations/create', methods=['GET', 'POST'])
def make_reservation(train_id=None):
    form = ReservationForm()

    if request.method == 'GET':
        return render_template('makereservation.html', form=form)
    elif request.method == 'POST':
        if form.validate():
            # add this reservation to the database and update accordingly
            # sqlalchemy stuff goes here

            message = 'The reservation has been made successfully!'
            return render_template('success.html', message=message)
        else:
            return render_template('makereservation.html', form=form)

@app.route('/reservations/success')
def success(message):
    return render_template('success.html', message=message)

@app.route('/reservations/rebook')
def rebook_reservation():
    return render_template('rebookreservation.html')

@app.route('/reservations/cancel', methods=['GET', 'POST'])
def cancel_reservation(email=None, reservations=None, reservation_id=None):
    form = GetReservationsForm()
    form2 = CancelReservationForm()

    if request.method == 'GET':
        return render_template('getreservations.html', form=form)
    elif request.method == 'POST':
        reservation_id = request.args.get('reservation_id', default=None, type=int)

        if reservation_id is not None:
            # query the database for the reservation given by
            # this reservation id
            # cancel the reservation

            message = 'The reservation has been cancelled. We will refund you shortly.'
            return render_template('success.html', message=message)

        elif form.validate():
            # query the database for any reservations for this person

            # replace reservations with something useful
            # i just used this for testing
            reservations = [1, 2, 4]

            return render_template('cancelreservation.html',
                                   form2=form2,
                                   email=form.email.data,
                                   reservations=reservations)
        else:
            return render_template('getreservations.html', form=form)

# Run Flask web server
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
