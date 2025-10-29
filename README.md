# ⚡ EcoWatt: Smart Energy Consumption Forecasting

A comprehensive machine learning project that forecasts energy consumption using time series analysis and provides an intuitive web interface for data visualization and prediction.

## 📋 Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Data Format](#data-format)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## ✨ Features

### User Features
- **Synthetic Data Generation**: Create realistic energy consumption data with seasonal patterns
- **CSV Upload Support**: Upload your own historical energy data with flexible date/time formats
- **Machine Learning Forecasting**: Time series prediction using linear regression with lag features
- **Interactive Web Interface**: Built with Streamlit for easy data exploration
- **Data Visualization**: Charts and statistics for historical and forecasted data
- **Export Functionality**: Download forecast results as CSV files
- **User Registration**: Create personal accounts for data management

### Admin Features
- **User Management**: View, manage, and delete user accounts
- **System Analytics**: Monitor system performance and data statistics
- **Data Management**: Generate and manage system-wide energy data
- **Model Training**: Train and update ML models for the system
- **Admin Dashboard**: Comprehensive overview of system status and users

## 🛠 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Web browser (Chrome, Firefox, Safari, etc.)

## 📦 Installation & Setup

### Step 1: Prepare the Project Folder
- Copy the entire `EcoWatt` folder to your target system
- Place it in a convenient location (e.g., `C:\Users\YourName\Desktop\EcoWatt` or `~/Desktop/EcoWatt` on Linux/Mac)

### Step 2: Set Up Virtual Environment (Recommended)
Open Command Prompt/Terminal and navigate to the EcoWatt directory:

**Windows:**
```bash
cd C:\Users\YourName\Desktop\EcoWatt
python -m venv venv_new
venv_new\Scripts\activate
```

**Linux/Mac:**
```bash
cd ~/Desktop/EcoWatt
python3 -m venv venv_new
source venv_new/bin/activate
```

### Step 3: Install Dependencies
With the virtual environment activated, run:

```bash
pip install -r requirements.txt
```

This will install:
- streamlit (web interface)
- pandas (data manipulation)
- numpy (numerical computations)
- scikit-learn (machine learning)
- matplotlib (plotting)
- tensorflow (deep learning - for advanced models)
- openpyxl (Excel file handling)
- joblib (model serialization)
- plotly (interactive charts)
- paho-mqtt (IoT connectivity)

## 🏗 Project Structure

```
EcoWatt/
│
├── main.py               # Main application entry point with routing
├── login.py              # Login and registration pages
├── app.py                # User dashboard - energy forecasting interface
├── admin_dashboard.py    # Admin dashboard - user management and analytics
├── auth.py               # Authentication and user management functions
├── data_generator.py     # Synthetic data generation script
├── model.py              # Machine learning model and prediction logic
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── users.xlsx            # Regular user accounts data
├── admin_users.xlsx      # Admin user accounts data
├── energy_data.csv       # Generated synthetic data (created after running)
└── energy_model.pkl      # Trained ML model (created after training)
```

## 🚀 Running the Project

### Quick Start (Windows)
1. Open Command Prompt and navigate to the EcoWatt folder:
   ```bash
   cd C:\path\to\EcoWatt
   ```

2. Activate virtual environment:
   ```bash
   venv_new\Scripts\activate
   ```

3. Run the application:
   ```bash
   streamlit run main.py
   ```

4. Open browser and go to: `http://localhost:8501`

### Quick Start (Linux/Mac)
1. Open Terminal and navigate to the EcoWatt folder:
   ```bash
   cd /path/to/EcoWatt
   ```

2. Activate virtual environment:
   ```bash
   source venv_new/bin/activate
   ```

3. Run the application:
   ```bash
   streamlit run main.py
   ```

4. Open browser and go to: `http://localhost:8501`

### Alternative Run Methods

**Run User Dashboard Only:**
```bash
streamlit run app.py
```

**Run Admin Dashboard Only:**
```bash
streamlit run admin_dashboard.py
```

**Run with Custom Port:**
```bash
streamlit run main.py --server.port 8502
```

### First Time Setup

1. **Access the Application**
   - Open `http://localhost:8501` in your web browser
   - You'll see the login page

2. **Login or Register**
   - **For Users**: Select "User" tab and login with existing credentials or register a new account
   - **For Admins**: Select "Admin" tab and login with admin credentials

**Default Login Credentials:**

**Regular Users:**
- Username: `user1` | Password: `password123`
- Username: `user2` | Password: `password123`

**Admin Users:**
- Username: `admin` | Password: `admin123`

### Using the Application

1. **Generate or Upload Data**
   - Click "📤 Upload Data" tab
   - Choose "Generate Synthetic Data" or "Upload CSV"
   - Generate sample data or upload your own CSV file

