from flask import Flask, render_template, session, redirect, url_for, flash
from forms import GetTrainsForm
import os

app = Flask(__name__)
app.secret_key = 'csc336railroad'

@app.route('/', methods=['GET'])
def index():
    form = GetTrainsForm()
    return render_template('index.html', form=form)

@app.route('/reservations', methods=['GET'])
def reservations():
    return render_template('viewavailableseats.html')

@app.route('/reservations/create')
def make_reservation():
    return render_template('makereservation.html')

@app.route('/reservations/cancel')
def cancel_reservation():
    return render_template('cancelreservation.html')

# Run Flask web server
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
