# Importing the modules
# Render_template renders HTML, request handles form data
# Redirect and url_for direct users to a route in the website navigation
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a new Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sleep_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define SleepRecord Model class
# Define the columns (attributes) for the class
class SleepRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each record
    date = db.Column(db.String(20), nullable=False)  # Date of sleep entry
    sleep_duration = db.Column(db.Float, nullable=False)  # Duration of sleep in hours
    sleep_quality = db.Column(db.String(20), nullable=False)  # Quality of sleep (e.g., Good, Average, Poor)
    wakeup_time = db.Column(db.String(10), nullable=False)  # Time the user woke up (HH:MM format)
    completed = db.Column(db.Boolean, default=False)  # Track if record is "complete"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of record creation
    
    # Add the repr method
    # This is a special Python method that returns a string representing the object
    def __repr__(self):
        return f'<SleepRecord id={self.id} date={self.date} sleep_duration={self.sleep_duration} sleep_quality={self.sleep_quality} wakeup_time={self.wakeup_time} created_at={self.created_at}>'

# Create the database and table to hold sleep records
with app.app_context():
    db.create_all()

# Create a home route that displays sleep records
@app.route('/')
def index():
    records = SleepRecord.query.order_by(SleepRecord.date.desc()).all()
    return render_template('index.html', records=records)

# Create a route for adding a new sleep record to the database
@app.route('/add', methods=['POST'])
def add():
    date = request.form.get('date')
    sleep_duration = request.form.get('sleep_duration')
    sleep_quality = request.form.get('sleep_quality')
    wakeup_time = request.form.get('wakeup_time')
    
    if date and sleep_duration and sleep_quality and wakeup_time:
        new_record = SleepRecord(date=date, sleep_duration=float(sleep_duration), sleep_quality=sleep_quality, wakeup_time=wakeup_time)
        db.session.add(new_record)
        db.session.commit()
    return redirect(url_for('index'))

# Create a route to delete a sleep record
@app.route('/delete/<int:record_id>')
def delete(record_id):
    record = SleepRecord.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('index'))

# Route to toggle completion status
@app.route('/toggle/<int:record_id>')
def toggle(record_id):
    record = SleepRecord.query.get_or_404(record_id)
    record.completed = not record.completed  # Flip the boolean
    db.session.commit()
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
