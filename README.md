# Movie Sentiment Analysis Project

A Django-based web application that performs sentiment analysis on movie reviews and provides movie search functionality with fuzzy matching capabilities.

## Features

- Movie search with fuzzy matching for misspelled titles
- Sentiment analysis for movie reviews
- User-friendly interface with responsive design
- Movie information display including ratings and release dates
- Auto-correction suggestions for movie titles

## Project Structure

```
sentiment_project/
├── data/
│   └── MoviesTopRated.csv      # Movie dataset
├── sentiment_app/
│   ├── static/
│   │   └── css/
│   │       └── stylesheet.css   # Application styling
│   ├── templates/
│   │   └── index.html          # Main application template
│   ├── ml_model.py             # Sentiment analysis model
│   ├── views.py                # Application views
│   ├── urls.py                 # URL configurations
│   └── models.py               # Database models
└── sentiment_project/
    ├── settings.py             # Project settings
    └── urls.py                 # Project URL routing

```

## Technology Stack

- Python 3.13
- Django 5.2.6
- scikit-learn (for machine learning)
- pandas (for data handling)
- joblib (for model serialization)
- HTML/CSS for frontend

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/ABHISHEK2222222/sentiment_project.git
   cd sentiment_project
   ```

2. Create and activate virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install required packages:
   ```bash
   pip install django scikit-learn pandas joblib numpy
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application at:
   ```
   http://127.0.0.1:8000/
   ```

## Usage

1. **Movie Search:**
   - Enter a movie title in the search box
   - The system will find exact or similar matches
   - If a title is misspelled, suggestions will be shown

2. **Sentiment Analysis:**
   - Enter a movie review in the text area
   - Click "Analyze" to get the sentiment prediction
   - Results will show whether the sentiment is positive or negative

## Project Components

- **ML Model (`ml_model.py`)**: Contains the sentiment analysis model implementation
- **Views (`views.py`)**: Handles HTTP requests and responses
- **Templates (`index.html`)**: User interface implementation
- **Static Files**: CSS styling and frontend assets
- **URL Configuration**: Routes for the web application

## Development

1. **Virtual Environment**
   - Always use the virtual environment
   - Activate it using `.\venv\Scripts\Activate.ps1`

2. **Dependencies**
   - Main requirements: Django, scikit-learn, pandas, joblib
   - Install using pip within the virtual environment

3. **Database**
   - Uses SQLite by default
   - Migrations should be run after model changes

## Troubleshooting

1. **Virtual Environment Issues**
   - Ensure you're in the correct directory
   - Use the correct activation script for your shell
   - Check Python version compatibility

2. **Import Errors**
   - Verify all required packages are installed
   - Ensure virtual environment is activated
   - Check Python path settings

3. **Model Loading Issues**
   - Verify model file exists in the correct location
   - Check joblib version compatibility

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

ABHISHEK2255

---
Feel free to contribute to this project by submitting issues or pull requests.
