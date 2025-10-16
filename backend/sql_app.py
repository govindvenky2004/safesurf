from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuring the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///safesurf.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class PhishingData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(2083), nullable=False)

    def __repr__(self):
        return f"<PhishingData {self.email}, {self.url}>"

# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')  # Ensure your HTML file is in the 'templates' folder

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form.get('email')
    url = request.form.get('url')
    
    # Validate inputs
    if email and url:
        # Save to the database
        data = PhishingData(email=email, url=url)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return "Error: Both email and URL are required", 400

if __name__ == "__main__":
    app.run(debug=True)
