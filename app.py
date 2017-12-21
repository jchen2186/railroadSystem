from flask import Flask, render_template, session, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'csc336railroad'

@app.route('/', methods=['GET'])
def index():
	return render_template('example.html')

# Run Flask web server
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
