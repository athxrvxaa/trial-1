from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Student Credit Model
class StudentCredit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(20), nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    certificate = db.Column(db.String(255), nullable=True)
    date_uploaded = db.Column(db.DateTime, default=datetime.utcnow)

# Create the database
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        student_id = request.form.get('student_id')
        course_name = request.form.get('course_name')
        file = request.files['certificate']

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
        else:
            filename = None

        new_entry = StudentCredit(
            student_name=student_name,
            student_id=student_id,
            course_name=course_name,
            certificate=filename
        )
        db.session.add(new_entry)
        db.session.commit()

    # Retrieve all student credits from the database
    all_credits = StudentCredit.query.all()
    return render_template('index.html', all_credits=all_credits)

if __name__ == '__main__':
    app.run(debug=True)
