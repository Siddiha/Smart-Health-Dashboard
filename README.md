# Smart Health Dashboard

A Flask-based web application for monitoring and visualizing health metrics.

## Features

- Real-time health data monitoring
- Interactive dashboard with charts
- Data visualization for key health metrics
- RESTful API for data access

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/smart-health-dashboard.git
cd smart-health-dashboard
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   Create a `.env` file in the root directory with the following content:

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
```

## Running the Application

1. Initialize the database:

```bash
flask db init
flask db migrate
flask db upgrade
```

2. Run the development server:

```bash
flask run
```

The application will be available at `http://localhost:5000`

## Project Structure

```
smart_health_dashboard/
├── app/
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   │   ├── templates/
│   │   │   └── index.html
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── utils.py
│   ├── data/
│   │   └── sample_health_data.csv
│   │   ├── notebooks/
│   │   │   └── data_exploration.ipynb
│   │   └── .env
│   │   └── .gitignore
│   │   └── app.py
│   │   └── requirements.txt
│   └── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
