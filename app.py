from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, DecimalField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
import joblib
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_shush'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/rainfall.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

# FIXED: Handle encoder loading with error handling
try:
    encoder = joblib.load('encoder.pkl')
    print(f"Encoder classes: {getattr(encoder, 'classes_', 'Not fitted')}")
except:
    print("WARNING: Could not load encoder properly")
    encoder = None

# ... (keep all your existing classes and forms) ...

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(255), nullable = False, unique = True)
    password = db.Column(db.String(255), nullable = False)

class Predictions(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    input_data = db.Column(db.PickleType, nullable=False)
    predicted_output = db.Column(db.PickleType, nullable=False)

login_manager = LoginManager()
login_manager.init_app(app)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class RainfallCheck(FlaskForm):
    pressure = DecimalField('Pressure', validators = [InputRequired()])
    temparature = DecimalField('Average Temperature', validators = [InputRequired()])
    dewpoint = DecimalField('Dewpoint', validators = [InputRequired()])
    humidity = IntegerField('Humidity', validators = [InputRequired()])
    cloud = IntegerField('Cloud Cover', validators = [InputRequired()])
    sunshine = IntegerField('Sunshine', validators = [InputRequired()])
    winddirection = IntegerField('Wind Direction', validators = [InputRequired()])
    windspeed = DecimalField('Wind Speed', validators = [InputRequired()])
    submit = SubmitField('Predict Rainfall')

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/login', methods = ["GET", "POST"])
def login():
    user_form = LoginForm()
    if user_form.validate_on_submit():
        user = Users.query.filter_by(username = user_form.username.data).first()
        if user:
            if check_password_hash(user.password, user_form.password.data):
                login_user(user)
                flash("User logged in successfully")
                return redirect(url_for('dashboard'))
            else:
                flash("Login Unsuccessful! Check your username or password")
        else:
            hashed_pass = generate_password_hash(user_form.password.data)
            new_user = Users(username = user_form.username.data, password = hashed_pass)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash("User created successfully")
            return redirect(url_for('dashboard'))
    return render_template('login.html', form = user_form)

@app.route('/dashboard', methods = ["GET", "POST"])
@login_required
def dashboard():
    rain_form = RainfallCheck()
    prediction = None
    
    if rain_form.validate_on_submit():
        print("DEBUG: Form validation passed!")
        
        input_df = pd.DataFrame({
            'pressure': [rain_form.pressure.data],
            'temparature': [rain_form.temparature.data],
            'dewpoint': [rain_form.dewpoint.data],
            'humidity': [rain_form.humidity.data],
            'cloud': [rain_form.cloud.data],
            'sunshine': [rain_form.sunshine.data],
            'winddirection': [rain_form.winddirection.data],
            'windspeed': [rain_form.windspeed.data]
        })
        
        input_scaled = scaler.transform(input_df)
        predictions = model.predict(input_scaled)
        
        print(f"DEBUG: Raw prediction: {predictions[0]}")
        
        # FIXED: Handle encoder with fallback
        try:
            if encoder is not None:
                prediction = encoder.inverse_transform([predictions[0]])[0]
                print(f"DEBUG: Encoder result: {prediction}")
            else:
                raise Exception("Encoder not available")
        except Exception as e:
            print(f"DEBUG: Encoder error: {e}")
            # Fallback: Direct mapping based on your training data
            if predictions[0] == 0:
                prediction = 'no'  # Lowercase to match training data
            elif predictions[0] == 1:
                prediction = 'yes'  # Lowercase to match training data
            else:
                prediction = str(predictions[0])
            print(f"DEBUG: Using fallback prediction: {prediction}")
        
        new_prediction = Predictions(
            user_id = current_user.id,
            input_data = input_df.to_dict(),
            predicted_output = prediction
        )
        
        db.session.add(new_prediction)
        db.session.commit()
        flash("Prediction saved successfully")
        print("DEBUG: Saved to database")
    else:
        print("DEBUG: Form not validated or GET request")
        if rain_form.errors:
            print(f"DEBUG: Form errors: {rain_form.errors}")
    
    return render_template('dashboard.html', form = rain_form, prediction = prediction)

@app.route('/history')
@login_required
def history():
    user_history = Predictions.query.filter_by(user_id=current_user.id).all()
    print(f"DEBUG: Found {len(user_history)} history entries")
    return render_template('history.html', history=user_history)

@app.route('/logout')
def logout():
    logout_user()
    user_form = LoginForm()
    return render_template('login.html', form = user_form)

if __name__ == "__main__":
    app.run(debug = True)
