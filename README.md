# 🌧️ Rainfall Prediction Web Application

A full-stack machine learning web application that predicts rainfall based on weather parameters. Built with Flask and deployed with user authentication and prediction history tracking.

## 📋 Project Overview

This project demonstrates end-to-end machine learning deployment by creating a web application that:

- Predicts rainfall probability using weather data
- Provides secure user authentication and registration
- Tracks individual user prediction history
- Offers a clean, responsive user interface

**Tech Stack**: Python, Flask, scikit-learn, SQLAlchemy, HTML/CSS, Flask WTForms

## ✨ Key Features

## 🔐 User Authentication System

- Secure user registration and login
- Password hashing with Werkzeug security
- Session management with Flask-Login
- Protected routes and user-specific data

## 🤖 Machine Learning Integration

- Pre-trained Logistic Regression model for rainfall prediction
- Real-time predictions based on 8 weather parameters
- Robust error handling and model fallback mechanisms
- Feature scaling and data preprocessing pipeline

## 📊 Weather Parameters

The model uses the following inputs to make predictions:

- Atmospheric Pressure (hPa)
- Average Temperature (°C)
- Dewpoint (°C)
- Humidity (%)
- Cloud Cover (%)
- Sunshine Duration (hours)
- Wind Direction (degrees)
- Wind Speed (km/h)

## 💾 Data Persistence

- SQLite database for development, PostgreSQL for production
- User-specific prediction history tracking
- Secure data storage with proper relationships

## 🎨 Professional UI/UX

- Modern, responsive design with CSS gradients
- Clean form interfaces with real-time validation
- Interactive navigation and user feedback
- Mobile-friendly responsive layout

## 🛠️ Technical Implementation

**Backend Architecture**  
```python
# Core components
- Flask web framework with blueprints
- SQLAlchemy ORM for database operations
- WTForms for secure form handling
- joblib for model serialization
- Pandas for data preprocessing
```  

**Machine Learning Pipeline**
```python
# Model workflow
1. Data preprocessing with StandardScaler
2. Logistic Regression classification
3. Label encoding for categorical outputs
4. Real-time prediction serving
```

**Security Features**

- CSRF protection with Flask-WTF
- Password hashing with salt
- Session-based authentication
- Input validation and sanitization

## 📈 Project Insights

**What I Learned**  

- **Model Deployment:** Moving from Jupyter notebooks to production web apps
- **Full-Stack Development:** Integrating ML models with web frameworks
- **User Experience:** Creating intuitive interfaces for technical applications
- **Production Challenges:** Handling model serialization, database migrations, and error recovery

**Technical Challenges Solved**

- **Model Loading:** Implemented robust error handling for pickle file loading
- **Data Pipeline:** Created seamless data flow from web forms to ML predictions
- **State Management:** Handled user sessions and prediction history efficiently
- **Responsive Design:** Built mobile-friendly interfaces for better accessibility

## 🔧 Installation & Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/rainfall-prediction-app.git
cd rainfall-prediction-app

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```
## 📊 Model Performance

- **Algorithm:** Logistic Regression
- **Features:** 8 weather parameters
- **Output:** Binary classification (Rain/No Rain)

## 🎯 Future Enhancements

- Add weather data visualization charts
- Implement rainfall amount regression model
- Create REST API endpoints for mobile apps
- Add model retraining capabilities
- Integrate real-time weather data APIs

## 👨‍💻 About This Project

This project represents my journey in bridging the gap between data science theory and practical web development. It showcases my ability to:

- Deploy machine learning models in production environments
- Build secure, user-friendly web applications
- Handle real-world challenges in ML deployment
- Create end-to-end solutions that users can actually interact with

**Built By:** Chitraksh Sharma