2. **Analyze Data**
   - Click "📊 Analyze Data" tab
   - View statistics, charts, and insights
   - Train the AI model when ready

3. **Generate Forecasts**
   - Click "🔮 Generate Forecast" tab
   - Set forecast parameters (days, confidence level)
   - Click "🚀 Generate AI Forecast"

4. **View Results**
   - Click "📈 View Results" tab
   - See combined historical + forecast charts
   - Download forecast data as CSV

### Admin Features (Admin Login Required)

**Access Admin Dashboard:**
- Login with admin credentials (username: `admin`, password: `admin123`)
- Navigate through admin sections: Dashboard Overview, User Management, System Data, Analytics

**User Management:**
- View all registered users
- Delete user accounts (except your own)
- Monitor user registration activity

**System Management:**
- Generate system-wide energy data
- Train global AI models
- View system analytics and performance metrics

### Troubleshooting Common Issues

**Port Already in Use:**
```bash
# Use a different port
streamlit run main.py --server.port 8502
```

**Virtual Environment Issues:**
```bash
# Recreate virtual environment
rmdir /s venv_new
python -m venv venv_new
venv_new\Scripts\activate
pip install -r requirements.txt
```

**Dependencies Installation Fails:**
```bash
# Upgrade pip first
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Model Training Fails:**
- Ensure you have at least 8 days of data
- Check that data contains valid numeric values
- Try regenerating synthetic data if upload fails

## 📊 Data Format

### Required Columns
- `date`: Date in YYYY-MM-DD format (e.g., 2023-01-01)
- `consumption_kwh`: Energy consumption in kilowatt-hours (numeric)

### Optional Column
- `time`: Time in HH:MM:SS format (e.g., 14:30:00)

### CSV Examples

**Date Only:**
```csv
date,consumption_kwh
2023-01-01,120.5
2023-01-02,118.8
2023-01-03,125.2
```

**Date and Time:**
```csv
date,time,consumption_kwh
2023-01-01,08:00:00,120.5
2023-01-01,14:30:00,150.2
2023-01-02,08:00:00,118.8
```

### Data Requirements
- Dates must be in chronological order (app will sort automatically)
- Consumption values should be positive numbers
- No missing values in required columns
- Minimum 8 data points for model training

## 🧠 How It Works

### Data Processing
1. **Input Validation**: Checks for required columns and data types
2. **Date/Time Handling**: Combines date and time columns if present
3. **Data Sorting**: Ensures chronological order for time series analysis

### Machine Learning Model
- **Algorithm**: Linear Regression with lag features
- **Features**: Uses previous 7 days of consumption as predictors
- **Training**: Splits data into 80% training, 20% testing
- **Prediction**: Generates future forecasts based on recent patterns

### Forecasting Process
1. Takes the last 7 days of actual consumption
2. Uses the trained model to predict the next day
3. Uses that prediction as input for the following day
4. Repeats for the desired forecast period

### Synthetic Data Generation
- **Base Consumption**: 100 kWh average
- **Seasonal Patterns**: Yearly cycles (±20 kWh)
- **Weekly Patterns**: Daily variations (±10 kWh)
- **Random Noise**: Realistic variability (±5 kWh)
- **Trend**: Slight upward consumption trend

## 🔧 Troubleshooting

### Common Issues

**"Module not found" errors:**
- Ensure virtual environment is activated: `venv_new\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`
- Upgrade pip: `python -m pip install --upgrade pip`

**App won't start:**
- Check if port 8501 is available (close other Streamlit apps)
- Try different port: `streamlit run main.py --server.port 8502`
- Ensure Python path is correct

**Login issues:**
- Use default credentials: user1/password123 or admin/admin123
- Check if Excel files (users.xlsx, admin_users.xlsx) exist
- Try registering a new account

**CSV upload fails:**
- Required columns: `date`, `consumption_kwh`
- Date format: YYYY-MM-DD (e.g., 2023-01-01)
- No missing values in required columns
- File size limit: Check Streamlit documentation

**Model training fails:**
- Minimum 8 data points required
- All consumption values must be numeric
- Dates must be parseable
- Check console for detailed error messages

**Forecast generation fails:**
- Train model first in "Analyze Data" tab
- Ensure data is loaded
- Check if energy_model.pkl exists
- Verify sufficient historical data

**Virtual environment issues:**
- Recreate venv: `rmdir /s venv_new && python -m venv venv_new`
- Activate: `venv_new\Scripts\activate`
- Reinstall: `pip install -r requirements.txt`

### Performance Tips
- Use Chrome browser for best performance
- Close other applications using port 8501
- For large datasets (>10,000 rows), consider data sampling
- Keep virtual environment lightweight

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add new feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For questions or issues:
1. Check the troubleshooting section above
2. Review the code comments in the Python files
3. Ensure all prerequisites are met

---

**Built with ❤️ using Streamlit, scikit-learn, and Python**
