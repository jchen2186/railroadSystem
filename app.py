from flask import Flask, render_template, session, redirect, url_for, flash, request
from forms import GetTrainsForm
import os

app = Flask(__name__)
app.secret_key = 'csc336railroad'

@app.route('/', methods=['GET'])
def index():
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

    print(date_year, date_month, date_day, station_start, station_end, num_adult, num_child, num_senior, num_military, num_pets)
    return render_template('index.html', form=form)

# in case a user somehow finds themselves at this route, redirect to index
@app.route('/reservation', methods=['GET'])
def reservation():
    form = GetTrainsForm()
    return redirect(url_for('index', form=form))

@app.route('/reservations/create')
def make_reservation():
    return render_template('makereservation.html')

@app.route('/reservations/rebook')
def rebook_reservation():
    return render_template('rebookreservation.html')

@app.route('/reservations/cancel')
def cancel_reservation():
    return render_template('cancelreservation.html')

# Run Flask web server
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
