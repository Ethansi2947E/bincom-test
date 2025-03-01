# Election Results Management System

This Django application manages and displays election results from polling units and local government areas in Delta State, Nigeria.

## Features

1. View results from individual polling units
2. View summed total results from all polling units in a Local Government Area
3. Store results for new polling units

## Live Demo

The application is hosted at: [Coming Soon]

## Technologies Used

- Python 3.8+
- Django 5.0.2
- MySQL Database
- Tailwind CSS
- Crispy Forms with Tailwind

## Requirements

- Python 3.8+
- MySQL Server
- Virtual Environment (recommended)

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/Ethansi2947E/bincom-test.git
cd bincom-test
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the database:
- Open `election_project/settings.py`
- Update the database configuration with your MySQL credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bincom_test',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

5. Create and set up the database:
```bash
python setup_database.py
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Run the development server:
```bash
python manage.py runserver
```

8. Visit http://localhost:8000 in your web browser

## Project Structure

```
election/
├── election_project/        # Project settings
├── election_results/        # Main application
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   └── urls.py            # URL configurations
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   └── election_results/   # App templates
├── static/                 # Static files
├── manage.py              # Django management script
├── setup_database.py      # Database setup script
└── requirements.txt       # Project dependencies
```

## API Endpoints

1. `/` - View polling unit results
2. `/lga/` - View LGA results
3. `/store/` - Store new polling unit results

## Database Schema

The application uses the following main tables:
- `polling_unit` - Stores polling unit information
- `announced_pu_results` - Stores polling unit results
- `announced_lga_results` - Stores LGA results
- `lga` - Stores Local Government Area information
- `ward` - Stores ward information
- `states` - Stores state information

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make changes and commit (`git commit -am 'Add feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Ethan

## Acknowledgments

- Bincom Dev Center for the project requirements
- All contributors and testers 